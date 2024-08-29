from flask import Flask, request, jsonify
from google.cloud import vision
from google.oauth2 import service_account
import requests
from flask_cors import CORS
from dotenv import load_dotenv
import os
import re
from googlesearch import search
from profitability_calculator import analyze_profitability  

load_dotenv()  # Load environment variables from the .env file

app = Flask(__name__)  # Initialize Flask app
CORS(app)  # Enable Cross-Origin Resource Sharing (CORS) to allow requests from the React frontend

# Setup Google Cloud Vision API client
key_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')  # Get the path to the Google Cloud service account credentials from environment variables
credentials = service_account.Credentials.from_service_account_file(key_path)  # Load the credentials from the file
client = vision.ImageAnnotatorClient(credentials=credentials)  # Initialize the Vision API client with the credentials

# Setup Canopy API
CANOPY_API_URL = 'https://graphql.canopyapi.co/'  # Canopy API GraphQL endpoint
CANOPY_API_KEY = os.getenv('CANOPY_API_KEY')  # Get the Canopy API key from environment variables

@app.route('/api/upload', methods=['POST'])  # Define the route and method for the upload API endpoint
def upload_file():
    file = request.files['file']  # Get the uploaded file from the request
    buy_price = float(request.form.get('buyPrice', 0))  # Get the buy price from the form data, defaulting to 0 if not provided

    content = file.read()  # Read the content of the uploaded file
    image = vision.Image(content=content)  # Create an Image object for the Vision API
    response = client.text_detection(image=image)  # Call the Vision API to detect text in the image
    texts = response.text_annotations  # Get the detected text annotations from the response

    if response.error.message:  # Check if there was an error in the Vision API response
        return jsonify({'error': response.error.message}), 500  # Return an error response with a 500 status code

    extracted_text = texts[0].description if texts else ""  # Extract the first detected text annotation (the main text) or an empty string if none found
    isbn = extract_isbn(extracted_text)  # Extract the ISBN from the detected text using a custom function

    if not isbn:  # Check if no ISBN was found
        return jsonify({'error': 'No ISBN found in the text'}), 400  # Return an error response with a 400 status code

    search_results = google_search_isbn(isbn)  # Perform a Google search for the ISBN and store the results
    asin = find_asin_in_results(search_results)  # Extract the ASIN from the search results using a custom function

    if not asin:  # Check if no ASIN was found
        return jsonify({'error': 'No ASIN found in Google search results'}), 400  # Return an error response with a 400 status code

    amazon_results = call_amazon_api(asin)  # Call the Canopy API to get product details using the ASIN
    amazon_product = amazon_results.get('data', {}).get('amazonProduct')  # Extract the Amazon product details from the API response

    if not amazon_product:  # Check if no product details were found
        return jsonify({'error': 'Product details not found'}), 400  # Return an error response with a 400 status code

    concise_response = {
        'title': amazon_product.get('title'),  # Extract and include the product title
        'isbn': isbn,  # Include the extracted ISBN
        'asin': asin,  # Include the ASIN
        'price': amazon_product.get('price', {}).get('display'),  # Extract and include the product price
        'main_image_url': amazon_product.get('mainImageUrl')  # Extract and include the main image URL
    }

    formatted_profitability = analyze_profitability(amazon_product, buy_price)  # Calculate profitability using the extracted product details and user-provided buy price

    return jsonify({
        'product_details': concise_response,  # Return the concise product details in the response
        'profitability': formatted_profitability  # Return the profitability calculation in the response
    })

def extract_isbn(text):
    # Use regex to search for an ISBN-10 or ISBN-13 in the text
    match = re.search(r'(\b\d{1,5}[-\s]?\d{1,7}[-\s]?\d{1,7}[-\s]?\d{1,7}[-\s]?\d|X\b|\b\d{3}[-\s]?\d{1,5}[-\s]?\d{1,7}[-\s]?\d{1,7}[-\s]?\d)\b', text)
    # If a match is found, return the ISBN without dashes or spaces, otherwise return None
    return match.group(0).replace('-', '').replace(' ', '') if match else None

def google_search_isbn(isbn):
    query = f"{isbn} amazon"  # Create a search query using the ISBN and "amazon"
    search_results = search(query, num_results=5)  # Perform a Google search and get the top 5 results
    return search_results  # Return the search results

def extract_asin_from_url(url):
    # Use regex to search for an ASIN (a 10-character alphanumeric identifier) in the Amazon URL
    match = re.search(r'/dp/([A-Z0-9]{10})', url)
    return match.group(1) if match else None  # If a match is found, return the ASIN, otherwise return None

def find_asin_in_results(search_results):
    for result in search_results:  # Iterate through the search results
        if "amazon.com" in result:  # Check if the result is an Amazon link
            asin = extract_asin_from_url(result)  # Extract the ASIN from the URL
            if asin:
                return asin  # Return the ASIN if found
    return None  # Return None if no ASIN was found in the search results

def call_amazon_api(asin):
    # Define the GraphQL query to fetch product details using the ASIN
    query = """
    query amazonProduct($asin: String!) {
      amazonProduct(input: {asin: $asin}) {
        title
        mainImageUrl
        rating
        price {
          display
        }
      }
    }
    """
    headers = {
        'Content-Type': 'application/json',  # Set the content type to JSON
        'API-KEY': CANOPY_API_KEY,  # Include the Canopy API key in the headers
    }
    payload = {
        'query': query,  # Include the GraphQL query in the payload
        'variables': {'asin': asin}  # Pass the ASIN as a variable to the query
    }

    response = requests.post(CANOPY_API_URL, json=payload, headers=headers)  # Make a POST request to the Canopy API

    if response.status_code == 200:  # Check if the API request was successful
        return response.json()  # Return the JSON response from the API
    else:
        return {'error': 'Failed to fetch data from Canopy API'}  # Return an error message if the API call failed

if __name__ == '__main__':
    app.run(debug=True)  
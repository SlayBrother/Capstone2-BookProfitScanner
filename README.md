ISBN Photo-to-Text Reading Application
This application processes images of book ISBNs, extracts text using the Google Cloud Vision API, and performs a profitability analysis by querying Amazon product information via the Canopy API.
https://capstone2-bookprofitscanner.onrender.com/
Features
Image Upload: Easily upload an image containing an ISBN.
Text Extraction: Utilize the Google Cloud Vision API to extract text from the uploaded image.
Product Lookup: Automatically retrieve product details from Amazon using the extracted ISBN.
Profitability Calculation: Calculate the profitability of the product based on the current market price and a user-provided buy price.
Tech Stack
Frontend: React, Material-UI (MUI)
Backend: Flask, Google Cloud Vision API, Canopy API
Deployment: Flask server
Installation
Prerequisites
Python 3.x
Node.js (for the frontend)
Google Cloud account with Vision API enabled
Canopy API credentials
API Credentials Setup
Environment Variables: Store your API credentials in a .env file within your application directory.
Both Google Cloud Vision API and Canopy API offer free trial versions, but charges apply after exceeding the free usage limits.
Google Cloud Vision API: First 1,000 requests are free.
Canopy API: First 100 requests are free.
Google Cloud Vision API Setup
Create a new project in the Google Cloud Console.
Enable billing (charges apply after exceeding the free tier).
Navigate to the Vision API and follow the instructions to generate your API key.
Save your credentials in the .env file: GOOGLE_APPLICATION_CREDENTIALS=path/to/your/google-credentials.json
For more detailed guidance, refer to Google Cloud's official documentation.
Canopy API Key Setup
Sign up at the Canopy API website and create an account.
Add a credit card (charges apply after exceeding the free tier).
Your API key will be provided immediately.
Save it in your .env file: CANOPY_API_KEY=your-canopy-api-key
Install Dependencies
To install all required dependencies, run: pip install -r requirements.txt
Usage
Upload an Image: Click the "Choose Image File" button to upload an image containing an ISBN.
Enter Buy Price: Input the price at which you acquired the product.
Submit: Click "Upload" to process the image.
View Results: After processing, view the extracted details and profitability information.
Profitability Calculation
Profitability is calculated using the following components:

Sale Price: Retrieved from Amazon.
Referral Fee: 15% of the Sale Price.
Closing Fee: $1.80.
FBA Fee: 40% of the Sale Price.
Inventory Charge: 0.25% of the Sale Price.
Shipping Fee: 2.67% of the Sale Price.
Buy Price: User-provided.
Formula:
Profitability = Sale Price - (Referral Fee + Closing Fee + FBA Fee + Inventory Charge + Shipping Fee + Buy Price)

Future Enhancements
Amazon Product Advertising API Integration
Though this project currently utilizes the Canopy API, future development aims to integrate Amazon's Product Advertising API for:

Better Pricing Accuracy: Access to real-time pricing.
Faster Processing: Quicker data retrieval.
Planned Features
Multi-Scan Capability: Enable users to scan multiple books in one session and aggregate the profitability analysis.
User Authentication: Add login and logout functionality to save scans and profitability analyses.
Rejected Publisher Alert: Notify users if a scanned book is published by a restricted publisher (e.g., Disney, Marvel).
Front Cover Text Recognition: Extend OCR to allow processing of book cover text to identify books without relying on the ISBN.
Multi-Book OCR Processing: Process multiple books from a single image, performing profitability analysis on all books.
Contributing
Feel free to submit issues or pull requests for any changes or enhancements.

License
This project is licensed under the MIT License.

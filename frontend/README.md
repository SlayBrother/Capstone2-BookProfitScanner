ISBN Photo-to-Text Reading Application
This application processes images of book ISBNs, extracts text using the Google Cloud Vision API, and performs a profitability analysis based on the extracted ISBN by querying Amazon product information via the Canopy API.

Features
Image Upload: Easily upload an image containing an ISBN.
Text Extraction: Utilize the Google Cloud Vision API to extract text from the uploaded image.
Product Lookup: Automatically search for and retrieve product details from Amazon using the extracted ISBN.
Profitability Calculation: Calculate the profitability of the product based on the current market price and a user-provided buy price.

Tech Stack
Frontend: React, MUI (Material-UI)
Backend: Flask, Google Cloud Vision API, Canopy API
Deployment: Flask server

Installation
Prerequisites
Python 3.x
Node.js (for running the frontend)
A Google Cloud account with the Vision API enabled.
Canopy API credentials.

API Credentials Setup
Environment Variables: Store your API credentials in a .env file within your application directory. Both Google Cloud Vision API and Canopy API offer free trial versions, but charges apply after exceeding the free usage limits (as of writing: the first 1,000 requests are free for Google Cloud Vision API, and the first 100 requests are free for Canopy API).

Google Cloud Vision API Setup
Create a new project in the Google Cloud Console.
Enable billing by adding a credit card (charges apply after exceeding the free tier).
Navigate to the Vision API and follow the instructions to generate your API key.
Save your credentials in your .env file: GOOGLE_APPLICATION_CREDENTIALS=path/to/your/google-credentials.json
For more detailed guidance, refer to Google Cloud's official documentation.

Canopy API Key Setup
Sign up at the Canopy API website and create an account.
Add a credit card (charges apply after exceeding the free tier).
Your API key will be provided immediately. Save it in your .env file: CANOPY_API_KEY=your-canopy-api-key

Install Dependencies
Ensure all requirements are installed by running: pip install -r requirements.txt

Usage
Upload an Image: Click the "Choose Image File" button to upload an image containing an ISBN.
Enter Buy Price: Input the price at which you acquired the product.
Submit: Click "Upload" to process the image.
View Results: After processing, view the extracted details and profitability information below the form.
Profitability Calculation
Profitability is calculated using the following components:

Sale Price: Retrieved from Amazon.
Referral Fee: 15% of the Sale Price.
Closing Fee: $1.80.
FBA Fee: 40% of the Sale Price.
Inventory Charge: 0.25% of the Sale Price.
Shipping Fee: 2.67% of the Sale Price.
Buy Price: User-provided.
Formula - Profitability = Sale Price - (Referral Fee + Closing Fee + FBA Fee + Inventory Charge + Shipping Fee + Buy Price)

Future Enhancements
Amazon Product Advertising API Integration
While this project currently utilizes the Canopy API for retrieving Amazon product information, the ideal approach would be to directly integrate with Amazon's Product Advertising API. Unfortunately, gaining access to this API is more challenging due to stringent eligibility requirements, but it offers several benefits, including:

Better Pricing Accuracy: Access to real-time and more accurate pricing directly from Amazon.
Faster Processing: Potentially faster API responses, resulting in quicker data retrieval and processing.
Though I wasn't able to implement this in the current version, integrating Amazon's API remains a priority for future development to enhance both the accuracy and efficiency of the application.

Planned Features
Looking ahead, here are some key features and improvements I plan to incorporate:

Interactive Storage System:
Multi-Scan Capability: Enable users to scan multiple books in one session and aggregate the profit or loss analysis. This will allow users to evaluate the profitability of multiple items together, simplifying batch processing and decision-making.
User Authentication:

Simple User System: Implement a basic user system to allow login and logout functionality. This will facilitate personalized user experiences, including saving scans and profitability analyses for future reference.
Rejected Publisher Alert:

Publisher Restriction Notification: Add a feature to alert users if a scanned book is published by a commonly restricted publisher, such as Disney, Oxford, Marvel, or National Geographic. This alert will inform users that selling the book on Amazon might be prohibited due to publisher agreements, thereby preventing potential compliance issues.
Front Cover Text Recognition:

Enhanced OCR Capabilities: Extend the OCR functionality to allow users to take a picture of the front cover of a book. The application will then determine if the book is profitable to sell, eliminating the need to rely solely on the ISBN on the back cover.
Multi-Book OCR Processing:

Batch Processing: Ultimately, the goal is to enable the application to recognize and process multiple books from a single image. This would involve the OCR identifying each book individually and performing profitability analysis on all books in the image simultaneously, greatly improving efficiency for users managing large inventories.

Contributing
Feel free to submit issues or pull requests for any changes or enhancements.

License
This project is licensed under the MIT License.
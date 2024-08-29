import React, { useState } from 'react';
import axios from 'axios';
import { Box, Button, Alert, Typography, TextField, CircularProgress } from '@mui/material';

const UploadForm = ({ darkMode }) => {
  const [file, setFile] = useState(null);
  const [fileName, setFileName] = useState(null);
  const [buyPrice, setBuyPrice] = useState(''); 
  const [response, setResponse] = useState(null);
  const [error, setError] = useState(null);
  const [productDetails, setProductDetails] = useState(null);
  const [loading, setLoading] = useState(false);

  // Handler to manage file selection
  const handleFileChange = (event) => {
    const selectedFile = event.target.files[0]; // Get the selected file from input
    setFile(selectedFile); // Update the file state
    setFileName(selectedFile.name); // Update the fileName state with the selected file's name
  };

  // Handler to manage buy price input change
  const handleBuyPriceChange = (event) => {
    setBuyPrice(event.target.value); // Update the buy price state
  };

  // Handler to manage form submission
  const handleSubmit = async (event) => {
    event.preventDefault(); // Prevent the default form submission behavior
    setLoading(true); // Show the loading spinner
    const formData = new FormData(); // Create a FormData object to hold the file and buy price
    formData.append('file', file); // Append the selected file to the form data
    formData.append('buyPrice', buyPrice); // Append the buy price to the form data

    try {
      // Make a POST request to the /api/upload endpoint with the form data
      const res = await axios.post('/api/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data', // Set content type to multipart for file upload
        },
      });

      setResponse(res.data); // Update the response state with the API response
      setProductDetails(res.data.product_details); // Update the product details state with the API data
      setError(null); // Clear any previous errors
    } catch (err) {
      // Handle any errors from the API request
      setError(err.response?.data?.error || 'An error occurred'); // Set error message
      setResponse(null); // Clear the response state
      setProductDetails(null); // Clear the product details state
    } finally {
      setLoading(false); // Hide the loading spinner
    }
  };

  // Function to determine profitability color based on the value
  const getProfitabilityColor = (profitability) => {
    const profitValue = parseFloat(profitability.replace('$', '')); // Convert profitability string to a float
    return profitValue >= 2.00 ? 'green' : 'red'; // Return green if profitable, red otherwise
  };

  return (
    <Box sx={{ mt: 3 }}>
      {/* Centered Layout for Input Fields and Buttons */}
      <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', mb: 3 }}>
        <TextField
          label="Buy Price"
          variant="outlined"
          value={buyPrice} // Controlled input bound to buyPrice state
          onChange={handleBuyPriceChange} // Update buyPrice state on input change
          sx={{ mr: 2, width: '150px' }} // Adjust the width to match buttons
          inputProps={{ inputMode: 'numeric', pattern: '[0-9]*' }} // Restrict input to numeric values
        />
        <input
          accept="image/*" // Restrict file input to images
          style={{ display: 'none' }} // Hide the input element
          id="raised-button-file"
          type="file"
          onChange={handleFileChange} // Update file state on file selection
        />
        <label htmlFor="raised-button-file">
          <Button variant="contained" component="span">
            {fileName ? fileName : "Choose Image File"} 
          </Button>
        </label>
        <Button variant="contained" color="primary" type="submit" onClick={handleSubmit} sx={{ ml: 2 }}>
          Upload
        </Button>
      </Box>

      {/* Loading Indicator */}
      {loading && (
        <Box sx={{ mt: 3, textAlign: 'center' }}>
          <CircularProgress /> {/* Show spinner during file upload */}
        </Box>
      )}

      {/* Display Product Details and Profitability Below with dark/light mode logic*/}
      {productDetails && (
        <Box sx={{ mt: 3 }}>
          <Typography variant="h6" sx={{ color: darkMode ? '#ffffff' : '#000000' }}>Product Details:</Typography>
          <Typography sx={{ color: darkMode ? '#ffffff' : '#000000' }}>Title: {productDetails.title}</Typography>
          <Typography sx={{ color: darkMode ? '#ffffff' : '#000000' }}>ISBN: {productDetails.isbn}</Typography>
          <Typography sx={{ color: darkMode ? '#ffffff' : '#000000' }}>ASIN: {productDetails.asin}</Typography>
          <Typography sx={{ color: darkMode ? '#ffffff' : '#000000' }}>Price: {productDetails.price}</Typography>
          <Typography sx={{ color: getProfitabilityColor(response.profitability.profitability) }}>
            Profitability: {response.profitability.profitability}
          </Typography>
          {productDetails.main_image_url && (
            <Box sx={{ mt: 2 }}>
              <img src={productDetails.main_image_url} alt={productDetails.title} style={{ maxWidth: '40%' }} /> {/* Display product image */}
            </Box>
          )}
        </Box>
      )}

      {/* Error Message Display */}
      {error && (
        <Alert severity="error" sx={{ mt: 3 }}>
          {error} {/* Display error message if present */}
        </Alert>
      )}
    </Box>
  );
};

export default UploadForm;
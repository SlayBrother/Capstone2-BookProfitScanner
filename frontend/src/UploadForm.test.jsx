import React from 'react';
import { render, fireEvent, screen, waitFor } from '@testing-library/react';
import axios from 'axios';
import UploadForm from './UploadForm';

// react testing library - check it out


// Mock axios
jest.mock('axios');

describe('UploadForm Component', () => {
  
  // Test: Component Renders Properly
  it('renders without crashing', () => {
    render(<UploadForm darkMode={false} />);
    
    expect(screen.getByText(/Choose Image File/i)).toBeInTheDocument();
    expect(screen.getByText(/Upload/i)).toBeInTheDocument();
  });

  // Test: File Selection Updates State
  it('updates file name on file selection', () => {
    render(<UploadForm darkMode={false} />);
    
    const file = new File(['dummy content'], 'example.png', { type: 'image/png' });
    const input = screen.getByLabelText(/Choose Image File/i);
    
    fireEvent.change(input, { target: { files: [file] } });
    
    expect(screen.getByText(/example.png/i)).toBeInTheDocument();
  });

  // Test: Loading Spinner Display During API Call
  it('displays loading spinner during API call', async () => {
    render(<UploadForm darkMode={false} />);
    
    const file = new File(['dummy content'], 'example.png', { type: 'image/png' });
    const input = screen.getByLabelText(/Choose Image File/i);
    fireEvent.change(input, { target: { files: [file] } });
    
    axios.post.mockImplementationOnce(() =>
      new Promise((resolve) => setTimeout(() => resolve({ data: { product_details: {}, profitability: {} } }), 1000))
    );
    
    fireEvent.click(screen.getByText(/Upload/i));
    
    expect(screen.getByTestId('loading-spinner')).toBeInTheDocument();
    
    await waitFor(() => expect(screen.queryByTestId('loading-spinner')).not.toBeInTheDocument());
  });

  // Test: Successful API Call Displays Product Details
  it('displays product details on successful upload', async () => {
    const productDetails = {
      title: 'Example Book',
      isbn: '1234567890',
      asin: 'B00EXAMPLE',
      price: '$10.00',
      main_image_url: 'http://example.com/image.png',
    };
    const profitability = { profitability: '$5.00' };
    
    axios.post.mockResolvedValueOnce({ data: { product_details: productDetails, profitability } });
    
    render(<UploadForm darkMode={false} />);
    
    const file = new File(['dummy content'], 'example.png', { type: 'image/png' });
    const input = screen.getByLabelText(/Choose Image File/i);
    fireEvent.change(input, { target: { files: [file] } });
    
    fireEvent.click(screen.getByText(/Upload/i));
    
    await waitFor(() => {
      expect(screen.getByText(/Example Book/i)).toBeInTheDocument();
      expect(screen.getByText(/1234567890/i)).toBeInTheDocument();
      expect(screen.getByText(/B00EXAMPLE/i)).toBeInTheDocument();
      expect(screen.getByText(/\$10\.00/i)).toBeInTheDocument();
      expect(screen.getByText(/\$5\.00/i)).toBeInTheDocument();
      expect(screen.getByAltText(/Example Book/i)).toBeInTheDocument();
    });
  });

  // Test: Error Handling on Failed API Call
  it('displays an error message on upload failure', async () => {
    axios.post.mockRejectedValueOnce({ response: { data: { error: 'Upload failed' } } });
    
    render(<UploadForm darkMode={false} />);
    
    const file = new File(['dummy content'], 'example.png', { type: 'image/png' });
    const input = screen.getByLabelText(/Choose Image File/i);
    fireEvent.change(input, { target: { files: [file] } });
    
    fireEvent.click(screen.getByText(/Upload/i));
    
    await waitFor(() => {
      expect(screen.getByText(/Upload failed/i)).toBeInTheDocument();
    });
  });
});
import React, { useState } from 'react';
import { Container, Box, Typography } from '@mui/material';
import NavBar from './NavBar';
import UploadForm from './UploadForm';

const HomePage = () => {
    const [darkMode, setDarkMode] = useState(false);

    const toggleDarkMode = () => {
        setDarkMode(prevMode => !prevMode);
    };

    return (
        <div style={{ background: darkMode ? 'linear-gradient(135deg, #434343, #000000)' : 'linear-gradient(135deg, #f5f7fa, #c3cfe2)', minHeight: '100vh' }}>
            <NavBar toggleDarkMode={toggleDarkMode} darkMode={darkMode} />
            <Container maxWidth="md">
                <Box sx={{ textAlign: 'center', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', minHeight: '100vh' }}>
                    <Typography variant="h2" component="h1" gutterBottom sx={{ color: darkMode ? '#ffffff' : '#000000' }}>
                        Is your book profitable to sell on Amazon? Scan the barcode on the bad and find out!
                    </Typography>
                    <UploadForm darkMode={darkMode} />
                </Box>
            </Container>
        </div>
    );
};

export default HomePage;


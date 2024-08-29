import React from 'react';
import { AppBar, Toolbar, Typography, IconButton, Switch } from '@mui/material';
import { Brightness4 as Brightness4Icon, Brightness7 as Brightness7Icon } from '@mui/icons-material';

const NavBar = ({ toggleDarkMode, darkMode }) => {
    return (
        <AppBar position="static">
            <Toolbar>
                <Typography variant="h6" sx={{ flexGrow: 1 }}>
                    Photo to Text App
                </Typography>
                <IconButton
                    edge="end"
                    color="inherit"
                    aria-label="dark mode toggle"
                    onClick={toggleDarkMode}
                >
                    {darkMode ? <Brightness7Icon /> : <Brightness4Icon />}
                </IconButton>
                <Switch
                    checked={darkMode}
                    onChange={toggleDarkMode}
                    color="default"
                />
            </Toolbar>
        </AppBar>
    );
};

export default NavBar;
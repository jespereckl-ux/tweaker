#!/usr/bin/env python3
"""
UI Themes

Theme definitions for the application.
"""

class Theme:
    """UI Theme configuration."""
    
    LIGHT = {
        'bg_color': '#f0f0f0',
        'fg_color': '#000000',
        'button_color': '#007acc',
        'button_fg': '#ffffff',
        'danger_color': '#d32f2f',
        'success_color': '#388e3c',
        'warning_color': '#f57c00',
        'info_color': '#0288d1',
        'border_color': '#cccccc',
    }
    
    DARK = {
        'bg_color': '#1e1e1e',
        'fg_color': '#ffffff',
        'button_color': '#007acc',
        'button_fg': '#ffffff',
        'danger_color': '#f44336',
        'success_color': '#4caf50',
        'warning_color': '#ff9800',
        'info_color': '#2196f3',
        'border_color': '#424242',
    }
    
    @staticmethod
    def get_theme(name: str = 'DARK') -> dict:
        """Get theme by name.
        
        Args:
            name: Theme name ('LIGHT' or 'DARK')
            
        Returns:
            dict: Theme colors
        """
        if name.upper() == 'LIGHT':
            return Theme.LIGHT
        return Theme.DARK

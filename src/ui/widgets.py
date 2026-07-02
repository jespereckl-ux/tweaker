#!/usr/bin/env python3
"""
Reusable UI Widgets

Common UI components.
"""

import PySimpleGUI as sg


class Widgets:
    """Reusable UI widgets."""
    
    @staticmethod
    def create_titled_section(title: str, elements: list, key: str = None) -> list:
        """Create a titled section with border.
        
        Args:
            title: Section title
            elements: Elements to include
            key: Section key
            
        Returns:
            list: Section layout
        """
        return [
            [sg.Text(title, font=('Arial', 12, 'bold'))],
            [sg.Column(elements, key=key)]
        ]
    
    @staticmethod
    def create_info_box(text: str, color: str = 'lightblue') -> sg.Element:
        """Create an info box.
        
        Args:
            text: Info text
            color: Background color
            
        Returns:
            sg.Element: Info box
        """
        return sg.Multiline(
            text,
            size=(60, 4),
            disabled=True,
            background_color=color,
            text_color='black',
            no_scrollbar=True
        )
    
    @staticmethod
    def create_risk_indicator(risk_level: str) -> str:
        """Create risk level indicator.
        
        Args:
            risk_level: Risk level string
            
        Returns:
            str: Formatted risk indicator
        """
        indicators = {
            'SAFE': '✓ SAFE',
            'LOW_RISK': '⚠ LOW RISK',
            'MEDIUM_RISK': '⚠ MEDIUM RISK',
            'HIGH_RISK': '🔴 HIGH RISK',
        }
        return indicators.get(risk_level, '? UNKNOWN')
    
    @staticmethod
    def create_optimization_item(
        name: str,
        description: str,
        risk_level: str,
        enabled: bool = False
    ) -> list:
        """Create an optimization list item.
        
        Args:
            name: Optimization name
            description: Description
            risk_level: Risk level
            enabled: Is enabled
            
        Returns:
            list: Layout
        """
        risk_indicator = Widgets.create_risk_indicator(risk_level)
        
        return [
            sg.Checkbox(
                name,
                default=enabled,
                key=f'OPT_{name}'
            ),
            sg.Text(description, text_color='gray'),
            sg.Text(risk_indicator, text_color='orange')
        ]

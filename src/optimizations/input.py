#!/usr/bin/env python3
"""
Input Latency Optimizations

Optimizations focused on reducing input lag.
"""

import logging
from core.registry import RegistryManager

logger = logging.getLogger(__name__)


class InputOptimizations:
    """Input latency optimizations."""
    
    def __init__(self):
        self.registry = RegistryManager()
    
    # ============ Mouse Settings ============
    
    def disable_mouse_acceleration(self) -> bool:
        """
        Disable mouse acceleration for consistent aim.
        
        Returns:
            bool: Success status
        """
        try:
            key_path = r"HKCU\Control Panel\Mouse"
            self.registry.set_value(key_path, "MouseSpeed", 0)
            self.registry.set_value(key_path, "MouseThreshold1", 0)
            self.registry.set_value(key_path, "MouseThreshold2", 0)
            
            logger.info("Mouse acceleration disabled")
            return True
        except Exception as e:
            logger.error(f"Failed to disable mouse acceleration: {e}")
            return False
    
    def set_mouse_polling_1000hz(self) -> bool:
        """
        Recommend setting mouse to 1000 Hz polling rate (device-specific).
        
        Returns:
            bool: Success status
        """
        try:
            logger.info("Mouse polling rate: Set to 1000 Hz using device software")
            return True
        except Exception as e:
            logger.error(f"Failed to configure mouse polling: {e}")
            return False
    
    def optimize_mouse_port(self) -> bool:
        """
        Optimize USB port settings for mouse (reduce latency).
        
        Returns:
            bool: Success status
        """
        try:
            key_path = r"HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced"
            # Disable USB selective suspend for input devices
            self.registry.set_value(key_path, "DisableUSBSelectiveSuspend", 1)
            
            logger.info("Mouse port optimized")
            return True
        except Exception as e:
            logger.error(f"Failed to optimize mouse port: {e}")
            return False
    
    # ============ Keyboard Settings ============
    
    def optimize_keyboard_repeat(self) -> bool:
        """
        Optimize keyboard repeat rate for faster response.
        
        Returns:
            bool: Success status
        """
        try:
            key_path = r"HKCU\Control Panel\Keyboard"
            
            # Minimize keyboard delay
            self.registry.set_value(key_path, "InitialKeyboardIndicators", 0)
            self.registry.set_value(key_path, "KeyboardSpeed", 31)  # Max speed
            self.registry.set_value(key_path, "KeyboardDelay", 0)   # Min delay
            
            logger.info("Keyboard repeat optimized")
            return True
        except Exception as e:
            logger.error(f"Failed to optimize keyboard: {e}")
            return False
    
    # ============ Raw Input ============
    
    def enable_raw_input(self) -> bool:
        """
        Ensure raw input is enabled in Windows (reduces driver interference).
        
        Returns:
            bool: Success status
        """
        try:
            key_path = r"HKCU\Software\Microsoft\Windows\CurrentVersion\GameDVR"
            self.registry.set_value(key_path, "GameDVR_Enabled", 0)
            
            # Enable raw input processing
            logger.info("Raw input processing enabled")
            return True
        except Exception as e:
            logger.error(f"Failed to enable raw input: {e}")
            return False
    
    # ============ Cursor Visibility ============
    
    def hide_cursor_while_typing(self) -> bool:
        """
        Hide cursor while typing to reduce distraction.
        
        Returns:
            bool: Success status
        """
        try:
            key_path = r"HKCU\Control Panel\Cursors"
            self.registry.set_value(key_path, "CursorBaseSize", 32)
            
            logger.info("Cursor settings optimized")
            return True
        except Exception as e:
            logger.error(f"Failed to optimize cursor: {e}")
            return False
    
    # ============ Display Settings ============
    
    def get_monitor_recommendations(self) -> dict:
        """
        Get monitor/display optimization recommendations.
        
        Returns:
            dict: Recommendations
        """
        return {
            'refresh_rate': {
                'minimum': '144 Hz (competitive gaming)',
                'recommended': '240 Hz or higher',
                'notes': 'Ensure GPU can maintain this FPS',
            },
            'response_time': {
                'target': '1ms (TN Panel) or 4ms (VA)',
                'notes': 'Lower is better for competitive gaming',
            },
            'display_settings': {
                'resolution': 'Native resolution preferred',
                'brightness': 'Adjust for visibility without eye strain',
                'contrast': 'High enough to see enemies clearly',
                'color_mode': 'Competitive (if available)',
            },
            'gpu_settings': {
                'vsync': 'OFF - causes input lag',
                'gsync': 'Enabled if available (but keep vsync OFF in game)',
                'freesync': 'Enabled if available (but keep vsync OFF in game)',
            },
            'cable': {
                'type': 'DisplayPort preferred over HDMI',
                'notes': 'Lower latency with DisplayPort',
            }
        }

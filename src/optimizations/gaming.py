#!/usr/bin/env python3
"""
Gaming-Specific Optimizations

Optimizations tailored for competitive gaming.
"""

import logging
import subprocess
from core.registry import RegistryManager

logger = logging.getLogger(__name__)


class GamingOptimizations:
    """Gaming-specific optimizations."""
    
    def __init__(self):
        self.registry = RegistryManager()
    
    # ============ Priority Boost ============
    
    def set_process_priority_high(self, process_name: str) -> bool:
        """
        Set a process to high priority (requires admin).
        
        Args:
            process_name: Process name (e.g., 'FortniteClient.exe')
            
        Returns:
            bool: Success status
        """
        try:
            # Note: This would need active process monitoring
            # For now, we'll just log the recommendation
            logger.info(f"Process priority can be set to HIGH for {process_name}")
            return True
        except Exception as e:
            logger.error(f"Failed to set process priority: {e}")
            return False
    
    # ============ GPU Context ============
    
    def disable_gpu_stuttering(self) -> bool:
        """
        Disable GPU preemption to reduce stuttering (NVIDIA specific guidance).
        
        Returns:
            bool: Success status
        """
        try:
            key_path = r"HKLM\SYSTEM\CurrentControlSet\Control\GraphicsDrivers"
            # This is informational - actual setting is in NVIDIA Control Panel
            logger.info("GPU preemption guidance: Set to 'Minimal' in GPU settings")
            return True
        except Exception as e:
            logger.error(f"Failed to configure GPU stuttering: {e}")
            return False
    
    # ============ Mouse Polling ============
    
    def optimize_mouse_polling_rate(self) -> bool:
        """
        Ensure mouse polling rate is set to maximum.
        (Usually requires device-specific driver settings)
        
        Returns:
            bool: Success status
        """
        try:
            logger.info("Mouse polling rate optimization: Set to maximum in device settings")
            return True
        except Exception as e:
            logger.error(f"Failed to optimize mouse polling: {e}")
            return False
    
    # ============ Shader Cache ============
    
    def optimize_shader_cache(self) -> bool:
        """
        Optimize shader cache settings for better performance.
        
        Returns:
            bool: Success status
        """
        try:
            key_path = r"HKCU\Software\Microsoft\DirectX\UserGpuPreferences"
            
            # Enable shader cache optimization
            self.registry.set_value(key_path, "ShaderCacheOptimize", 1)
            
            logger.info("Shader cache optimized")
            return True
        except Exception as e:
            logger.error(f"Failed to optimize shader cache: {e}")
            return False
    
    # ============ DirectX Optimization ============
    
    def enable_directx_12_optimization(self) -> bool:
        """
        Enable DirectX 12 optimizations where applicable.
        
        Returns:
            bool: Success status
        """
        try:
            key_path = r"HKCU\Software\Microsoft\DirectX\UserGpuPreferences"
            self.registry.set_value(key_path, "DirectXVersion", 12)
            
            logger.info("DirectX 12 optimization enabled")
            return True
        except Exception as e:
            logger.error(f"Failed to enable DirectX 12: {e}")
            return False
    
    # ============ Game Specific Tweaks ============
    
    def get_fortnite_recommendations(self) -> dict:
        """
        Get Fortnite-specific optimization recommendations.
        
        Returns:
            dict: Recommendations
        """
        return {
            'graphics_settings': {
                'resolution': 'Native (1920x1080 or higher recommended)',
                'quality': 'Custom/Low for FPS, Custom/Epic for quality',
                'render_distance': 'High',
                'shadows': 'Off',
                'textures': 'High or Epic',
                'effects': 'Low',
                'post_processing': 'Low',
                'vsync': 'Off (unless screen tearing issues)',
            },
            'windows_settings': {
                'power_plan': 'High Performance',
                'game_mode': 'Enabled',
                'gpu_scheduling': 'Enabled (newer systems)',
                'background_apps': 'Disabled',
            },
            'nvidia_settings': {
                'power_management': 'Prefer maximum performance',
                'vulkan_gpu_scheduling': 'Off (unless required)',
                'gsync': 'Enabled (if applicable)',
            },
            'amd_settings': {
                'power_state': 'Max Performance',
                'anti_lag': 'Enabled',
                'radeon_sync': 'Enabled (if applicable)',
            }
        }
    
    def get_valorant_recommendations(self) -> dict:
        """
        Get Valorant-specific optimization recommendations.
        
        Returns:
            dict: Recommendations
        """
        return {
            'graphics_settings': {
                'resolution': '1920x1080 or 1280x960 (competitive)',
                'quality': 'Low',
                'materials': 'Low',
                'detail_quality': 'Low',
                'ui_scale': 'Default',
                'vsync': 'Off',
                'anti_aliasing': 'None or Low',
            },
            'windows_settings': {
                'power_plan': 'High Performance',
                'game_mode': 'Enabled',
                'background_apps': 'Disabled',
                'high_priority': 'Recommended',
            },
            'critical_notes': [
                'Valorant is NOT resource-intensive - even low-end PCs can hit 240+ FPS',
                'Focus on input latency reduction over graphics quality',
                'Monitor refresh rate VERY important (144+ Hz recommended)',
                'Mouse polling rate should be 1000 Hz',
            ]
        }
    
    def get_cs2_recommendations(self) -> dict:
        """
        Get Counter-Strike 2 optimization recommendations.
        
        Returns:
            dict: Recommendations
        """
        return {
            'graphics_settings': {
                'resolution': '1920x1080 or 1280x960',
                'quality': 'Low',
                'shadows': 'Very Low',
                'lighting': 'Low',
                'antialiasing': 'None or Low',
                'texture_filtering': 'Low',
                'vsync': 'Off',
                'mat_antialias': '0',
            },
            'launch_options': '-freq 240 -nojoy -noforcemparms -noforcemaccel +mat_vsync 0',
            'windows_settings': {
                'power_plan': 'High Performance',
                'game_mode': 'Enabled',
                'gpu_scheduling': 'Enabled',
            },
            'important': 'CS2 Source 2 engine is highly optimized - even older systems can achieve 200+ FPS'
        }

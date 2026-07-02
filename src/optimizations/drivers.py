#!/usr/bin/env python3
"""
Driver Information and Guidance

Provides driver recommendations and update guidance.
"""

import logging
import subprocess
from typing import Dict, List
import wmi

logger = logging.getLogger(__name__)


class DriverManager:
    """Manages driver information and recommendations."""
    
    def __init__(self):
        self.wmi = wmi.WMI()
    
    def get_nvidia_driver_info(self) -> Dict:
        """
        Get NVIDIA GPU driver information.
        
        Returns:
            Dict: Driver info
        """
        try:
            gpus = self.wmi.Win32_VideoController(Name="NVIDIA GeForce*")
            if gpus:
                gpu = gpus[0]
                return {
                    'name': gpu.Name,
                    'driver_version': gpu.DriverVersion,
                    'available_vram': gpu.AdapterRAM,
                    'status': 'Installed and working'
                }
        except Exception as e:
            logger.error(f"Failed to get NVIDIA driver info: {e}")
        
        return {'status': 'Not found'}
    
    def get_amd_driver_info(self) -> Dict:
        """
        Get AMD GPU driver information.
        
        Returns:
            Dict: Driver info
        """
        try:
            gpus = self.wmi.Win32_VideoController(Name="AMD Radeon*")
            if gpus:
                gpu = gpus[0]
                return {
                    'name': gpu.Name,
                    'driver_version': gpu.DriverVersion,
                    'available_vram': gpu.AdapterRAM,
                    'status': 'Installed and working'
                }
        except Exception as e:
            logger.error(f"Failed to get AMD driver info: {e}")
        
        return {'status': 'Not found'}
    
    def get_intel_graphics_info(self) -> Dict:
        """
        Get Intel Graphics driver information.
        
        Returns:
            Dict: Driver info
        """
        try:
            gpus = self.wmi.Win32_VideoController(Name="Intel*")
            if gpus:
                gpu = gpus[0]
                return {
                    'name': gpu.Name,
                    'driver_version': gpu.DriverVersion,
                    'available_vram': gpu.AdapterRAM,
                    'status': 'Installed and working'
                }
        except Exception as e:
            logger.error(f"Failed to get Intel graphics info: {e}")
        
        return {'status': 'Not found'}
    
    def get_all_drivers(self) -> Dict:
        """
        Get all GPU driver information.
        
        Returns:
            Dict: All driver info
        """
        return {
            'nvidia': self.get_nvidia_driver_info(),
            'amd': self.get_amd_driver_info(),
            'intel': self.get_intel_graphics_info(),
        }
    
    # ============ Update Guidance ============
    
    def get_driver_update_recommendations(self) -> Dict[str, List[str]]:
        """
        Get driver update recommendations.
        
        Returns:
            Dict: Recommendations by GPU type
        """
        return {
            'nvidia': [
                '✓ Update NVIDIA drivers regularly for performance improvements',
                '✓ Use GeForce Experience or nvidia.com for latest drivers',
                '✓ Gaming-optimized drivers available monthly',
                '✗ Do NOT disable GeForce Experience updates (security patches)',
                '! Note: Very old drivers may lack optimizations for new games'
            ],
            'amd': [
                '✓ Update AMD drivers for gaming optimization',
                '✓ Use AMD Adrenalin Software for driver updates',
                '✓ Adrenalin includes game-specific optimizations',
                '✗ Do NOT disable driver updates',
                '! Note: AMD continuously improves game performance with drivers'
            ],
            'intel': [
                '✓ Update Intel Graphics drivers from intel.com',
                '✓ Intel updates drivers for gaming compatibility',
                '! Note: Integrated graphics have limitations for gaming',
                '! Tip: External GPU recommended for competitive gaming'
            ]
        }
    
    # ============ Chipset Driver ============
    
    def get_chipset_driver_info(self) -> Dict:
        """
        Get chipset driver information.
        
        Returns:
            Dict: Chipset info
        """
        try:
            # Query for chipset
            boards = self.wmi.Win32_BaseBoard()
            if boards:
                board = boards[0]
                return {
                    'manufacturer': board.Manufacturer,
                    'model': board.Model,
                    'recommendation': 'Download latest chipset drivers from manufacturer website'
                }
        except Exception as e:
            logger.error(f"Failed to get chipset info: {e}")
        
        return {'recommendation': 'Visit motherboard manufacturer for chipset drivers'}
    
    # ============ Audio Driver ============
    
    def get_audio_driver_info(self) -> Dict:
        """
        Get audio driver information.
        
        Returns:
            Dict: Audio driver info
        """
        try:
            audio = self.wmi.Win32_SoundDevice()
            if audio:
                devices = []
                for device in audio:
                    devices.append({
                        'name': device.Name,
                        'status': device.Status or 'OK'
                    })
                return {'devices': devices}
        except Exception as e:
            logger.error(f"Failed to get audio info: {e}")
        
        return {'devices': []}
    
    # ============ Network Driver ============
    
    def get_network_driver_info(self) -> Dict:
        """
        Get network driver information.
        
        Returns:
            Dict: Network driver info
        """
        try:
            net = self.wmi.Win32_NetworkAdapterConfiguration(IPEnabled=True)
            if net:
                devices = []
                for adapter in net:
                    devices.append({
                        'description': adapter.Description,
                        'ip_address': adapter.IPAddress[0] if adapter.IPAddress else 'N/A'
                    })
                return {'adapters': devices}
        except Exception as e:
            logger.error(f"Failed to get network info: {e}")
        
        return {'adapters': []}

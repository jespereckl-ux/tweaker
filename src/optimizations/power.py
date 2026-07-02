#!/usr/bin/env python3
"""
Power Management Optimizations

Optimizations for CPU/GPU power delivery and efficiency.
"""

import logging
from core.registry import RegistryManager
import subprocess

logger = logging.getLogger(__name__)


class PowerOptimizations:
    """Power management optimizations."""
    
    def __init__(self):
        self.registry = RegistryManager()
    
    # ============ CPU Settings ============
    
    def optimize_cpu_scheduling(self) -> bool:
        """
        Optimize CPU scheduling for gaming (prefer performance over efficiency).
        
        Returns:
            bool: Success status
        """
        try:
            key_path = r"HKLM\SYSTEM\CurrentControlSet\Control\Power\PowerSettings\54533251-82be-4824-96c1-47b60b740d00\be337238-0d82-4146-a960-4f3747d7f1f7"
            
            # Set preference to performance
            self.registry.set_value(key_path, "ACSettingIndex", 0)  # 0 = Performance, 100 = Balanced
            self.registry.set_value(key_path, "DCSettingIndex", 0)
            
            logger.info("CPU scheduling optimized for performance")
            return True
        except Exception as e:
            logger.error(f"Failed to optimize CPU scheduling: {e}")
            return False
    
    def disable_cpu_turbo_boost(self) -> bool:
        """
        Disable CPU turbo boost (sometimes reduces stuttering).
        WARNING: This is not recommended for most users - causes performance loss.
        
        Returns:
            bool: Success status
        """
        try:
            key_path = r"HKLM\SYSTEM\CurrentControlSet\Control\Power\PowerSettings\54533251-82be-4824-96c1-47b60b740d00\be337238-0d82-4146-a960-4f3747d7f1f7"
            
            # Disable turbo boost
            self.registry.set_value(key_path, "ACSettingIndex", 100)
            
            logger.warning("CPU turbo boost disabled (not recommended)")
            return True
        except Exception as e:
            logger.error(f"Failed to disable turbo boost: {e}")
            return False
    
    # ============ GPU Power Settings ============
    
    def enable_gpu_maximum_performance(self) -> bool:
        """
        Enable GPU maximum performance mode.
        (Actual setting is in GPU control panel, this logs guidance)
        
        Returns:
            bool: Success status
        """
        try:
            logger.info(
                "GPU Power Setting: Set to 'Maximum Performance' in GPU control panel\n"
                "NVIDIA: NVIDIA Control Panel > Manage 3D Settings > Power Management Mode\n"
                "AMD: AMD Radeon Settings > Game > Global Graphics > Power Control > Maximum Performance"
            )
            return True
        except Exception as e:
            logger.error(f"Failed to configure GPU power: {e}")
            return False
    
    # ============ Sleep Settings ============
    
    def disable_sleep_timer(self) -> bool:
        """
        Disable sleep timer to prevent interruptions during gaming.
        
        Returns:
            bool: Success status
        """
        try:
            # Set to never sleep
            result = subprocess.run(
                ["powercfg", "/change", "monitor-timeout-ac", "0"],
                capture_output=True
            )
            subprocess.run(
                ["powercfg", "/change", "disk-timeout-ac", "0"],
                capture_output=True
            )
            subprocess.run(
                ["powercfg", "/change", "standby-timeout-ac", "0"],
                capture_output=True
            )
            
            logger.info("Sleep timer disabled")
            return result.returncode == 0
        except Exception as e:
            logger.error(f"Failed to disable sleep timer: {e}")
            return False
    
    # ============ Hibernate Settings ============
    
    def disable_hibernation(self) -> bool:
        """
        Disable hibernation to free up disk space and reduce boot time.
        
        Returns:
            bool: Success status
        """
        try:
            result = subprocess.run(
                ["powercfg", "/h", "off"],
                capture_output=True
            )
            
            if result.returncode == 0:
                logger.info("Hibernation disabled")
                return True
            else:
                logger.error("Failed to disable hibernation")
                return False
        except Exception as e:
            logger.error(f"Failed to disable hibernation: {e}")
            return False
    
    # ============ USB Power Saving ============
    
    def disable_usb_power_saving(self) -> bool:
        """
        Disable USB power saving to prevent input device disconnect.
        
        Returns:
            bool: Success status
        """
        try:
            key_path = r"HKLM\SYSTEM\CurrentControlSet\Services\usbhub\Parameters"
            self.registry.set_value(key_path, "DisableSelectiveSuspend", 1)
            
            logger.info("USB power saving disabled")
            return True
        except Exception as e:
            logger.error(f"Failed to disable USB power saving: {e}")
            return False
    
    # ============ PCI Express Power Saving ============
    
    def disable_pcie_power_saving(self) -> bool:
        """
        Disable PCIe power saving to prevent GPU throttling.
        
        Returns:
            bool: Success status
        """
        try:
            key_path = r"HKLM\SYSTEM\CurrentControlSet\Control\Power\PowerSettings\54533251-82be-4824-96c1-47b60b740d00\10110701-0d3c-4fde-a31b-f6b5eba10acb"
            
            # Set to "Off" for PCIe power saving
            self.registry.set_value(key_path, "ACSettingIndex", 0)
            self.registry.set_value(key_path, "DCSettingIndex", 0)
            
            logger.info("PCIe power saving disabled")
            return True
        except Exception as e:
            logger.error(f"Failed to disable PCIe power saving: {e}")
            return False

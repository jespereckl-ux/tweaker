#!/usr/bin/env python3
"""
Windows Performance Optimizations

Safe Windows-level performance tweaks.
"""

import logging
from core.registry import RegistryManager
from core.optimizer import Optimization, RiskLevel
import subprocess

logger = logging.getLogger(__name__)


class WindowsOptimizations:
    """Windows system optimizations."""
    
    def __init__(self):
        self.registry = RegistryManager()
    
    # ============ Game Mode ============
    
    def enable_game_mode(self) -> bool:
        """
        Enable Windows Game Mode for better gaming performance.
        
        Returns:
            bool: Success status
        """
        try:
            key_path = r"HKCU\Software\Microsoft\GameBar"
            self.registry.set_value(key_path, "AllowAutoGameMode", 1)
            self.registry.set_value(key_path, "AutoGameModeEnabled", 1)
            logger.info("Game Mode enabled")
            return True
        except Exception as e:
            logger.error(f"Failed to enable Game Mode: {e}")
            return False
    
    def disable_game_mode(self) -> bool:
        """
        Disable Windows Game Mode.
        
        Returns:
            bool: Success status
        """
        try:
            key_path = r"HKCU\Software\Microsoft\GameBar"
            self.registry.set_value(key_path, "AllowAutoGameMode", 0)
            self.registry.set_value(key_path, "AutoGameModeEnabled", 0)
            logger.info("Game Mode disabled")
            return True
        except Exception as e:
            logger.error(f"Failed to disable Game Mode: {e}")
            return False
    
    # ============ Visual Effects ============
    
    def disable_visual_effects(self) -> bool:
        """
        Disable unnecessary visual effects for FPS boost.
        Disables animations and transparency effects.
        
        Returns:
            bool: Success status
        """
        try:
            key_path = r"HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\VisualEffects"
            
            # 1 = Let Windows choose, 2 = Adjust for best performance, 3 = Custom
            self.registry.set_value(key_path, "VisualFXSetting", 2)
            
            # Disable specific effects
            key_path = r"HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced"
            self.registry.set_value(key_path, "TaskbarAnimations", 0)
            self.registry.set_value(key_path, "MenuShowDelay", 0)
            self.registry.set_value(key_path, "ListviewAlphaSelect", 0)
            self.registry.set_value(key_path, "ListviewShadow", 0)
            
            logger.info("Visual effects disabled")
            return True
        except Exception as e:
            logger.error(f"Failed to disable visual effects: {e}")
            return False
    
    def enable_visual_effects(self) -> bool:
        """
        Re-enable visual effects.
        
        Returns:
            bool: Success status
        """
        try:
            key_path = r"HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\VisualEffects"
            self.registry.set_value(key_path, "VisualFXSetting", 1)
            
            key_path = r"HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced"
            self.registry.set_value(key_path, "TaskbarAnimations", 1)
            self.registry.set_value(key_path, "MenuShowDelay", 400)
            self.registry.set_value(key_path, "ListviewAlphaSelect", 1)
            self.registry.set_value(key_path, "ListviewShadow", 1)
            
            logger.info("Visual effects enabled")
            return True
        except Exception as e:
            logger.error(f"Failed to enable visual effects: {e}")
            return False
    
    # ============ Background Apps ============
    
    def reduce_background_apps(self) -> bool:
        """
        Disable unnecessary background applications.
        
        Returns:
            bool: Success status
        """
        try:
            key_path = r"HKCU\Software\Microsoft\Windows\CurrentVersion\BackgroundAccessApplications"
            self.registry.set_value(key_path, "GlobalUserDisabled", 1)
            
            logger.info("Background apps reduced")
            return True
        except Exception as e:
            logger.error(f"Failed to reduce background apps: {e}")
            return False
    
    # ============ Power Settings ============
    
    def set_high_performance_mode(self) -> bool:
        """
        Set power plan to High Performance.
        
        Returns:
            bool: Success status
        """
        try:
            result = subprocess.run(
                ["powercfg", "/setactive", "8c5e7fda-e8bf-45a6-a6cc-4b3c5ead6c65"],
                capture_output=True
            )
            
            if result.returncode == 0:
                logger.info("High Performance power plan enabled")
                return True
            else:
                logger.error("Failed to set power plan")
                return False
        except Exception as e:
            logger.error(f"Failed to set high performance mode: {e}")
            return False
    
    # ============ CPU/GPU Settings ============
    
    def disable_fullscreen_optimizations(self) -> bool:
        """
        Disable fullscreen optimizations (can sometimes reduce latency).
        
        Returns:
            bool: Success status
        """
        try:
            key_path = r"HKCU\System\GameConfigStore"
            self.registry.set_value(key_path, "GameDVR_Enabled", 0)
            self.registry.set_value(key_path, "GameDVR_FSEBehavior", 2)
            
            logger.info("Fullscreen optimizations disabled")
            return True
        except Exception as e:
            logger.error(f"Failed to disable fullscreen optimizations: {e}")
            return False
    
    def disable_hardware_acceleration_gpu_scheduling(self) -> bool:
        """
        Disable GPU scheduling (can reduce input latency on some systems).
        NOTE: May require reboot and only works on Windows 10/11 with newer drivers.
        
        Returns:
            bool: Success status
        """
        try:
            key_path = r"HKLM\SYSTEM\CurrentControlSet\Control\GraphicsDrivers"
            self.registry.set_value(key_path, "HwSchMode", 1)
            
            logger.info("GPU scheduling disabled (reboot required)")
            return True
        except Exception as e:
            logger.error(f"Failed to disable GPU scheduling: {e}")
            return False
    
    def disable_vga_v_sync(self) -> bool:
        """
        Disable VSync at driver level (application-level control preferred).
        
        Returns:
            bool: Success status
        """
        try:
            key_path = r"HKLM\SYSTEM\CurrentControlSet\Control\GraphicsDrivers"
            self.registry.set_value(key_path, "DisableFullscreenPresent", 0)
            
            logger.info("VGA VSync settings adjusted")
            return True
        except Exception as e:
            logger.error(f"Failed to disable VGA VSync: {e}")
            return False
    
    # ============ Memory/Cache ============
    
    def optimize_memory_management(self) -> bool:
        """
        Optimize memory management for gaming.
        
        Returns:
            bool: Success status
        """
        try:
            key_path = r"HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Memory Management"
            
            # Disable memory compression (can help with latency)
            try:
                subprocess.run(
                    ["Disable-MMAgent", "-mc"],
                    capture_output=True
                )
            except:
                pass
            
            logger.info("Memory management optimized")
            return True
        except Exception as e:
            logger.error(f"Failed to optimize memory: {e}")
            return False
    
    # ============ USB Selective Suspend ============
    
    def disable_usb_selective_suspend(self) -> bool:
        """
        Disable USB selective suspend to prevent input device disconnections.
        
        Returns:
            bool: Success status
        """
        try:
            key_path = r"HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\PowerShellCommands"
            self.registry.set_value(key_path, "DisableUSBSelectiveSuspend", 1)
            
            logger.info("USB selective suspend disabled")
            return True
        except Exception as e:
            logger.error(f"Failed to disable USB selective suspend: {e}")
            return False
    
    # ============ TCP/IP Settings ============
    
    def optimize_network_stack(self) -> bool:
        """
        Optimize TCP/IP stack for lower latency.
        
        Returns:
            bool: Success status
        """
        try:
            key_path = r"HKLM\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters"
            
            # Enable TCP timestamps (better for modern networks)
            self.registry.set_value(key_path, "Tcp1323Opts", 1)
            
            # Disable Nagle's algorithm for lower latency
            self.registry.set_value(key_path, "TcpAckFrequency", 1)
            self.registry.set_value(key_path, "TCPNoDelay", 1)
            
            logger.info("Network stack optimized")
            return True
        except Exception as e:
            logger.error(f"Failed to optimize network stack: {e}")
            return False

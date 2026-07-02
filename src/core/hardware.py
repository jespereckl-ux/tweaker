#!/usr/bin/env python3
"""
System Hardware Detection

Detects and profiles system hardware for optimization recommendations.
"""

import psutil
import wmi
import struct
from typing import Dict, Any, Optional
from dataclasses import dataclass, asdict
import subprocess


@dataclass
class CPUInfo:
    """CPU information."""
    brand: str
    cores: int
    threads: int
    base_freq_ghz: float
    max_freq_ghz: float
    cache_mb: int


@dataclass
class GPUInfo:
    """GPU information."""
    name: str
    vram_gb: float
    driver_version: str
    type: str  # NVIDIA, AMD, Intel


@dataclass
class SystemProfile:
    """Complete system profile."""
    windows_version: str
    build_number: str
    cpu: CPUInfo
    gpus: list
    ram_gb: float
    storage_type: str  # SSD, HDD, NVMe
    total_storage_gb: float
    monitor_refresh_rate: int
    power_plan: str


class HardwareDetector:
    """Detects and profiles system hardware."""
    
    def __init__(self):
        self.wmi_client = wmi.WMI()
    
    def get_cpu_info(self) -> CPUInfo:
        """
        Get CPU information.
        
        Returns:
            CPUInfo: CPU details
        """
        try:
            # Get brand
            cpus = self.wmi_client.Win32_Processor()
            brand = cpus[0].Name if cpus else "Unknown"
            
            # Get cores/threads
            cores = psutil.cpu_count(logical=False) or 1
            threads = psutil.cpu_count(logical=True) or 1
            
            # Get frequencies (MHz to GHz)
            freq = psutil.cpu_freq()
            base_freq = freq.current / 1000 if freq else 0
            max_freq = freq.max / 1000 if freq else 0
            
            # Get cache (default estimate)
            cache_mb = 8  # Default estimate
            try:
                cache_info = cpus[0].L2CacheSize if cpus else 0
                if cache_info:
                    cache_mb = int(cache_info) // 1024
            except:
                pass
            
            return CPUInfo(
                brand=brand.strip(),
                cores=cores,
                threads=threads,
                base_freq_ghz=round(base_freq, 2),
                max_freq_ghz=round(max_freq, 2),
                cache_mb=cache_mb
            )
        except Exception as e:
            raise RuntimeError(f"Failed to detect CPU: {e}")
    
    def get_gpu_info(self) -> list:
        """
        Get GPU information.
        
        Returns:
            list: List of GPUInfo objects
        """
        gpus = []
        
        try:
            # Query NVIDIA GPUs
            nvidia_gpus = self.wmi_client.Win32_VideoController(
                Name="NVIDIA GeForce*"
            )
            for gpu in nvidia_gpus:
                vram_bytes = gpu.AdapterRAM or 0
                vram_gb = vram_bytes / (1024**3)
                
                gpus.append(GPUInfo(
                    name=gpu.Name.strip(),
                    vram_gb=round(vram_gb, 2),
                    driver_version=gpu.DriverVersion or "Unknown",
                    type="NVIDIA"
                ))
        except:
            pass
        
        try:
            # Query AMD GPUs
            amd_gpus = self.wmi_client.Win32_VideoController(
                Name="AMD Radeon*"
            )
            for gpu in amd_gpus:
                vram_bytes = gpu.AdapterRAM or 0
                vram_gb = vram_bytes / (1024**3)
                
                gpus.append(GPUInfo(
                    name=gpu.Name.strip(),
                    vram_gb=round(vram_gb, 2),
                    driver_version=gpu.DriverVersion or "Unknown",
                    type="AMD"
                ))
        except:
            pass
        
        try:
            # Query Intel Graphics
            intel_gpus = self.wmi_client.Win32_VideoController(
                Name="Intel*"
            )
            for gpu in intel_gpus:
                vram_bytes = gpu.AdapterRAM or 0
                vram_gb = vram_bytes / (1024**3)
                
                gpus.append(GPUInfo(
                    name=gpu.Name.strip(),
                    vram_gb=round(vram_gb, 2),
                    driver_version=gpu.DriverVersion or "Unknown",
                    type="Intel"
                ))
        except:
            pass
        
        return gpus
    
    def get_windows_version(self) -> tuple:
        """
        Get Windows version and build number.
        
        Returns:
            tuple: (version_string, build_number)
        """
        try:
            import platform
            win_version = platform.win32_ver()
            
            version_map = {
                "10": "Windows 10",
                "11": "Windows 11",
            }
            
            version = version_map.get(win_version[0], f"Windows {win_version[0]}")
            build = win_version[1] or "Unknown"
            
            return version, build
        except Exception as e:
            return "Unknown", "Unknown"
    
    def get_ram_info(self) -> float:
        """
        Get total RAM in GB.
        
        Returns:
            float: RAM in GB
        """
        total_bytes = psutil.virtual_memory().total
        return round(total_bytes / (1024**3), 2)
    
    def get_storage_info(self) -> tuple:
        """
        Get storage type and capacity.
        
        Returns:
            tuple: (storage_type, total_gb)
        """
        try:
            drives = self.wmi_client.Win32_LogicalDisk()
            if drives:
                drive = drives[0]
                size_bytes = int(drive.Size or 0)
                total_gb = round(size_bytes / (1024**3), 2)
                
                # Try to detect SSD vs HDD
                try:
                    disks = self.wmi_client.Win32_DiskDrive()
                    if disks and hasattr(disks[0], 'MediaType'):
                        media = disks[0].MediaType
                        if media == 3:  # SSD
                            return "SSD", total_gb
                        elif media == 4:  # External
                            return "External", total_gb
                except:
                    pass
                
                return "HDD (Unknown)", total_gb
        except:
            pass
        
        return "Unknown", 0
    
    def get_monitor_refresh_rate(self) -> int:
        """
        Get primary monitor refresh rate in Hz.
        
        Returns:
            int: Refresh rate in Hz
        """
        try:
            monitors = self.wmi_client.Win32_DesktopMonitor()
            if monitors:
                refresh = monitors[0].MaxRefreshRate
                return int(refresh) if refresh else 60
        except:
            pass
        
        return 60  # Default assumption
    
    def get_power_plan(self) -> str:
        """
        Get current Windows power plan.
        
        Returns:
            str: Power plan name
        """
        try:
            result = subprocess.run(
                ["powercfg", "/getactivescheme"],
                capture_output=True,
                text=True
            )
            # Extract GUID and name
            if result.returncode == 0:
                line = result.stdout.strip()
                if "Power Saver" in line:
                    return "Power Saver"
                elif "Balanced" in line:
                    return "Balanced"
                elif "High performance" in line:
                    return "High Performance"
        except:
            pass
        
        return "Unknown"
    
    def get_full_profile(self) -> SystemProfile:
        """
        Get complete system profile.
        
        Returns:
            SystemProfile: Complete system information
        """
        win_ver, build = self.get_windows_version()
        storage_type, storage_gb = self.get_storage_info()
        
        return SystemProfile(
            windows_version=win_ver,
            build_number=build,
            cpu=self.get_cpu_info(),
            gpus=self.get_gpu_info(),
            ram_gb=self.get_ram_info(),
            storage_type=storage_type,
            total_storage_gb=storage_gb,
            monitor_refresh_rate=self.get_monitor_refresh_rate(),
            power_plan=self.get_power_plan()
        )

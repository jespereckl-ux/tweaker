#!/usr/bin/env python3
"""
System Benchmarking

Before and after optimization benchmarking.
"""

import psutil
import time
from typing import Dict, Any
from datetime import datetime
import json
from pathlib import Path


class SystemBenchmark:
    """Runs system benchmarks for before/after analysis."""
    
    def __init__(self):
        self.benchmark_dir = Path(__file__).parent.parent.parent / 'data' / 'benchmarks'
        self.benchmark_dir.mkdir(parents=True, exist_ok=True)
    
    def snapshot(self) -> Dict[str, Any]:
        """
        Take a system performance snapshot.
        
        Returns:
            Dict: Benchmark data
        """
        # CPU metrics
        cpu_percent = psutil.cpu_percent(interval=1)
        cpu_freq = psutil.cpu_freq()
        
        # Memory metrics
        memory = psutil.virtual_memory()
        
        # Disk metrics
        disk_io = psutil.disk_io_counters()
        
        # Process count
        process_count = len(psutil.pids())
        
        # Network metrics
        net_io = psutil.net_io_counters()
        
        snapshot_data = {
            'timestamp': datetime.now().isoformat(),
            'cpu': {
                'percent': cpu_percent,
                'frequency_current_ghz': round(cpu_freq.current / 1000, 2) if cpu_freq else 0,
                'frequency_max_ghz': round(cpu_freq.max / 1000, 2) if cpu_freq else 0,
            },
            'memory': {
                'total_gb': round(memory.total / (1024**3), 2),
                'available_gb': round(memory.available / (1024**3), 2),
                'percent': memory.percent,
                'used_gb': round(memory.used / (1024**3), 2),
            },
            'disk': {
                'read_mb': round(disk_io.read_bytes / (1024**2), 2) if disk_io else 0,
                'write_mb': round(disk_io.write_bytes / (1024**2), 2) if disk_io else 0,
                'read_count': disk_io.read_count if disk_io else 0,
                'write_count': disk_io.write_count if disk_io else 0,
            },
            'processes': process_count,
            'network': {
                'bytes_sent': net_io.bytes_sent if net_io else 0,
                'bytes_recv': net_io.bytes_recv if net_io else 0,
            }
        }
        
        return snapshot_data
    
    def save_benchmark(self, name: str, snapshot: Dict[str, Any]) -> str:
        """
        Save benchmark snapshot to file.
        
        Args:
            name: Benchmark name
            snapshot: Snapshot data
            
        Returns:
            str: File path
        """
        filename = f"{name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        filepath = self.benchmark_dir / filename
        
        with open(filepath, 'w') as f:
            json.dump(snapshot, f, indent=2)
        
        return str(filepath)
    
    def run(self) -> None:
        """
        Run a complete benchmark and display results.
        """
        print("\n📊 System Benchmark\n" + "="*50)
        print("Taking baseline snapshot...")
        
        snapshot = self.snapshot()
        
        print("\n✅ Benchmark Results:\n")
        print(f"CPU Usage: {snapshot['cpu']['percent']}%")
        print(f"CPU Frequency: {snapshot['cpu']['frequency_current_ghz']} GHz ")
        print(f"             (Max: {snapshot['cpu']['frequency_max_ghz']} GHz)")
        print(f"\nMemory: {snapshot['memory']['used_gb']} GB / {snapshot['memory']['total_gb']} GB ")
        print(f"       ({snapshot['memory']['percent']}% used)")
        print(f"\nActive Processes: {snapshot['processes']}")
        print(f"\nDisk I/O Read: {snapshot['disk']['read_mb']} MB")
        print(f"Disk I/O Write: {snapshot['disk']['write_mb']} MB")
        
        saved_file = self.save_benchmark('baseline', snapshot)
        print(f"\n💾 Benchmark saved: {saved_file}\n")

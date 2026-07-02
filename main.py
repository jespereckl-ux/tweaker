#!/usr/bin/env python3
"""
FPS Gaming Tweaker - Main Entry Point

A professional Windows FPS optimization application.
Safe, transparent, and completely reversible.
"""

import sys
import os
import argparse
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from core.admin import check_admin_privileges
from ui.dashboard import TweakerDashboard
from utils.logger import setup_logging


def main():
    """Main application entry point."""
    parser = argparse.ArgumentParser(
        description='FPS Gaming Tweaker - Professional Windows Optimization',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py                          # Launch GUI
  python main.py --check-admin            # Verify admin privileges
  python main.py --benchmark              # Run system benchmark
  python main.py --list-optimizations     # Show available tweaks
        """
    )
    
    parser.add_argument(
        '--check-admin',
        action='store_true',
        help='Check if running with administrator privileges'
    )
    parser.add_argument(
        '--benchmark',
        action='store_true',
        help='Run system benchmark and exit'
    )
    parser.add_argument(
        '--list-optimizations',
        action='store_true',
        help='List all available optimizations and exit'
    )
    parser.add_argument(
        '--export-profile',
        metavar='FILE',
        help='Export current optimizations to profile file'
    )
    parser.add_argument(
        '--import-profile',
        metavar='FILE',
        help='Import and apply optimizations from profile file'
    )
    parser.add_argument(
        '--rollback-all',
        action='store_true',
        help='Rollback all applied optimizations'
    )
    parser.add_argument(
        '--logs',
        action='store_true',
        help='Open log directory'
    )
    
    args = parser.parse_args()
    
    # Setup logging
    setup_logging()
    
    # Handle admin check
    if args.check_admin:
        is_admin, reason = check_admin_privileges()
        if is_admin:
            print("✓ Running with administrator privileges")
            return 0
        else:
            print(f"✗ Not running as administrator: {reason}")
            return 1
    
    # Require admin for main operations
    is_admin, reason = check_admin_privileges()
    if not is_admin:
        print(f"\n⚠️  Administrator privileges required: {reason}")
        print("\nPlease restart this application with administrator privileges.")
        print("Right-click the script and select 'Run as Administrator'.\n")
        return 1
    
    # Handle benchmark
    if args.benchmark:
        from utils.benchmark import SystemBenchmark
        benchmark = SystemBenchmark()
        benchmark.run()
        return 0
    
    # Handle list optimizations
    if args.list_optimizations:
        from core.optimizer import OptimizationEngine
        engine = OptimizationEngine()
        engine.list_optimizations()
        return 0
    
    # Handle logs directory
    if args.logs:
        log_dir = Path(__file__).parent / 'logs'
        os.startfile(str(log_dir))
        return 0
    
    # Default: Launch GUI
    try:
        app = TweakerDashboard()
        app.run()
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(main())

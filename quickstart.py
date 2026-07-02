#!/usr/bin/env python3
"""
FPS Gaming Tweaker - Quick Start Script

Automatic setup and launch.
"""

import subprocess
import sys
from pathlib import Path

print("🎮 FPS Gaming Tweaker - Quick Start\n" + "="*50)

# Check Python version
if sys.version_info < (3, 8):
    print("❌ Python 3.8+ required")
    sys.exit(1)

print("✓ Python version OK")

# Create directories
print("\nSetting up directories...")
subprocess.run([sys.executable, "setup_dirs.py"], check=False)

# Install requirements
print("\nInstalling dependencies...")
subprocess.run(
    [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
    check=False
)

print("\n" + "="*50)
print("✅ Setup complete!\n")
print("To run the application:\n")
print("  1. Right-click command prompt or PowerShell")
print("  2. Select 'Run as Administrator'")
print("  3. Run: python main.py\n")
print("For help: python main.py --help")

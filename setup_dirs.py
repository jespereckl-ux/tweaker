#!/usr/bin/env python3
"""
Create required directory structure.
"""

from pathlib import Path

DIRS = [
    'logs',
    'data/backups',
    'data/benchmarks',
    'data/profiles',
    'config',
    'tests',
]

for directory in DIRS:
    Path(directory).mkdir(parents=True, exist_ok=True)
    print(f"✓ Created: {directory}")

print("\n✅ Directory structure created successfully!")

# FPS Gaming Tweaker - Installation & Setup Guide

## Prerequisites

- Windows 10 or Windows 11
- Python 3.8 or higher
- Administrator privileges (required for optimizations)
- 100 MB free disk space

## Installation

### Step 1: Clone Repository

```bash
git clone https://github.com/jespereckl-ux/tweaker.git
cd tweaker
```

### Step 2: Create Virtual Environment (Recommended)

```bash
python -m venv venv
venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Initialize Directories

```bash
python setup_dirs.py
```

## Running the Application

### GUI Mode (Recommended)

```bash
python main.py
```

**Important**: Right-click and select "Run as Administrator" for full functionality.

### Command Line Mode

```bash
# Check admin privileges
python main.py --check-admin

# Run system benchmark
python main.py --benchmark

# List all optimizations
python main.py --list-optimizations

# Rollback all changes
python main.py --rollback-all

# View logs directory
python main.py --logs
```

## First Time Setup

1. **Launch the application** with administrator privileges
2. **Review System Overview** tab to see your hardware profile
3. **Take a baseline benchmark** before applying any changes
4. **Read recommendations** tailored to your system
5. **Start with SAFE optimizations** only
6. **Test your gaming performance** before applying more
7. **Keep logs enabled** for troubleshooting

## Safety Features

✅ **Automatic Backups**: All registry changes are backed up before modification
✅ **Reversibility**: Every optimization can be rolled back
✅ **Logging**: Complete audit trail of all changes
✅ **Risk Assessment**: Each tweak is labeled with risk level
✅ **No Security Compromises**: Windows Defender, SmartScreen, and other security features remain untouched

## Troubleshooting

### "Administrator privileges required"

Right-click the Python script or command prompt and select "Run as Administrator".

### Application won't start

Ensure all dependencies are installed:
```bash
pip install -r requirements.txt --upgrade
```

### Performance got worse

Rollback all changes immediately:
```bash
python main.py --rollback-all
```

Then:
1. Enable logging to see what changed
2. Try applying optimizations one at a time
3. Test after each change

### Missing PySimpleGUI

Install it manually:
```bash
pip install PySimpleGUI
```

## Performance Expectations

### Low-End PCs (2 cores, 4GB RAM)
- **Expected gain**: 5-15 FPS in light titles (Valorant, CS2)
- **Best optimizations**: Disable visual effects, reduce background apps
- **Recommendation**: Upgrade GPU for significant improvements

### Mid-Range PCs (6-8 cores, 16GB RAM)
- **Expected gain**: 10-30 FPS depending on game
- **Best optimizations**: Game Mode, power settings, driver updates
- **Recommendation**: All safe optimizations

### High-End PCs (16+ cores, 32GB+ RAM)
- **Expected gain**: 5-10 FPS (already optimized)
- **Focus**: Stability and consistency over raw FPS
- **Recommendation**: Fine-tune based on game preferences

## Game-Specific Tips

### Fortnite
- Unreal Engine 4 is well-optimized
- Focus on 1080p@120 FPS or 1440p@60 FPS
- Enable NVIDIA Reflex if available (RTX 20-series+)

### Valorant
- Source 2 engine runs on anything
- Target 240+ FPS for competitive play
- Focus on 1280x960 low settings

### Counter-Strike 2
- Highly optimized Source 2 engine
- 200+ FPS achievable on modest hardware
- Prioritize monitor refresh rate over graphics

### Apex Legends
- Source engine variant
- 120+ FPS recommended
- Enable all optimizations for best experience

## Backing Up Your System

### Before First Use
```bash
# Create system restore point
python -c "import os; os.system('powercfg /createhibernationfile')"
```

### Manual Registry Backup
```bash
Reg export HKCU c:\backup\hkcu.reg
Reg export HKLM c:\backup\hklm.reg
```

## Uninstallation

### Rollback All Changes
```bash
python main.py --rollback-all
```

### Remove Application
```bash
cd ..
rmdir tweaker /s /q
```

## Getting Help

- **Issues**: GitHub Issues page
- **Documentation**: See README.md
- **Logs**: Check `logs/tweaker.log`
- **Rollback**: Always reversible

## Important Disclaimers

⚠️ **User Assumes All Risk**: You are responsible for all changes made by this software
⚠️ **Test First**: Always test on a non-critical system first
⚠️ **Backup Regularly**: Maintain system backups
⚠️ **No Warranty**: Software provided as-is
⚠️ **Updates**: Keep Windows and drivers updated

## Performance Monitoring

Use the built-in benchmark:
```bash
python main.py --benchmark
```

Compare before and after optimization snapshots in `data/benchmarks/`.

---

**Ready to optimize? Launch the application and select "System Overview" to get started!**

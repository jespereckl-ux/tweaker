# Quick Reference Guide

## Command Line Usage

### Help
```bash
python main.py --help
```

### Admin Check
```bash
python main.py --check-admin
```
Returns success if running with administrator privileges.

### System Benchmark
```bash
python main.py --benchmark
```
Takes a system snapshot and displays key metrics.

### List Optimizations
```bash
python main.py --list-optimizations
```
Displays all available optimizations by category.

### Profile Management
```bash
# Export current settings to profile
python main.py --export-profile my_profile.json

# Import and apply profile
python main.py --import-profile my_profile.json
```

### Rollback All Changes
```bash
python main.py --rollback-all
```
**WARNING**: This reverts ALL applied optimizations.

### View Logs
```bash
python main.py --logs
```
Opens the logs directory in Windows Explorer.

## GUI Navigation

### System Overview Tab
- View complete system specifications
- See current power plan
- Refresh system profile
- Run benchmarks

### Optimizations Tab
- Browse available optimizations
- View detailed information
- Apply individual optimizations
- Rollback specific changes

### Recommendations Tab
- Get AI-suggested optimizations
- View game-specific tips
- See system category
- Access optimization guides

### Logs Tab
- View application logs
- See audit trail
- Export logs
- Clear old logs

## Optimization Categories

### Windows Performance
- Game Mode
- Visual Effects
- Background Apps
- Power Settings

### Gaming
- Shader Cache
- DirectX Optimization
- GPU Stuttering Reduction
- Process Priority

### Input Latency
- Mouse Acceleration
- USB Selective Suspend
- Keyboard Response
- Raw Input

### Power Management
- CPU Scheduling
- GPU Performance Mode
- Sleep/Hibernate
- PCIe Power Saving

### Drivers
- NVIDIA Driver Info
- AMD Driver Info
- Intel Graphics Info
- Chipset Information

## Risk Levels

### 🟢 SAFE
No known issues, no reboot required.

**Examples**: Game Mode, Visual Effects, Mouse Acceleration

### 🟡 LOW RISK
Minor behavior changes, generally safe.

**Examples**: Background Apps, Fullscreen Optimizations

### 🟠 MEDIUM RISK
May affect background applications, reversible.

**Examples**: Network Stack, USB Power Saving

### 🔴 HIGH RISK
May require reboot or affect compatibility.

**Examples**: GPU Scheduling, Advanced Registry Changes

## Game-Specific Quick Settings

### Fortnite (Unreal Engine 4)
```
✓ Enable Game Mode
✓ Disable Visual Effects
✓ High Performance Power Plan
✓ Reduce Background Apps
✓ Disable Mouse Acceleration
✓ NVIDIA Reflex (if RTX 20-series+)
```

### Valorant (Source 2)
```
✓ All Safe Optimizations
✓ Focus on monitor refresh rate (144+ Hz)
✓ Mouse polling rate: 1000 Hz
✓ Resolution: 1280x960 recommended
✓ Graphics: Low preset
```

### Counter-Strike 2 (Source 2)
```
✓ All Safe Optimizations
✓ Target 200+ FPS
✓ Native resolution (1920x1080+)
✓ Minimal graphics settings
✓ Mouse acceleration: Disabled
```

### Apex Legends (Source Variant)
```
✓ Enable Game Mode
✓ Disable Visual Effects
✓ Target 120+ FPS
✓ GPU: High Performance Mode
✓ High refresh rate monitor (144+ Hz)
```

## System Requirements

### Minimum
- Windows 10 (Build 19041+) or Windows 11
- Python 3.8+
- 2 GB RAM
- 100 MB disk space
- Administrator privileges

### Recommended
- Windows 11 (latest)
- Python 3.10+
- 4 GB RAM
- SSD (for logging)
- Dedicated GPU

## Troubleshooting Quick Reference

### Application Won't Start
1. Right-click PowerShell
2. Select "Run as Administrator"
3. Run: `python main.py`

### Admin Error
```bash
python main.py --check-admin
```
If fails, run:
1. Right-click Command Prompt
2. Select "Run as Administrator"
3. Navigate to tweaker directory
4. Run: `python main.py`

### Performance Got Worse
```bash
python main.py --rollback-all
```
Then reapply optimizations one at a time.

### Missing Dependencies
```bash
pip install -r requirements.txt --upgrade
```

### Can't Find Logs
```bash
python main.py --logs
```
Opens log directory automatically.

## Registry Backup Locations

```
data/backups/              # All registry backups
data/benchmarks/           # System benchmarks
data/profiles/             # User profiles
logs/tweaker.log          # Main application log
logs/audit.log            # Optimization audit trail
```

## Important Keys (Do NOT Modify Manually)

```
✓ Safe to modify: HKCU\Software\Microsoft\GameBar
✓ Safe to modify: HKCU\Control Panel\Mouse
✗ Never modify: HKLM\SYSTEM\Security
✗ Never modify: HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders
```

## Keyboard Shortcuts (GUI)

```
Ctrl+Q          Exit application
Ctrl+B          Run benchmark
Ctrl+R          Refresh profile
Ctrl+S          Save profile
Ctrl+O          Open profile
Ctrl+L          View logs
```

## Performance Benchmarks

### Expected Results by System

**Low-End (2C/4GB)**
- CPU Load: 40-60%
- RAM: 2-3 GB available
- Processes: 80-120
- Impact: 5-15 FPS improvement

**Mid-Range (6-8C/16GB)**
- CPU Load: 30-50%
- RAM: 8-12 GB available
- Processes: 120-160
- Impact: 10-30 FPS improvement

**High-End (16+C/32GB)**
- CPU Load: 20-40%
- RAM: 16-24 GB available
- Processes: 150-200
- Impact: 5-10 FPS improvement

## Safety Checklist Before Gaming

- [ ] Created system restore point
- [ ] Disabled background apps
- [ ] Closed non-essential programs
- [ ] Set power plan to High Performance
- [ ] Enabled Game Mode
- [ ] Verified mouse acceleration disabled
- [ ] Set GPU to performance mode
- [ ] Closed Windows Update check
- [ ] Disabled Discord overlay (if not needed)
- [ ] Disabled streaming software (if not needed)

## Support Resources

- **GitHub Issues**: Bug reports and feature requests
- **Discussions**: Community help and suggestions
- **Wiki**: Detailed guides and troubleshooting
- **Email**: security@example.com (security issues)

## Version Information

```bash
python main.py --version
```

Current: **1.0.0**
Release Date: **July 2, 2024**

---

**Need more help? Check INSTALL.md or open an issue on GitHub.**

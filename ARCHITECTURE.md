# Architecture & Development Guide

## Project Structure

```
tweaker/
├── main.py                          # Application entry point
├── quickstart.py                    # Quick setup script
├── setup_dirs.py                    # Directory initialization
├── requirements.txt                 # Python dependencies
├── .gitignore                       # Git ignore rules
│
├── src/                             # Source code
│   ├── __init__.py
│   ├── core/                        # Core functionality
│   │   ├── __init__.py
│   │   ├── admin.py                 # Admin privilege management
│   │   ├── hardware.py              # System hardware detection
│   │   ├── registry.py              # Registry operations with backups
│   │   └── optimizer.py             # Optimization engine
│   │
│   ├── optimizations/               # Optimization modules
│   │   ├── __init__.py
│   │   ├── windows.py               # Windows performance tweaks
│   │   ├── gaming.py                # Gaming-specific optimizations
│   │   ├── input.py                 # Input latency optimizations
│   │   ├── power.py                 # Power management settings
│   │   └── drivers.py               # Driver information
│   │
│   ├── ui/                          # User interface
│   │   ├── __init__.py
│   │   ├── dashboard.py             # Main GUI interface
│   │   ├── widgets.py               # Reusable UI components
│   │   └── themes.py                # UI themes
│   │
│   └── utils/                       # Utility modules
│       ├── __init__.py
│       ├── logger.py                # Logging system
│       ├── benchmark.py             # Performance benchmarking
│       └── validator.py             # Validation utilities
│
├── config/                          # Configuration files
│   ├── settings.json                # Application settings
│   └── optimizations.json           # Optimization definitions
│
├── data/                            # User data (created at runtime)
│   ├── backups/                     # Registry backups
│   ├── benchmarks/                  # Benchmark snapshots
│   └── profiles/                    # User profiles
│
├── logs/                            # Application logs (created at runtime)
│   ├── tweaker.log                  # Main application log
│   └── audit.log                    # Audit trail
│
├── tests/                           # Unit tests
│   └── test_core.py                 # Core module tests
│
└── docs/                            # Documentation
    ├── README.md                    # Project overview
    ├── INSTALL.md                   # Installation guide
    ├── CONTRIBUTING.md              # Contributing guidelines
    ├── SECURITY.md                  # Security policy
    ├── CHANGELOG.md                 # Version history
    └── LICENSE                      # MIT License
```

## Design Principles

### 1. Safety First
- **Zero Compromise**: Never disable security features
- **Reversible**: Every change can be rolled back
- **Logged**: Complete audit trail of all modifications
- **Backed Up**: Automatic registry backups before changes
- **Verified**: Pre and post-application validation

### 2. Transparency
- **Open Source**: Full code visibility
- **No Telemetry**: No data collection or reporting
- **Local Only**: All processing happens locally
- **Clear Logging**: Detailed audit logs
- **User Control**: User approves every change

### 3. Modularity
- **Separation of Concerns**: Each module has single responsibility
- **Loose Coupling**: Modules are independent
- **Easy Testing**: Each component testable in isolation
- **Extensible**: Easy to add new optimizations
- **Reusable**: Components can be used independently

### 4. Performance
- **Efficient Detection**: Optimized hardware queries
- **Lazy Loading**: Load data only when needed
- **Batch Operations**: Combine registry operations
- **Smart Caching**: Cache profile data between updates
- **Light UI**: Responsive interface with minimal overhead

## Core Components

### Admin Management (`core/admin.py`)
Handles administrator privilege detection and enforcement.

**Key Functions:**
- `check_admin_privileges()` - Verify admin status
- `is_admin()` - Quick admin check
- `require_admin()` - Decorator for admin-only functions

**Usage:**
```python
from core.admin import require_admin

@require_admin
def dangerous_operation():
    pass
```

### Hardware Detection (`core/hardware.py`)
Detects and profiles system hardware.

**Key Classes:**
- `SystemProfile` - Complete system information
- `CPUInfo` - CPU specifications
- `GPUInfo` - GPU specifications
- `HardwareDetector` - Main detection engine

**Usage:**
```python
from core.hardware import HardwareDetector

detector = HardwareDetector()
profile = detector.get_full_profile()
print(f"CPU: {profile.cpu.brand}")
print(f"GPUs: {len(profile.gpus)}")
```

### Registry Operations (`core/registry.py`)
Safe registry modification with automatic backups.

**Key Classes:**
- `RegistryManager` - Registry operations
- `RegistryBackup` - Backup and restore system

**Key Features:**
- Automatic backup before modification
- Type-safe value setting
- Structured backup files (JSON)
- Complete rollback capability

**Usage:**
```python
from core.registry import RegistryManager

reg = RegistryManager()
reg.set_value(
    r"HKCU\Software\Microsoft\GameBar",
    "AllowAutoGameMode",
    1
)

# Later: restore
reg.backup.restore_backup("backup_name")
```

### Optimization Engine (`core/optimizer.py`)
Manages optimization registration and application.

**Key Classes:**
- `OptimizationEngine` - Main engine
- `Optimization` - Optimization definition
- `RiskLevel` - Risk classification enum

**Usage:**
```python
from core.optimizer import OptimizationEngine, Optimization, RiskLevel

engine = OptimizationEngine()
opt = Optimization(
    id="my_opt",
    name="My Optimization",
    category="Performance",
    description="Does something cool",
    explanation="How it works",
    risk_level=RiskLevel.SAFE,
    requires_reboot=False,
    reversible=True,
    default_enabled=True,
    compatibility=["Windows 10", "Windows 11"]
)

engine.register_optimization(opt)
engine.apply_optimization("my_opt")
```

## Adding New Optimizations

### Step 1: Create Optimization Module

```python
# src/optimizations/my_category.py
from core.registry import RegistryManager

class MyOptimizations:
    def __init__(self):
        self.registry = RegistryManager()
    
    def my_optimization(self) -> bool:
        """My awesome optimization.
        
        Returns:
            bool: Success status
        """
        try:
            # Perform optimization
            self.registry.set_value(
                r"HKCU\Software\...",
                "ValueName",
                1
            )
            return True
        except Exception as e:
            logger.error(f"Failed: {e}")
            return False
```

### Step 2: Register in Configuration

```json
// config/optimizations.json
{
  "optimizations": [
    {
      "id": "my_opt_id",
      "name": "My Optimization",
      "category": "My Category",
      "description": "Short description",
      "explanation": "How it works",
      "risk_level": "SAFE",
      "requires_reboot": false,
      "reversible": true,
      "default_enabled": true,
      "compatibility": ["Windows 10", "Windows 11"]
    }
  ]
}
```

### Step 3: Integrate with UI

```python
# In dashboard.py
from optimizations.my_category import MyOptimizations

class TweakerDashboard:
    def __init__(self):
        self.my_opts = MyOptimizations()
        # Add to optimization list
```

## Logging System

### Application Logs (`logs/tweaker.log`)
Main application log with INFO level and above.

```
[2024-07-02 17:45:35] INFO     | tweaker | Optimization applied: Game Mode
[2024-07-02 17:45:36] WARNING  | tweaker | GPU scheduling disabled (reboot required)
[2024-07-02 17:45:37] ERROR    | tweaker | Failed to set registry value
```

### Audit Log (`logs/audit.log`)
Detailed audit trail of all optimizations.

```
[2024-07-02T17:45:35] | Game Mode | Windows Performance | OFF: 0 | ON: 1 | RISK: SAFE | STATUS: SUCCESS
```

### Usage

```python
from utils.logger import setup_logging, OptimizationLogger

logger = setup_logging()  # Setup for main logs
audit = OptimizationLogger()  # Setup for audit logs

audit.log_optimization(
    name="Game Mode",
    category="Windows Performance",
    old_value="Disabled",
    new_value="Enabled",
    risk_level="SAFE",
    status="SUCCESS"
)
```

## Testing

### Running Tests

```bash
# Run all tests
python -m pytest tests/

# Run specific test file
python -m pytest tests/test_core.py

# Run with coverage
python -m pytest --cov=src tests/
```

### Writing Tests

```python
# tests/test_my_feature.py
import unittest
from src.core.my_module import MyClass

class TestMyFeature(unittest.TestCase):
    def setUp(self):
        self.obj = MyClass()
    
    def test_basic_functionality(self):
        result = self.obj.some_method()
        self.assertTrue(result)
    
    def tearDown(self):
        # Cleanup
        pass
```

## Configuration System

### Application Settings (`config/settings.json`)

```json
{
  "application": {
    "name": "FPS Gaming Tweaker",
    "version": "1.0.0"
  },
  "safety": {
    "never_modify": ["antivirus", "windows_defender"],
    "require_admin": true
  }
}
```

### Optimization Definitions (`config/optimizations.json`)

Defines all available optimizations with metadata.

## Performance Benchmarking

### Snapshot Format

```json
{
  "timestamp": "2024-07-02T17:45:35",
  "cpu": {
    "percent": 45.2,
    "frequency_current_ghz": 3.6,
    "frequency_max_ghz": 4.8
  },
  "memory": {
    "total_gb": 32,
    "used_gb": 18,
    "percent": 56.25
  },
  "disk": {
    "read_mb": 1024,
    "write_mb": 512
  },
  "processes": 156
}
```

## Backup System

### Backup File Format

```json
{
  "timestamp": "2024-07-02T17:45:35",
  "key_path": "HKCU\\Software\\...",
  "value_name": "ValueName",
  "value": 1,
  "type": 4
}
```

### Recovery Process

1. Find backup file in `data/backups/`
2. Call `RegistryBackup.restore_backup(backup_name)`
3. System automatically restores original value

## Development Workflow

### 1. Setup Development Environment

```bash
git clone https://github.com/jespereckl-ux/tweaker.git
cd tweaker
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python setup_dirs.py
```

### 2. Create Feature Branch

```bash
git checkout -b feature/your-feature
```

### 3. Implement Feature

- Add code to appropriate module
- Add unit tests
- Update documentation
- Add to changelog

### 4. Test Locally

```bash
python -m pytest tests/
python main.py --check-admin
python main.py
```

### 5. Commit and Push

```bash
git add .
git commit -m "Add: Your feature description"
git push origin feature/your-feature
```

### 6. Create Pull Request

Describe your changes and reference any issues.

## Code Style

### Python Style Guide (PEP 8)
- 4 spaces for indentation
- Max 88 characters per line
- Use type hints
- Comprehensive docstrings

### Example

```python
def calculate_performance_boost(
    cpu_cores: int,
    current_fps: float,
    optimization_category: str
) -> float:
    """
    Calculate expected FPS boost from optimization.
    
    Args:
        cpu_cores: Number of CPU cores
        current_fps: Current FPS reading
        optimization_category: Category of optimization
        
    Returns:
        float: Expected FPS boost percentage
        
    Raises:
        ValueError: If FPS is negative
    """
    if current_fps < 0:
        raise ValueError("FPS cannot be negative")
    
    # Implementation
    return boost_amount
```

## Version Management

Follows Semantic Versioning: `MAJOR.MINOR.PATCH`

- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes

## Deployment Checklist

- [ ] All tests pass
- [ ] Code follows style guide
- [ ] Documentation updated
- [ ] Changelog updated
- [ ] Version bumped in `__init__.py`
- [ ] Security review completed
- [ ] Performance verified
- [ ] All features tested on Windows 10 and 11

## Troubleshooting Development

### Import Errors

Ensure `src/` is in Python path:
```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / 'src'))
```

### Admin Requirement

Always run development scripts as Administrator for full functionality.

### Registry Access Denied

Ensure you have administrator privileges and the registry key exists.

---

**Questions? See CONTRIBUTING.md for guidelines or open an issue on GitHub.**

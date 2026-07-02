# Contributing to FPS Gaming Tweaker

Thank you for your interest in contributing to this project!

## Guidelines

### Safety First
- **Never** add optimizations that compromise Windows security
- **Never** add features that disable antivirus or security software
- **Every** change must be reversible
- **All** modifications must be logged

### Code Quality
- Use type hints for all functions
- Include comprehensive docstrings
- Follow PEP 8 style guidelines
- Add unit tests for new functionality
- Use logging instead of print statements

### Risk Assessment
- Classify all changes with risk levels (SAFE, LOW, MEDIUM, HIGH)
- Document potential side effects
- Provide rollback procedures
- Test on multiple Windows versions

### Pull Request Process
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/YourFeature`)
3. Commit changes with clear messages
4. Push to your fork
5. Submit a pull request with detailed description

### Prohibited Changes
❌ Disabling security features
❌ Modifying antivirus behavior
❌ Non-reversible system changes
❌ Undocumented registry modifications
❌ Bypassing Windows protections
✅ Performance optimizations
✅ Configuration helpers
✅ Game-specific guidance
✅ Hardware detection improvements

## Testing

Before submitting:
```bash
python -m pytest tests/
python main.py --check-admin
python main.py --benchmark
```

## Questions?

Open an issue for discussion before implementing major changes.

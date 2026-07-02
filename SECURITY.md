# Security Policy

## Reporting Security Issues

If you discover a security vulnerability, please email security@example.com instead of using the issue tracker.

## What We Protect

This application **never**:
- Disables antivirus software
- Removes security updates
- Bypasses Windows protections
- Modifies SmartScreen settings
- Tampers with Secure Boot
- Disables Windows Defender
- Compromises system integrity

## What We Monitor

✅ All registry modifications (logged automatically)
✅ System changes (backed up before application)
✅ User confirmations (required for high-risk operations)
✅ Rollback capability (maintained for every change)

## Security Best Practices

1. **Keep Windows Updated**: Security patches are essential
2. **Maintain Antivirus**: Windows Defender is enabled by default
3. **Use Strong Passwords**: Protect your system
4. **Regular Backups**: Always have a recovery point
5. **Verify Downloads**: Only download from official repository
6. **Read Changelogs**: Understand what each update does

## Verified Safety Features

🔒 Open-source code for community audit
🔒 No telemetry or data collection
🔒 No internet connectivity required
🔒 Local file-based logging only
🔒 Fully reversible changes
🔒 Comprehensive backup system

## Incident Response

If you believe the application caused an issue:

1. **Rollback immediately**: `python main.py --rollback-all`
2. **Create system restore point**: Windows will prompt
3. **Report the issue** with logs from `logs/tweaker.log`
4. **Do not disable security features** while investigating

## Compliance

- ✅ Meets Windows 10/11 security standards
- ✅ Respects Windows Defender guidelines
- ✅ Compatible with enterprise security policies
- ✅ No anti-cheat system interference
- ✅ No kernel-level modifications

---

**Security is our top priority. Every change is transparent, logged, and reversible.**

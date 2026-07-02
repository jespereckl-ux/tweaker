#!/usr/bin/env python3
"""
Administrator Privileges Management

Handles detection and elevation of admin privileges.
"""

import os
import sys
import ctypes
from typing import Tuple


def check_admin_privileges() -> Tuple[bool, str]:
    """
    Check if the current process has administrator privileges.
    
    Returns:
        Tuple[bool, str]: (is_admin, reason_if_not)
    """
    try:
        return bool(ctypes.windll.shell32.IsUserAnAdmin()), ""
    except Exception as e:
        return False, f"Could not verify: {str(e)}"


def is_admin() -> bool:
    """
    Lightweight admin check.
    
    Returns:
        bool: True if running as administrator
    """
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def require_admin(func):
    """
    Decorator to ensure a function runs with admin privileges.
    
    Args:
        func: Function to decorate
        
    Returns:
        Decorated function
    """
    def wrapper(*args, **kwargs):
        if not is_admin():
            raise PermissionError(
                "This operation requires administrator privileges. "
                "Please restart with 'Run as Administrator'."
            )
        return func(*args, **kwargs)
    return wrapper

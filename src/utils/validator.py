#!/usr/bin/env python3
"""
Validation Utilities

Validates system state and optimization results.
"""

import logging
from typing import Callable, Any, Tuple

logger = logging.getLogger(__name__)


class ValidationError(Exception):
    """Raised when validation fails."""
    pass


class Validator:
    """Validates optimizations and system state."""
    
    @staticmethod
    def validate_registry_value(
        registry_manager,
        key_path: str,
        value_name: str,
        expected_value: Any
    ) -> bool:
        """
        Validate a registry value was set correctly.
        
        Args:
            registry_manager: RegistryManager instance
            key_path: Registry key path
            value_name: Value name
            expected_value: Expected value
            
        Returns:
            bool: Validation result
        """
        try:
            result = registry_manager.get_value(key_path, value_name)
            if result is None:
                logger.warning(f"Registry value not found: {key_path}\\{value_name}")
                return False
            
            actual_value, _ = result
            if actual_value != expected_value:
                logger.warning(
                    f"Registry value mismatch: expected {expected_value}, "
                    f"got {actual_value}"
                )
                return False
            
            return True
        
        except Exception as e:
            logger.error(f"Validation error: {e}")
            return False
    
    @staticmethod
    def validate_with_callback(
        callback: Callable,
        *args,
        **kwargs
    ) -> Tuple[bool, str]:
        """
        Validate using a custom callback function.
        
        Args:
            callback: Validation function
            *args: Arguments for callback
            **kwargs: Keyword arguments for callback
            
        Returns:
            Tuple[bool, str]: (success, message)
        """
        try:
            result = callback(*args, **kwargs)
            if result:
                return True, "Validation passed"
            else:
                return False, "Validation callback returned False"
        
        except Exception as e:
            logger.error(f"Validation callback error: {e}")
            return False, str(e)

#!/usr/bin/env python3
"""
Registry Operations Manager

Safe registry modification with automatic backups and rollback.
"""

import winreg
import json
from pathlib import Path
from typing import Any, Dict, Optional, Tuple
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class RegistryBackup:
    """Manages registry backups for rollback."""
    
    def __init__(self, backup_dir: Path = None):
        """Initialize backup manager.
        
        Args:
            backup_dir: Directory to store backups
        """
        self.backup_dir = backup_dir or Path(__file__).parent.parent.parent / 'data' / 'backups'
        self.backup_dir.mkdir(parents=True, exist_ok=True)
    
    def create_backup(
        self,
        key_path: str,
        value_name: str,
        backup_name: str
    ) -> bool:
        """Create backup of registry value before modification.
        
        Args:
            key_path: Registry key path
            value_name: Value name to backup
            backup_name: Name for this backup
            
        Returns:
            bool: Success status
        """
        try:
            key, subkey = self._parse_key_path(key_path)
            registry = winreg.ConnectRegistry(None, key)
            
            with winreg.OpenKey(registry, subkey, 0, winreg.KEY_READ) as reg_key:
                try:
                    value, value_type = winreg.QueryValueEx(reg_key, value_name)
                except WindowsError:
                    # Value doesn't exist - store as null
                    value = None
                    value_type = None
            
            backup_data = {
                'timestamp': datetime.now().isoformat(),
                'key_path': key_path,
                'value_name': value_name,
                'value': value,
                'type': value_type
            }
            
            backup_file = self.backup_dir / f"{backup_name}.json"
            with open(backup_file, 'w') as f:
                json.dump(backup_data, f, indent=2)
            
            logger.info(f"Registry backup created: {backup_file}")
            return True
        
        except Exception as e:
            logger.error(f"Failed to create backup: {e}")
            return False
    
    def restore_backup(self, backup_name: str) -> bool:
        """Restore registry from backup.
        
        Args:
            backup_name: Name of backup to restore
            
        Returns:
            bool: Success status
        """
        try:
            backup_file = self.backup_dir / f"{backup_name}.json"
            
            if not backup_file.exists():
                logger.error(f"Backup not found: {backup_file}")
                return False
            
            with open(backup_file, 'r') as f:
                backup_data = json.load(f)
            
            key_path = backup_data['key_path']
            value_name = backup_data['value_name']
            value = backup_data['value']
            value_type = backup_data['type']
            
            # Restore value
            if value is None:
                # Delete the value if it didn't exist originally
                self.delete_value(key_path, value_name)
            else:
                self.set_value(key_path, value_name, value, value_type)
            
            logger.info(f"Registry restored from backup: {backup_name}")
            return True
        
        except Exception as e:
            logger.error(f"Failed to restore backup: {e}")
            return False


class RegistryManager:
    """Manages safe registry modifications."""
    
    # Common registry hive abbreviations
    HIVES = {
        'HKLM': winreg.HKEY_LOCAL_MACHINE,
        'HKCU': winreg.HKEY_CURRENT_USER,
        'HKCR': winreg.HKEY_CLASSES_ROOT,
        'HKU': winreg.HKEY_USERS,
    }
    
    # Registry value types
    VALUE_TYPES = {
        'REG_SZ': winreg.REG_SZ,
        'REG_DWORD': winreg.REG_DWORD,
        'REG_QWORD': winreg.REG_QWORD,
        'REG_BINARY': winreg.REG_BINARY,
        'REG_MULTI_SZ': winreg.REG_MULTI_SZ,
    }
    
    def __init__(self):
        """Initialize registry manager."""
        self.backup = RegistryBackup()
    
    def _parse_key_path(self, key_path: str) -> Tuple[int, str]:
        """Parse registry key path into hive and subkey.
        
        Args:
            key_path: Full registry path (e.g., 'HKLM\\Software\\...')
            
        Returns:
            Tuple: (hive_handle, subkey_path)
        """
        parts = key_path.split('\\', 1)
        hive_name = parts[0]
        subkey = parts[1] if len(parts) > 1 else ""
        
        if hive_name not in self.HIVES:
            raise ValueError(f"Unknown registry hive: {hive_name}")
        
        return self.HIVES[hive_name], subkey
    
    def get_value(
        self,
        key_path: str,
        value_name: str
    ) -> Optional[Tuple[Any, int]]:
        """Get registry value.
        
        Args:
            key_path: Registry key path
            value_name: Name of value to retrieve
            
        Returns:
            Tuple[value, type] or None if not found
        """
        try:
            hive, subkey = self._parse_key_path(key_path)
            registry = winreg.ConnectRegistry(None, hive)
            
            with winreg.OpenKey(registry, subkey, 0, winreg.KEY_READ) as key:
                return winreg.QueryValueEx(key, value_name)
        
        except WindowsError:
            return None
        except Exception as e:
            logger.error(f"Failed to read registry value: {e}")
            return None
    
    def set_value(
        self,
        key_path: str,
        value_name: str,
        value: Any,
        value_type: int = winreg.REG_DWORD
    ) -> bool:
        """Set registry value (with automatic backup).
        
        Args:
            key_path: Registry key path
            value_name: Name of value to set
            value: Value to set
            value_type: Registry value type
            
        Returns:
            bool: Success status
        """
        try:
            hive, subkey = self._parse_key_path(key_path)
            registry = winreg.ConnectRegistry(None, hive)
            
            # Create backup first
            backup_name = f"{subkey.replace(chr(92), '_')}_{value_name}"
            self.backup.create_backup(key_path, value_name, backup_name)
            
            # Set the value
            with winreg.OpenKey(registry, subkey, 0, winreg.KEY_WRITE) as key:
                winreg.SetValueEx(key, value_name, 0, value_type, value)
            
            logger.info(f"Registry value set: {key_path}\\{value_name}")
            return True
        
        except Exception as e:
            logger.error(f"Failed to set registry value: {e}")
            return False
    
    def delete_value(
        self,
        key_path: str,
        value_name: str
    ) -> bool:
        """Delete registry value.
        
        Args:
            key_path: Registry key path
            value_name: Name of value to delete
            
        Returns:
            bool: Success status
        """
        try:
            hive, subkey = self._parse_key_path(key_path)
            registry = winreg.ConnectRegistry(None, hive)
            
            with winreg.OpenKey(registry, subkey, 0, winreg.KEY_WRITE) as key:
                winreg.DeleteValue(key, value_name)
            
            logger.info(f"Registry value deleted: {key_path}\\{value_name}")
            return True
        
        except WindowsError:
            return False
        except Exception as e:
            logger.error(f"Failed to delete registry value: {e}")
            return False
    
    def create_key(self, key_path: str) -> bool:
        """Create registry key if it doesn't exist.
        
        Args:
            key_path: Registry key path
            
        Returns:
            bool: Success status
        """
        try:
            hive, subkey = self._parse_key_path(key_path)
            registry = winreg.ConnectRegistry(None, hive)
            winreg.CreateKey(registry, subkey)
            
            logger.info(f"Registry key created: {key_path}")
            return True
        
        except Exception as e:
            logger.error(f"Failed to create registry key: {e}")
            return False

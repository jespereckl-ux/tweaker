#!/usr/bin/env python3
"""
Logging System

Handles application logging with file and console output.
"""

import logging
import logging.handlers
from pathlib import Path
from datetime import datetime


def setup_logging(name: str = 'tweaker', level=logging.INFO) -> logging.Logger:
    """
    Setup logging for the application.
    
    Args:
        name: Logger name
        level: Logging level
        
    Returns:
        logging.Logger: Configured logger
    """
    log_dir = Path(__file__).parent.parent.parent / 'logs'
    log_dir.mkdir(parents=True, exist_ok=True)
    
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # File handler with rotation
    log_file = log_dir / 'tweaker.log'
    file_handler = logging.handlers.RotatingFileHandler(
        log_file,
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5
    )
    file_handler.setLevel(logging.DEBUG)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    
    # Formatter
    formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)-8s | %(name)s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # Add handlers
    if not logger.handlers:
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
    
    return logger


class OptimizationLogger:
    """Logs optimization operations for audit trail."""
    
    def __init__(self):
        self.logger = logging.getLogger('tweaker')
        self.audit_file = Path(__file__).parent.parent.parent / 'logs' / 'audit.log'
        self.audit_file.parent.mkdir(parents=True, exist_ok=True)
    
    def log_optimization(
        self,
        name: str,
        category: str,
        old_value: str,
        new_value: str,
        risk_level: str,
        status: str,
        rollback_id: str = None
    ) -> None:
        """
        Log an optimization operation.
        
        Args:
            name: Optimization name
            category: Category
            old_value: Previous value
            new_value: New value
            risk_level: Risk level (SAFE, LOW_RISK, MEDIUM_RISK, HIGH_RISK)
            status: Status (SUCCESS, FAILED, PENDING_ROLLBACK)
            rollback_id: ID for rollback reference
        """
        timestamp = datetime.now().isoformat()
        
        entry = (
            f"[{timestamp}] | {name} | {category} | "
            f"OLD: {old_value} | NEW: {new_value} | "
            f"RISK: {risk_level} | STATUS: {status}"
        )
        
        if rollback_id:
            entry += f" | ROLLBACK_ID: {rollback_id}"
        
        with open(self.audit_file, 'a') as f:
            f.write(entry + '\n')
        
        # Also log to main logger
        if status == 'SUCCESS':
            self.logger.info(f"Optimization applied: {name}")
        elif status == 'FAILED':
            self.logger.error(f"Optimization failed: {name}")
        else:
            self.logger.debug(f"Optimization {status}: {name}")

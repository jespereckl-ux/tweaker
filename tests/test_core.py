#!/usr/bin/env python3
"""
Unit Tests

Basic tests for core modules.
"""

import unittest
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from core.admin import is_admin
from core.optimizer import RiskLevel, Optimization
from utils.validator import Validator


class TestAdmin(unittest.TestCase):
    """Test admin privilege detection."""
    
    def test_admin_check(self):
        """Test admin check returns boolean."""
        result = is_admin()
        self.assertIsInstance(result, bool)


class TestOptimizer(unittest.TestCase):
    """Test optimization engine."""
    
    def test_risk_levels(self):
        """Test risk level enum."""
        self.assertEqual(RiskLevel.SAFE.value, "SAFE")
        self.assertEqual(RiskLevel.LOW.value, "LOW_RISK")
        self.assertEqual(RiskLevel.MEDIUM.value, "MEDIUM_RISK")
        self.assertEqual(RiskLevel.HIGH.value, "HIGH_RISK")
    
    def test_optimization_creation(self):
        """Test optimization object creation."""
        opt = Optimization(
            id="test",
            name="Test Optimization",
            category="Testing",
            description="Test",
            explanation="Test explanation",
            risk_level=RiskLevel.SAFE,
            requires_reboot=False,
            reversible=True,
            default_enabled=False,
            compatibility=["Windows 10"]
        )
        
        self.assertEqual(opt.name, "Test Optimization")
        self.assertEqual(opt.risk_level, RiskLevel.SAFE)
        self.assertTrue(opt.reversible)


class TestValidator(unittest.TestCase):
    """Test validation utilities."""
    
    def test_validation_callback(self):
        """Test validation with callback."""
        def always_true():
            return True
        
        success, msg = Validator.validate_with_callback(always_true)
        self.assertTrue(success)
    
    def test_validation_callback_false(self):
        """Test validation callback returns False."""
        def always_false():
            return False
        
        success, msg = Validator.validate_with_callback(always_false)
        self.assertFalse(success)


if __name__ == '__main__':
    unittest.main()

#!/usr/bin/env python3
"""
Optimization Engine

Core optimization application and management system.
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)


class RiskLevel(Enum):
    """Risk levels for optimizations."""
    SAFE = "SAFE"
    LOW = "LOW_RISK"
    MEDIUM = "MEDIUM_RISK"
    HIGH = "HIGH_RISK"


@dataclass
class Optimization:
    """Represents a single optimization."""
    id: str
    name: str
    category: str
    description: str
    explanation: str
    risk_level: RiskLevel
    requires_reboot: bool
    reversible: bool
    default_enabled: bool
    compatibility: List[str]  # Hardware/OS compatibility
    apply_func: callable = None
    validate_func: callable = None


class OptimizationEngine:
    """Manages and applies optimizations."""
    
    def __init__(self):
        self.optimizations: Dict[str, Optimization] = {}
        self.applied_optimizations: set = set()
        self.config_dir = Path(__file__).parent.parent.parent / 'config'
        self.config_dir.mkdir(parents=True, exist_ok=True)
    
    def register_optimization(self, optimization: Optimization) -> None:
        """
        Register an optimization.
        
        Args:
            optimization: Optimization to register
        """
        self.optimizations[optimization.id] = optimization
        logger.debug(f"Registered optimization: {optimization.name}")
    
    def get_optimization(self, opt_id: str) -> Optional[Optimization]:
        """
        Get optimization by ID.
        
        Args:
            opt_id: Optimization ID
            
        Returns:
            Optimization or None
        """
        return self.optimizations.get(opt_id)
    
    def list_optimizations(self) -> None:
        """
        List all available optimizations.
        """
        print("\n📋 Available Optimizations\n" + "="*60)
        
        by_category = {}
        for opt in self.optimizations.values():
            if opt.category not in by_category:
                by_category[opt.category] = []
            by_category[opt.category].append(opt)
        
        for category in sorted(by_category.keys()):
            print(f"\n🎮 {category}")
            print("-" * 60)
            
            for opt in by_category[category]:
                risk_emoji = {
                    RiskLevel.SAFE: "✅",
                    RiskLevel.LOW: "🟢",
                    RiskLevel.MEDIUM: "🟡",
                    RiskLevel.HIGH: "🔴",
                }.get(opt.risk_level, "❓")
                
                print(f"\n{risk_emoji} {opt.name}")
                print(f"   Risk: {opt.risk_level.value}")
                print(f"   Reboot Required: {'Yes' if opt.requires_reboot else 'No'}")
                print(f"   Reversible: {'Yes' if opt.reversible else 'No'}")
                print(f"   {opt.description}")
    
    def get_optimizations_by_category(self, category: str) -> List[Optimization]:
        """
        Get optimizations by category.
        
        Args:
            category: Category name
            
        Returns:
            List of optimizations
        """
        return [opt for opt in self.optimizations.values() 
                if opt.category == category]
    
    def get_optimizations_by_risk(self, risk_level: RiskLevel) -> List[Optimization]:
        """
        Get optimizations by risk level.
        
        Args:
            risk_level: Risk level
            
        Returns:
            List of optimizations
        """
        return [opt for opt in self.optimizations.values() 
                if opt.risk_level == risk_level]
    
    def apply_optimization(self, opt_id: str) -> bool:
        """
        Apply an optimization.
        
        Args:
            opt_id: Optimization ID
            
        Returns:
            bool: Success status
        """
        optimization = self.get_optimization(opt_id)
        if not optimization:
            logger.error(f"Optimization not found: {opt_id}")
            return False
        
        try:
            if optimization.apply_func:
                result = optimization.apply_func()
                
                if result and optimization.validate_func:
                    if optimization.validate_func():
                        self.applied_optimizations.add(opt_id)
                        logger.info(f"Optimization applied: {optimization.name}")
                        return True
                    else:
                        logger.error(f"Validation failed: {optimization.name}")
                        return False
                elif result:
                    self.applied_optimizations.add(opt_id)
                    logger.info(f"Optimization applied: {optimization.name}")
                    return True
            
            return False
        
        except Exception as e:
            logger.error(f"Failed to apply optimization: {e}")
            return False
    
    def rollback_optimization(self, opt_id: str) -> bool:
        """
        Rollback an optimization.
        
        Args:
            opt_id: Optimization ID
            
        Returns:
            bool: Success status
        """
        optimization = self.get_optimization(opt_id)
        if not optimization:
            logger.error(f"Optimization not found: {opt_id}")
            return False
        
        if not optimization.reversible:
            logger.warning(f"Optimization is not reversible: {optimization.name}")
            return False
        
        if opt_id not in self.applied_optimizations:
            logger.warning(f"Optimization was not applied: {opt_id}")
            return False
        
        logger.info(f"Rollback initiated: {optimization.name}")
        self.applied_optimizations.discard(opt_id)
        return True

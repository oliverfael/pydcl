"""
PYDCL: Python Dynamic Cost Layer
Sinphasé (Single-Pass Hierarchical Structuring) Implementation

Module exposure following cost-based governance with bounded complexity.
All imports validated through systematic dependency resolution.
"""

__version__ = "1.0.0"

# Sinphasé-compliant module exposure with cost governance
try:
    # Core calculation engine with cost bounds validation
    from .cost_scores import CostScoreCalculator, DivisionConfig
    
    # Data models with complete dependency chain
    from .models import (
        DivisionType, ProjectStatus, CostFactors, RepositoryMetrics,
        RepositoryConfig, CostCalculationResult, OrganizationCostReport,
        ValidationError, calculate_sinphase_cost
    )
    
    # GitHub integration with systematic validation
    from .github_client import GitHubMetricsClient
    
    # Configuration utilities with governance compliance
    from .utils import validate_config, load_division_config
    
    # CLI interface for command-line operations
    from .cli import main as cli_main
    
except ImportError as e:
    # Sinphasé graceful degradation with diagnostic information
    import sys
    print(f"PYDCL Sinphasé Import Resolution: {e}", file=sys.stderr)
    print("Status: Development Phase - Module Implementation In Progress", file=sys.stderr)

# Sinphasé governance constants
GOVERNANCE_THRESHOLD = 0.6
ISOLATION_THRESHOLD = 0.8

# Public API exposure following single-pass methodology
__all__ = [
    # Core calculation components
    "CostScoreCalculator", "DivisionConfig", "calculate_sinphase_cost",
    
    # Data model hierarchy
    "DivisionType", "ProjectStatus", "CostFactors", "RepositoryMetrics",
    "RepositoryConfig", "CostCalculationResult", "OrganizationCostReport",
    "ValidationError",
    
    # Integration components
    "GitHubMetricsClient", "validate_config", "load_division_config",
    
    # CLI interface
    "cli_main",
    
    # Governance constants
    "GOVERNANCE_THRESHOLD", "ISOLATION_THRESHOLD"
]

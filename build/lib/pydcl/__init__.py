"""
PYDCL: Python Dynamic Cost Layer
Sinphasé-compliant single-pass hierarchical structuring
"""

__version__ = "1.0.0"

# Basic imports aligned with current placeholder implementations
try:
    from .cost_scores import CostScoreCalculator, DivisionConfig
    from .models import DivisionType, RepositoryMetrics
    from .github_client import GitHubMetricsClient
    from .utils import validate_config, load_division_config
except ImportError as e:
    # Graceful degradation for incomplete implementations
    print(f"PYDCL: Module import incomplete - {e}")

__all__ = [
    "CostScoreCalculator", "DivisionConfig", 
    "DivisionType", "RepositoryMetrics",
    "GitHubMetricsClient", "validate_config", "load_division_config"
]

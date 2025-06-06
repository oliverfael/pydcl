"""
PYDCL: Python Dynamic Cost Layer

A division-aware GitHub organization cost modeling toolkit implementing
the OBINexus Sinphas� methodology for hierarchical project structuring.

This package provides:
- Division-aware cost function modeling
- GitHub API integration with telemetry collection
- Sinphas�-compliant cost governance checkpoints
- JSON output for inverted triangle visualization components

Technical Architecture:
- Single-pass compilation requirements
- Cost-based governance with threshold monitoring
- Hierarchical isolation protocols
- Deterministic build behavior enforcement

Authors: OBINexus Computing Team
Lead Architect: Nnamdi Michael Okpala
License: MIT
"""

__version__ = "1.0.0"
__author__ = "OBINexus Computing"
__email__ = "support@obinexuscomputing.com"
__license__ = "MIT"

# Core API exports for deterministic single-pass import resolution
from .cost_scores import CostScoreCalculator, DivisionConfig
from .models import (
    RepositoryMetrics, CostFactors, DivisionMetadata,
    CostCalculationResult, OrganizationCostReport
)
from .github_client import GitHubMetricsClient
from .utils import validate_config, load_division_config

# CLI registration for entry point resolution
from .cli import main as cli_main

# Version information
VERSION_INFO = (1, 0, 0)

# OBINexus Division Constants
SUPPORTED_DIVISIONS = [
    "Computing",
    "UCHE Nnamdi", 
    "Publishing",
    "OBIAxis R&D",
    "TDA",
    "Nkwak?ba",
    "Aegis Engineering"
]

# Cost governance thresholds (Sinphas� compliance)
DEFAULT_COST_THRESHOLD = 0.6
ISOLATION_TRIGGER_THRESHOLD = 0.8
ARCHITECTURAL_REORGANIZATION_THRESHOLD = 1.0

# Status classifications aligned with Sinphas� phases
PROJECT_STATUSES = [
    "Core",          # Stable, foundational components
    "Active",        # Implementation phase projects
    "Incubator",     # Research phase projects
    "Legacy",        # Maintained for compatibility
    "Experimental",  # Pre-research exploration
    "Isolated"       # Components requiring architectural reorganization
]

__all__ = [
    "__version__",
    "CostScoreCalculator",
    "DivisionConfig", 
    "RepositoryMetrics",
    "CostFactors",
    "DivisionMetadata",
    "GitHubMetricsClient",
    "validate_config",
    "load_division_config",
    "SUPPORTED_DIVISIONS",
    "PROJECT_STATUSES",
    "DEFAULT_COST_THRESHOLD",
    "ISOLATION_TRIGGER_THRESHOLD",
    "ARCHITECTURAL_REORGANIZATION_THRESHOLD"
]

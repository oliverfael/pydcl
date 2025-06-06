"""
PYDCL Data Models

Pydantic models for division-aware cost governance implementing
the Sinphasé (Single-Pass Hierarchical Structuring) methodology.
"""

from typing import Dict, List, Optional, Union
from datetime import datetime
from enum import Enum

class DivisionType(str, Enum):
    """OBINexus organizational divisions following structured hierarchy."""
    COMPUTING = "Computing"
    UCHE_NNAMDI = "UCHE Nnamdi"
    PUBLISHING = "Publishing"
    OBIAXIS_RD = "OBIAxis R&D"
    TDA = "TDA"
    NKWAKOBA = "Nkwakọba"
    AEGIS_ENGINEERING = "Aegis Engineering"

class ProjectStatus(str, Enum):
    """Sinphasé-compliant project lifecycle states."""
    CORE = "Core"
    ACTIVE = "Active"
    INCUBATOR = "Incubator"
    LEGACY = "Legacy"
    EXPERIMENTAL = "Experimental"
    ISOLATED = "Isolated"

class CostFactors:
    """Cost calculation weights for repository evaluation."""
    def __init__(self):
        self.stars_weight = 0.2
        self.commit_activity_weight = 0.3
        self.build_time_weight = 0.2
        self.size_weight = 0.2
        self.test_coverage_weight = 0.1
        self.manual_boost = 1.0

class RepositoryMetrics:
    """Repository metrics extracted from GitHub API."""
    def __init__(self, name: str):
        self.name = name
        self.stars_count = 0
        self.commits_last_30_days = 0
        self.size_kb = 0

class RepositoryConfig:
    """Repository-specific configuration from .github/repo.yaml."""
    def __init__(self, division: DivisionType, status: ProjectStatus):
        self.division = division
        self.status = status
        self.cost_factors = CostFactors()

class CostCalculationResult:
    """Complete cost calculation output for a repository."""
    def __init__(self, repository: str, division: DivisionType, status: ProjectStatus):
        self.repository = repository
        self.division = division
        self.status = status
        self.normalized_score = 0.0
        self.governance_alerts = []
        self.sinphase_violations = []
        self.requires_isolation = False

class OrganizationCostReport:
    """Complete cost analysis report for GitHub organization."""
    def __init__(self, organization: str):
        self.organization = organization
        self.total_repositories = 0
        self.analyzed_repositories = 0
        self.repository_scores = []
        self.division_summaries = {}

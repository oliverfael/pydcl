"""
PYDCL Data Models

Pydantic models for division-aware cost governance implementing
the Sinphas‚ (Single-Pass Hierarchical Structuring) methodology.

These models enforce structural validation and type safety for:
- Repository metadata extraction
- Division-specific cost factors
- Sinphas‚ compliance validation
- Cost governance thresholds
"""

from typing import Dict, List, Optional, Union, Literal
from datetime import datetime
from pydantic import BaseModel, Field, validator, root_validator
from enum import Enum


class DivisionType(str, Enum):
    """OBINexus organizational divisions following structured hierarchy."""
    COMPUTING = "Computing"
    UCHE_NNAMDI = "UCHE Nnamdi"
    PUBLISHING = "Publishing"
    OBIAXIS_RD = "OBIAxis R&D"
    TDA = "TDA"
    NKWAKOBA = "Nkwak?ba"
    AEGIS_ENGINEERING = "Aegis Engineering"


class ProjectStatus(str, Enum):
    """Sinphas‚-compliant project lifecycle states."""
    CORE = "Core"                    # Stable, foundational components
    ACTIVE = "Active"                # Implementation phase projects
    INCUBATOR = "Incubator"         # Research phase projects
    LEGACY = "Legacy"               # Maintained for compatibility
    EXPERIMENTAL = "Experimental"   # Pre-research exploration
    ISOLATED = "Isolated"           # Requires architectural reorganization


class CostFactors(BaseModel):
    """Cost calculation weights for repository evaluation."""
    stars_weight: float = Field(default=0.2, ge=0.0, le=1.0)
    commit_activity_weight: float = Field(default=0.3, ge=0.0, le=1.0)
    build_time_weight: float = Field(default=0.2, ge=0.0, le=1.0)
    size_weight: float = Field(default=0.2, ge=0.0, le=1.0)
    test_coverage_weight: float = Field(default=0.1, ge=0.0, le=1.0)
    manual_boost: float = Field(default=1.0, ge=0.1, le=3.0)
    
    @validator('*', pre=True)
    def validate_weights(cls, v):
        """Ensure all weight values are positive and reasonable."""
        if isinstance(v, (int, float)) and v < 0:
            raise ValueError("Cost weights must be non-negative")
        return v
    
    @root_validator
    def validate_total_weights(cls, values):
        """Ensure weights sum to approximately 1.0 (excluding manual_boost)."""
        weight_sum = sum([
            values.get('stars_weight', 0.2),
            values.get('commit_activity_weight', 0.3),
            values.get('build_time_weight', 0.2),
            values.get('size_weight', 0.2),
            values.get('test_coverage_weight', 0.1)
        ])
        if not (0.8 <= weight_sum <= 1.2):
            raise ValueError(f"Weight sum {weight_sum} should be approximately 1.0")
        return values


class DivisionMetadata(BaseModel):
    """Division-specific configuration and governance parameters."""
    division: DivisionType
    description: str
    governance_threshold: float = Field(default=0.6, ge=0.0, le=1.0)
    isolation_threshold: float = Field(default=0.8, ge=0.0, le=1.0)
    priority_boost: float = Field(default=1.0, ge=0.5, le=2.0)
    responsible_architect: Optional[str] = None
    
    class Config:
        use_enum_values = True


class RepositoryMetrics(BaseModel):
    """Raw metrics extracted from GitHub API and CI systems."""
    name: str
    full_name: str
    stars_count: int = Field(ge=0)
    forks_count: int = Field(ge=0)
    watchers_count: int = Field(ge=0)
    size_kb: int = Field(ge=0)
    open_issues_count: int = Field(ge=0)
    commits_last_30_days: int = Field(ge=0)
    last_commit_date: Optional[datetime] = None
    primary_language: Optional[str] = None
    languages: Dict[str, int] = Field(default_factory=dict)
    has_ci: bool = False
    build_time_minutes: Optional[float] = Field(default=None, ge=0)
    test_coverage_percent: Optional[float] = Field(default=None, ge=0, le=100)
    has_readme: bool = False
    has_license: bool = False
    is_fork: bool = False
    is_archived: bool = False
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat() if v else None
        }


class RepositoryConfig(BaseModel):
    """Repository-specific configuration from .github/repo.yaml."""
    division: DivisionType
    status: ProjectStatus
    cost_factors: CostFactors = Field(default_factory=CostFactors)
    tags: List[str] = Field(default_factory=list)
    dependencies: List[str] = Field(default_factory=list)
    sinphase_compliance: bool = True
    isolation_required: bool = False
    manual_override: Optional[Dict[str, Union[str, float, bool]]] = None
    
    class Config:
        use_enum_values = True


class CostCalculationResult(BaseModel):
    """Complete cost calculation output for a repository."""
    repository: str
    division: DivisionType
    status: ProjectStatus
    raw_metrics: RepositoryMetrics
    cost_factors: CostFactors
    calculated_score: float = Field(ge=0.0)
    normalized_score: float = Field(ge=0.0, le=100.0)
    governance_alerts: List[str] = Field(default_factory=list)
    sinphase_violations: List[str] = Field(default_factory=list)
    requires_isolation: bool = False
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        use_enum_values = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class DivisionSummary(BaseModel):
    """Aggregated statistics for a division."""
    division: DivisionType
    total_repositories: int = Field(ge=0)
    average_cost_score: float = Field(ge=0.0)
    status_distribution: Dict[ProjectStatus, int] = Field(default_factory=dict)
    governance_violations: int = Field(ge=0)
    isolation_candidates: int = Field(ge=0)
    top_repositories: List[str] = Field(default_factory=list)
    
    class Config:
        use_enum_values = True


class OrganizationCostReport(BaseModel):
    """Complete cost analysis report for GitHub organization."""
    organization: str
    generation_timestamp: datetime = Field(default_factory=datetime.utcnow)
    total_repositories: int = Field(ge=0)
    analyzed_repositories: int = Field(ge=0)
    division_summaries: Dict[DivisionType, DivisionSummary] = Field(default_factory=dict)
    repository_scores: List[CostCalculationResult] = Field(default_factory=list)
    global_governance_alerts: List[str] = Field(default_factory=list)
    sinphase_compliance_rate: float = Field(ge=0.0, le=1.0)
    
    class Config:
        use_enum_values = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
    
    def get_inverted_triangle_layers(self) -> Dict[str, List[CostCalculationResult]]:
        """Generate inverted triangle visualization layers."""
        sorted_repos = sorted(
            self.repository_scores, 
            key=lambda x: x.normalized_score, 
            reverse=True
        )
        
        total_count = len(sorted_repos)
        if total_count == 0:
            return {"surface": [], "active": [], "core": []}
        
        # Layer distribution: 30% surface, 40% active, 30% core
        surface_count = max(1, int(total_count * 0.3))
        active_count = max(1, int(total_count * 0.4))
        
        return {
            "surface": sorted_repos[:surface_count],
            "active": sorted_repos[surface_count:surface_count + active_count],
            "core": sorted_repos[surface_count + active_count:]
        }


class ValidationError(BaseModel):
    """Structured validation error reporting."""
    field: str
    message: str
    value: Optional[Union[str, int, float]] = None
    severity: Literal["warning", "error", "critical"] = "error"

"""
PYDCL Data Models - Sinphasé Compliant Implementation

Single-Pass Hierarchical Structuring with cost-based governance checkpoints.
All classes implement bounded complexity within measurable thresholds.
"""

from typing import Dict, List, Optional, Union, Literal, Any
from datetime import datetime
from enum import Enum

# Sinphasé Cost Governance Threshold Constants
GOVERNANCE_THRESHOLD = 0.6
ISOLATION_THRESHOLD = 0.8
ARCHITECTURAL_REORGANIZATION_THRESHOLD = 1.0

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
    CORE = "Core"                    # Stable, foundational components
    ACTIVE = "Active"                # Implementation phase projects
    INCUBATOR = "Incubator"         # Research phase projects
    LEGACY = "Legacy"               # Maintained for compatibility
    EXPERIMENTAL = "Experimental"   # Pre-research exploration
    ISOLATED = "Isolated"           # Requires architectural reorganization

class CostFactors:
    """Cost calculation weights implementing Sinphasé governance."""
    def __init__(self) -> None:
        self.stars_weight = 0.2
        self.commit_activity_weight = 0.3
        self.build_time_weight = 0.2
        self.size_weight = 0.2
        self.test_coverage_weight = 0.1
        self.manual_boost = 1.0
        
    def validate_cost_bounds(self) -> bool:
        """Validate cost factors remain within Sinphasé bounds."""
        total_weight = (self.stars_weight + self.commit_activity_weight + 
                       self.build_time_weight + self.size_weight + 
                       self.test_coverage_weight)
        return 0.8 <= total_weight <= 1.2

class RepositoryMetrics:
    """Repository metrics with Sinphasé complexity bounds."""
    def __init__(self, name: str):
        self.name = name
        self.stars_count = 0
        self.commits_last_30_days = 0
        self.size_kb = 0
        self.build_time_minutes = None
        self.test_coverage_percent = None
        
    def calculate_complexity_score(self) -> float:
        """Calculate repository complexity within bounded thresholds."""
        # Sinphasé bounded complexity calculation
        normalized_size = min(self.size_kb / 50000.0, 1.0)
        normalized_activity = min(self.commits_last_30_days / 100.0, 1.0)
        return (normalized_size + normalized_activity) / 2.0

class RepositoryConfig:
    """Repository-specific configuration implementing Sinphasé governance."""
    def __init__(self, division: DivisionType, status: ProjectStatus):
        self.division = division
        self.status = status
        self.cost_factors = CostFactors()
        self.sinphase_compliance = True
        self.isolation_required = False
        
    def validate_sinphase_compliance(self) -> List[str]:
        """Validate Sinphasé methodology compliance."""
        violations = []
        if not self.cost_factors.validate_cost_bounds():
            violations.append("Cost factors exceed Sinphasé bounds")
        if self.isolation_required and self.status != ProjectStatus.ISOLATED:
            violations.append("Isolation required but status not updated")
        return violations

class DivisionMetadata:
    """
    Division-specific metadata implementing Sinphasé governance compliance.
    
    Technical Implementation:
    - Division-aware configuration parameter management
    - Governance threshold enforcement per division specifications
    - Priority boost coefficient systematic application
    - Responsible architect assignment and accountability tracking
    """
    
    def __init__(
        self,
        division: DivisionType,
        description: Optional[str] = None,
        governance_threshold: float = 0.6,
        isolation_threshold: float = 0.8,
        priority_boost: float = 1.0,
        responsible_architect: Optional[str] = None
    ):
        """
        Initialize division metadata with systematic validation.
        
        Args:
            division: OBINexus division type classification
            description: Technical description of division responsibilities
            governance_threshold: Cost score threshold for governance alerts (0.0-1.0)
            isolation_threshold: Cost score threshold for isolation recommendations (0.0-1.0)
            priority_boost: Division-specific priority coefficient (0.1-3.0)
            responsible_architect: Technical lead responsible for division
        """
        self.division = division
        self.description = description or f"{division.value} Division"
        self.governance_threshold = governance_threshold
        self.isolation_threshold = isolation_threshold
        self.priority_boost = priority_boost
        self.responsible_architect = responsible_architect
        self.created_at = datetime.utcnow()
        
        # Validate Sinphasé compliance bounds
        self._validate_threshold_bounds()
        self._validate_priority_bounds()
    
    def _validate_threshold_bounds(self) -> None:
        """Validate governance and isolation thresholds within Sinphasé bounds."""
        if not (0.0 <= self.governance_threshold <= 1.0):
            raise ValueError(f"Governance threshold out of bounds: {self.governance_threshold}")
        
        if not (0.0 <= self.isolation_threshold <= 1.0):
            raise ValueError(f"Isolation threshold out of bounds: {self.isolation_threshold}")
        
        if self.governance_threshold > self.isolation_threshold:
            raise ValueError(
                f"Governance threshold ({self.governance_threshold}) "
                f"cannot exceed isolation threshold ({self.isolation_threshold})"
            )
    
    def _validate_priority_bounds(self) -> None:
        """Validate priority boost within reasonable operational bounds."""
        if not (0.1 <= self.priority_boost <= 3.0):
            raise ValueError(f"Priority boost out of bounds: {self.priority_boost}")
    
    def is_governance_compliant(self, cost_score: float) -> bool:
        """
        Evaluate governance compliance for given cost score.
        
        Args:
            cost_score: Normalized cost score (0.0-1.0)
            
        Returns:
            Boolean indicating governance threshold compliance
        """
        return cost_score <= self.governance_threshold
    
    def requires_isolation(self, cost_score: float) -> bool:
        """
        Evaluate isolation requirement for given cost score.
        
        Args:
            cost_score: Normalized cost score (0.0-1.0)
            
        Returns:
            Boolean indicating isolation requirement per division thresholds
        """
        return cost_score >= self.isolation_threshold
    
    def apply_priority_boost(self, base_score: float) -> float:
        """
        Apply division-specific priority boost to base cost score.
        
        Args:
            base_score: Base cost calculation result
            
        Returns:
            Priority-adjusted cost score with division coefficient applied
        """
        boosted_score = base_score * self.priority_boost
        
        # Ensure boosted score remains within mathematical bounds
        return min(boosted_score, ARCHITECTURAL_REORGANIZATION_THRESHOLD)
    
    def generate_governance_report(self, repositories: List[Dict]) -> Dict[str, Any]:
        """
        Generate division-specific governance compliance report.
        
        Args:
            repositories: List of repository analysis results
            
        Returns:
            Comprehensive division governance compliance assessment
        """
        total_repos = len(repositories)
        compliant_repos = sum(1 for repo in repositories 
                            if self.is_governance_compliant(repo.get('cost_score', 0.0)))
        isolation_candidates = sum(1 for repo in repositories
                                 if self.requires_isolation(repo.get('cost_score', 0.0)))
        
        compliance_rate = compliant_repos / total_repos if total_repos > 0 else 1.0
        
        return {
            'division': self.division.value,
            'total_repositories': total_repos,
            'compliant_repositories': compliant_repos,
            'compliance_rate': compliance_rate,
            'isolation_candidates': isolation_candidates,
            'governance_threshold': self.governance_threshold,
            'isolation_threshold': self.isolation_threshold,
            'responsible_architect': self.responsible_architect,
            'assessment_timestamp': datetime.utcnow().isoformat()
        }
    
    def __repr__(self) -> str:
        """Technical string representation for debugging and logging."""
        return (
            f"DivisionMetadata("
            f"division={self.division.value}, "
            f"governance_threshold={self.governance_threshold}, "
            f"isolation_threshold={self.isolation_threshold}, "
            f"priority_boost={self.priority_boost})"
        )

class CostCalculationResult:
    """Complete cost calculation with governance validation."""
    def __init__(self, repository: str, division: DivisionType, status: ProjectStatus):
        self.repository = repository
        self.division = division
        self.status = status
        self.normalized_score = 0.0
        self.governance_alerts: List[str] = []
        self.sinphase_violations: List[str] = []
        self.requires_isolation = False
        self.raw_metrics = None
        self.cost_factors = CostFactors()
        self.calculated_score = 0.0  # Raw calculation result (0.0-1.0)
        
    def apply_governance_thresholds(self) -> None:
        """Apply Sinphasé governance thresholds with isolation triggers."""
        if self.normalized_score >= GOVERNANCE_THRESHOLD * 100:
            self.governance_alerts.append(f"Governance threshold exceeded: {self.normalized_score:.1f}")
        
        if self.normalized_score >= ISOLATION_THRESHOLD * 100:
            self.governance_alerts.append(f"Isolation threshold exceeded: {self.normalized_score:.1f}")
            self.requires_isolation = True
            
        if self.normalized_score >= ARCHITECTURAL_REORGANIZATION_THRESHOLD * 100:
            self.governance_alerts.append("Architectural reorganization required")
    
    def set_calculation_result(self, raw_score: float, normalized_score: float, alerts: List[str]) -> None:
        """Set calculation results with systematic validation."""
        self.calculated_score = raw_score
        self.normalized_score = normalized_score
        self.governance_alerts = alerts.copy()
        self.apply_governance_thresholds()

class OrganizationCostReport:
    """Complete cost analysis implementing Sinphasé governance."""
    def __init__(self, organization: str):
        self.organization = organization
        self.total_repositories = 0
        self.analyzed_repositories = 0
        self.repository_scores: List[CostCalculationResult] = []
        self.division_summaries: Dict[str, Dict[str, Any]] = {}
        self.sinphase_compliance_rate = 1.0
        
    def calculate_governance_metrics(self) -> None:
        """Calculate organization-wide governance compliance."""
        if not self.repository_scores:
            return
            
        total_violations = sum(len(repo.sinphase_violations) for repo in self.repository_scores)
        self.sinphase_compliance_rate = 1.0 - (total_violations / len(self.repository_scores))
        
    def get_isolation_candidates(self) -> List[CostCalculationResult]:
        """Identify repositories requiring isolation per Sinphasé protocol."""
        return [repo for repo in self.repository_scores if repo.requires_isolation]

class ValidationError:
    """Structured validation error with Sinphasé compliance tracking."""
    def __init__(self, field: str, message: str, severity: str = "error"):
        self.field = field
        self.message = message
        self.severity = severity
        self.timestamp = datetime.utcnow()
        
    def is_sinphase_violation(self) -> bool:
        """Determine if error represents Sinphasé methodology violation."""
        sinphase_keywords = ["cost", "threshold", "isolation", "complexity", "governance"]
        return any(keyword in self.message.lower() for keyword in sinphase_keywords)

# Sinphasé Cost Function Implementation
def calculate_sinphase_cost(metrics: RepositoryMetrics, factors: CostFactors) -> float:
    """
    Core Sinphasé cost calculation with bounded complexity validation.
    
    Cost = Σ(metrici × weighti) + circularpenalty + temporalpressure
    Where cost must remain <= 0.6 for autonomous operation.
    """
    complexity_score = metrics.calculate_complexity_score()
    
    # Weighted cost calculation
    base_cost = (
        (metrics.stars_count / 1000.0) * factors.stars_weight +
        (metrics.commits_last_30_days / 100.0) * factors.commit_activity_weight +
        complexity_score * (factors.size_weight + factors.build_time_weight) +
        (factors.test_coverage_weight * 0.8)  # Base coverage assumption
    )
    
    # Apply manual boost with governance bounds
    final_cost = base_cost * factors.manual_boost
    
    # Sinphasé governance: trigger isolation if cost exceeds threshold
    if final_cost > GOVERNANCE_THRESHOLD:
        return min(final_cost, ARCHITECTURAL_REORGANIZATION_THRESHOLD)
    
    return final_cost
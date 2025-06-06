"""
PYDCL Cost Calculation Engine

Technical implementation of division-aware cost modeling following
the Sinphas‚ (Single-Pass Hierarchical Structuring) methodology.

Core Technical Features:
- Weighted cost factor calculation with governance threshold validation
- Sinphas‚ compliance monitoring with architectural reorganization triggers
- Division-specific parameter application and priority boost calculation
- Systematic normalization and aggregation algorithms

Architecture: Deterministic calculation engine with validation checkpoints
Lead Engineer: Technical implementation aligned with Nnamdi Okpala's specifications
"""

import logging
import math
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta

from .models import (
    RepositoryMetrics, RepositoryConfig, CostFactors, DivisionMetadata,
    CostCalculationResult, DivisionSummary, OrganizationCostReport,
    DivisionType, ProjectStatus, ValidationError
)

logger = logging.getLogger(__name__)


class CostScoreCalculator:
    """
    Technical cost calculation engine implementing Sinphas‚ methodology.
    
    Provides systematic cost evaluation with:
    - Weighted factor calculation according to division parameters
    - Governance threshold validation and violation detection
    - Sinphas‚ compliance monitoring for architectural reorganization
    - Deterministic normalization for consistent scoring
    """
    
    def __init__(self):
        """Initialize calculation engine with technical constants."""
        # Sinphas‚ governance thresholds
        self.default_governance_threshold = 0.6
        self.isolation_trigger_threshold = 0.8
        self.architectural_reorganization_threshold = 1.0
        
        # Technical calculation parameters
        self.normalization_ceiling = 100.0
        self.temporal_decay_factor = 0.1
        self.circular_penalty_weight = 0.2
        
        # Division configuration cache
        self._division_configs: Dict[DivisionType, DivisionMetadata] = {}
        
        logger.info("CostScoreCalculator initialized with Sinphas‚ parameters")
    
    def calculate_repository_cost(
        self,
        metrics: RepositoryMetrics,
        config: Optional[RepositoryConfig] = None
    ) -> CostCalculationResult:
        """
        Execute systematic cost calculation for repository.
        
        Technical Implementation:
        1. Parameter validation and configuration loading
        2. Raw metric normalization and temporal adjustment
        3. Weighted cost factor application
        4. Governance threshold validation
        5. Sinphas‚ compliance assessment
        
        Args:
            metrics: Raw repository metrics from GitHub API
            config: Repository-specific configuration (optional)
            
        Returns:
            Complete cost calculation result with governance alerts
        """
        
        try:
            # Phase 1: Configuration Resolution
            effective_config = self._resolve_repository_configuration(config)
            division_metadata = self._get_division_metadata(effective_config.division)
            
            # Phase 2: Metric Normalization
            normalized_metrics = self._normalize_raw_metrics(metrics)
            
            # Phase 3: Cost Factor Application
            weighted_score = self._calculate_weighted_score(
                normalized_metrics=normalized_metrics,
                cost_factors=effective_config.cost_factors,
                division_metadata=division_metadata
            )
            
            # Phase 4: Governance Validation
            governance_alerts = self._validate_governance_thresholds(
                score=weighted_score,
                division_metadata=division_metadata,
                repository_name=metrics.name
            )
            
            # Phase 5: Sinphas‚ Compliance Assessment
            sinphase_violations = self._assess_sinphase_compliance(
                metrics=metrics,
                config=effective_config,
                calculated_score=weighted_score
            )
            
            # Phase 6: Final Score Normalization
            normalized_score = self._normalize_final_score(weighted_score)
            
            # Determine isolation requirement
            requires_isolation = (
                weighted_score >= self.isolation_trigger_threshold or
                len(sinphase_violations) > 0 or
                effective_config.isolation_required
            )
            
            result = CostCalculationResult(
                repository=metrics.name,
                division=effective_config.division,
                status=effective_config.status,
                raw_metrics=metrics,
                cost_factors=effective_config.cost_factors,
                calculated_score=weighted_score,
                normalized_score=normalized_score,
                governance_alerts=governance_alerts,
                sinphase_violations=sinphase_violations,
                requires_isolation=requires_isolation
            )
            
            logger.debug(f"Cost calculated for {metrics.name}: {normalized_score:.1f}")
            return result
            
        except Exception as e:
            logger.error(f"Cost calculation failed for {metrics.name}: {e}")
            raise
    
    def _resolve_repository_configuration(
        self, 
        config: Optional[RepositoryConfig]
    ) -> RepositoryConfig:
        """Resolve effective configuration with systematic defaults."""
        
        if config is not None:
            return config
        
        # Default configuration for repositories without explicit config
        return RepositoryConfig(
            division=DivisionType.COMPUTING,  # Default to Computing division
            status=ProjectStatus.ACTIVE,
            cost_factors=CostFactors()
        )
    
    def _get_division_metadata(self, division: DivisionType) -> DivisionMetadata:
        """Retrieve or generate division-specific metadata."""
        
        if division in self._division_configs:
            return self._division_configs[division]
        
        # Generate default division metadata
        metadata = DivisionMetadata(
            division=division,
            description=f"{division.value} Division",
            governance_threshold=self.default_governance_threshold,
            isolation_threshold=self.isolation_trigger_threshold,
            priority_boost=self._get_division_priority_boost(division)
        )
        
        self._division_configs[division] = metadata
        return metadata
    
    def _get_division_priority_boost(self, division: DivisionType) -> float:
        """Calculate division-specific priority boost factors."""
        
        # Technical priority matrix based on OBINexus organizational structure
        priority_matrix = {
            DivisionType.COMPUTING: 1.2,           # Primary technical division
            DivisionType.UCHE_NNAMDI: 1.5,         # Leadership and strategic projects
            DivisionType.AEGIS_ENGINEERING: 1.3,   # Core engineering projects
            DivisionType.OBIAXIS_RD: 1.1,          # Research and development
            DivisionType.TDA: 1.0,                 # Tactical defense projects
            DivisionType.PUBLISHING: 0.9,          # Documentation and content
            DivisionType.NKWAKOBA: 1.0             # Packaging and presentation
        }
        
        return priority_matrix.get(division, 1.0)
    
    def _normalize_raw_metrics(self, metrics: RepositoryMetrics) -> Dict[str, float]:
        """Systematic normalization of raw GitHub metrics."""
        
        # Temporal adjustment for commit activity
        temporal_weight = self._calculate_temporal_weight(metrics.last_commit_date)
        
        # Normalized metrics with ceiling constraints
        normalized = {
            'stars': min(metrics.stars_count / 1000.0, 1.0),
            'commits': min(metrics.commits_last_30_days / 100.0, 1.0) * temporal_weight,
            'size': min(metrics.size_kb / 50000.0, 1.0),
            'build_time': self._normalize_build_time(metrics.build_time_minutes),
            'test_coverage': (metrics.test_coverage_percent or 0) / 100.0,
            'language_diversity': self._calculate_language_diversity(metrics.languages)
        }
        
        logger.debug(f"Normalized metrics for {metrics.name}: {normalized}")
        return normalized
    
    def _calculate_temporal_weight(self, last_commit: Optional[datetime]) -> float:
        """Calculate temporal decay factor for activity metrics."""
        
        if last_commit is None:
            return 0.5  # Neutral weight for unknown commit dates
        
        days_since_commit = (datetime.utcnow() - last_commit).days
        
        # Exponential decay with configurable factor
        decay = math.exp(-days_since_commit * self.temporal_decay_factor / 365.0)
        return max(0.1, min(1.0, decay))  # Bounded between 0.1 and 1.0
    
    def _normalize_build_time(self, build_time: Optional[float]) -> float:
        """Normalize build time with inverse relationship (faster = better)."""
        
        if build_time is None:
            return 0.5  # Neutral score for unknown build times
        
        # Inverse normalization: longer build times result in lower scores
        normalized = max(0.0, 1.0 - (build_time / 60.0))  # 60 minutes = 0 score
        return min(1.0, normalized)
    
    def _calculate_language_diversity(self, languages: Dict[str, int]) -> float:
        """Calculate language diversity factor using Shannon entropy."""
        
        if not languages or len(languages) <= 1:
            return 0.0
        
        total_bytes = sum(languages.values())
        if total_bytes == 0:
            return 0.0
        
        # Shannon entropy calculation
        entropy = 0.0
        for byte_count in languages.values():
            if byte_count > 0:
                proportion = byte_count / total_bytes
                entropy -= proportion * math.log2(proportion)
        
        # Normalize to 0-1 range (log2(5) ~ 2.32 for reasonable upper bound)
        return min(1.0, entropy / 2.32)
    
    def _calculate_weighted_score(
        self,
        normalized_metrics: Dict[str, float],
        cost_factors: CostFactors,
        division_metadata: DivisionMetadata
    ) -> float:
        """Apply weighted cost factors with division-specific adjustments."""
        
        # Base weighted calculation
        base_score = (
            normalized_metrics['stars'] * cost_factors.stars_weight +
            normalized_metrics['commits'] * cost_factors.commit_activity_weight +
            normalized_metrics['build_time'] * cost_factors.build_time_weight +
            normalized_metrics['size'] * cost_factors.size_weight +
            normalized_metrics['test_coverage'] * cost_factors.test_coverage_weight
        )
        
        # Apply manual boost factor
        boosted_score = base_score * cost_factors.manual_boost
        
        # Apply division priority boost
        final_score = boosted_score * division_metadata.priority_boost
        
        return final_score
    
    def _validate_governance_thresholds(
        self,
        score: float,
        division_metadata: DivisionMetadata,
        repository_name: str
    ) -> List[str]:
        """Systematic governance threshold validation."""
        
        alerts = []
        
        # Governance threshold validation
        if score >= division_metadata.governance_threshold:
            alerts.append(
                f"Governance threshold exceeded: {score:.2f} >= {division_metadata.governance_threshold}"
            )
        
        # Isolation threshold validation
        if score >= division_metadata.isolation_threshold:
            alerts.append(
                f"Isolation threshold exceeded: {score:.2f} >= {division_metadata.isolation_threshold}"
            )
        
        # Architectural reorganization threshold
        if score >= self.architectural_reorganization_threshold:
            alerts.append(
                f"Architectural reorganization required: {score:.2f} >= {self.architectural_reorganization_threshold}"
            )
        
        return alerts
    
    def _assess_sinphase_compliance(
        self,
        metrics: RepositoryMetrics,
        config: RepositoryConfig,
        calculated_score: float
    ) -> List[str]:
        """Assess Sinphas‚ methodology compliance violations."""
        
        violations = []
        
        # Single-pass compilation requirement assessment
        if not config.sinphase_compliance:
            violations.append("Explicit Sinphas‚ non-compliance declared")
        
        # Circular dependency detection (heuristic based on size/complexity)
        if metrics.size_kb > 100000 and calculated_score > 0.8:
            violations.append("Potential circular dependency complexity detected")
        
        # Build system complexity assessment
        if metrics.build_time_minutes and metrics.build_time_minutes > 30:
            violations.append("Build complexity exceeds single-pass threshold")
        
        # Temporal coupling assessment
        if (metrics.commits_last_30_days > 200 and 
            len(config.dependencies) > 10):
            violations.append("High temporal coupling risk detected")
        
        return violations
    
    def _normalize_final_score(self, raw_score: float) -> float:
        """Final score normalization to 0-100 range."""
        
        # Apply ceiling constraint and scale to 0-100
        normalized = min(raw_score, 1.0) * self.normalization_ceiling
        return round(normalized, 1)
    
    def generate_division_summaries(
        self, 
        organization_report: OrganizationCostReport
    ) -> None:
        """Generate systematic division-level aggregation summaries."""
        
        division_data: Dict[DivisionType, List[CostCalculationResult]] = {}
        
        # Group repositories by division
        for result in organization_report.repository_scores:
            if result.division not in division_data:
                division_data[result.division] = []
            division_data[result.division].append(result)
        
        # Calculate division summaries
        for division, repositories in division_data.items():
            if not repositories:
                continue
            
            # Aggregate metrics
            total_repos = len(repositories)
            average_score = sum(r.normalized_score for r in repositories) / total_repos
            governance_violations = sum(len(r.governance_alerts) for r in repositories)
            isolation_candidates = sum(1 for r in repositories if r.requires_isolation)
            
            # Status distribution
            status_distribution = {}
            for status in ProjectStatus:
                count = sum(1 for r in repositories if r.status == status)
                if count > 0:
                    status_distribution[status] = count
            
            # Top repositories (by score)
            top_repos = sorted(repositories, key=lambda r: r.normalized_score, reverse=True)
            top_repo_names = [r.repository for r in top_repos[:5]]
            
            summary = DivisionSummary(
                division=division,
                total_repositories=total_repos,
                average_cost_score=round(average_score, 1),
                status_distribution=status_distribution,
                governance_violations=governance_violations,
                isolation_candidates=isolation_candidates,
                top_repositories=top_repo_names
            )
            
            organization_report.division_summaries[division] = summary
        
        # Calculate global compliance rate
        total_violations = sum(
            len(r.sinphase_violations) for r in organization_report.repository_scores
        )
        total_repos = len(organization_report.repository_scores)
        
        if total_repos > 0:
            compliance_rate = 1.0 - (total_violations / total_repos)
            organization_report.sinphase_compliance_rate = max(0.0, compliance_rate)
        
        logger.info(f"Division summaries generated for {len(division_data)} divisions")


class DivisionConfig:
    """
    Division-specific configuration management following systematic methodology.
    
    Provides centralized configuration for division parameters, governance
    thresholds, and priority boost calculations aligned with OBINexus
    organizational structure.
    """
    
    @staticmethod
    def load_division_configurations() -> Dict[DivisionType, DivisionMetadata]:
        """Load systematic division configurations."""
        
        configurations = {
            DivisionType.COMPUTING: DivisionMetadata(
                division=DivisionType.COMPUTING,
                description="Core technical infrastructure and toolchain development",
                governance_threshold=0.6,
                isolation_threshold=0.8,
                priority_boost=1.2,
                responsible_architect="Nnamdi Michael Okpala"
            ),
            
            DivisionType.UCHE_NNAMDI: DivisionMetadata(
                division=DivisionType.UCHE_NNAMDI,
                description="Strategic leadership and architectural oversight",
                governance_threshold=0.5,
                isolation_threshold=0.7,
                priority_boost=1.5,
                responsible_architect="Nnamdi Michael Okpala"
            ),
            
            DivisionType.AEGIS_ENGINEERING: DivisionMetadata(
                division=DivisionType.AEGIS_ENGINEERING,
                description="Core engineering systems and build orchestration",
                governance_threshold=0.6,
                isolation_threshold=0.8,
                priority_boost=1.3,
                responsible_architect="Aegis Engineering Team"
            ),
            
            DivisionType.OBIAXIS_RD: DivisionMetadata(
                division=DivisionType.OBIAXIS_RD,
                description="Research and development initiatives",
                governance_threshold=0.7,
                isolation_threshold=0.9,
                priority_boost=1.1
            ),
            
            DivisionType.TDA: DivisionMetadata(
                division=DivisionType.TDA,
                description="Tactical defense and security applications",
                governance_threshold=0.6,
                isolation_threshold=0.8,
                priority_boost=1.0
            ),
            
            DivisionType.PUBLISHING: DivisionMetadata(
                division=DivisionType.PUBLISHING,
                description="Documentation and content management",
                governance_threshold=0.7,
                isolation_threshold=0.9,
                priority_boost=0.9
            ),
            
            DivisionType.NKWAKOBA: DivisionMetadata(
                division=DivisionType.NKWAKOBA,
                description="Packaging and presentation systems",
                governance_threshold=0.6,
                isolation_threshold=0.8,
                priority_boost=1.0
            )
        }
        
        return configurations

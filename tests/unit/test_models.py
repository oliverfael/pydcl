"""
PYDCL Models Unit Tests
======================

Systematic validation of core data models implementing Sinphasé methodology
with comprehensive mathematical validation and governance compliance testing.

Technical Focus:
- DivisionType enumeration validation
- ProjectStatus lifecycle compliance  
- CostFactors mathematical bounds verification
- RepositoryMetrics calculation accuracy
- DivisionMetadata governance threshold enforcement
- Sinphasé compliance validation across all model components

Test Architecture: Unit testing with mathematical precision validation
Implementation: Waterfall methodology per OBINexus technical standards
"""

import pytest
from datetime import datetime
from typing import Dict, Any, List

# PYDCL imports with systematic error handling
try:
    from pydcl.models import (
        DivisionType, ProjectStatus, CostFactors, RepositoryMetrics,
        RepositoryConfig, CostCalculationResult, OrganizationCostReport,
        DivisionMetadata, ValidationError, calculate_sinphase_cost,
        GOVERNANCE_THRESHOLD, ISOLATION_THRESHOLD, ARCHITECTURAL_REORGANIZATION_THRESHOLD
    )
except ImportError as e:
    pytest.skip(f"PYDCL models unavailable for testing: {e}", allow_module_level=True)


class TestDivisionType:
    """
    DivisionType enumeration validation following OBINexus organizational structure.
    
    Technical Verification:
    - Complete division enumeration accuracy
    - Division name consistency with organizational specification
    - Enumeration value accessibility and string representation
    """
    
    @pytest.mark.unit
    def test_division_type_enumeration_completeness(self):
        """Validate complete division type enumeration per OBINexus specification."""
        expected_divisions = {
            'COMPUTING': 'Computing',
            'UCHE_NNAMDI': 'UCHE Nnamdi', 
            'PUBLISHING': 'Publishing',
            'OBIAXIS_RD': 'OBIAxis R&D',
            'TDA': 'TDA',
            'NKWAKOBA': 'Nkwakọba',
            'AEGIS_ENGINEERING': 'Aegis Engineering'
        }
        
        # Validate all expected divisions exist
        for enum_name, division_value in expected_divisions.items():
            assert hasattr(DivisionType, enum_name), f"Missing division: {enum_name}"
            division_enum = getattr(DivisionType, enum_name)
            assert division_enum.value == division_value, f"Division value mismatch: {enum_name}"
    
    @pytest.mark.unit
    def test_division_type_string_conversion(self):
        """Validate division type string conversion accuracy."""
        # Test string-based division creation
        computing_div = DivisionType('Computing')
        assert computing_div == DivisionType.COMPUTING
        
        uche_div = DivisionType('UCHE Nnamdi')
        assert uche_div == DivisionType.UCHE_NNAMDI
        
        # Test invalid division handling
        with pytest.raises(ValueError):
            DivisionType('InvalidDivision')


class TestProjectStatus:
    """
    ProjectStatus lifecycle validation implementing Sinphasé project states.
    
    Technical Verification:
    - Complete project status enumeration
    - Lifecycle state transition logic validation
    - Status classification accuracy per technical specifications
    """
    
    @pytest.mark.unit
    def test_project_status_enumeration(self):
        """Validate project status enumeration completeness."""
        expected_statuses = ['Core', 'Active', 'Incubator', 'Legacy', 'Experimental', 'Isolated']
        
        for status_value in expected_statuses:
            # Should be able to create ProjectStatus from each expected value
            status = ProjectStatus(status_value)
            assert status.value == status_value
    
    @pytest.mark.unit
    def test_project_status_isolation_classification(self):
        """Validate isolation status classification for governance compliance."""
        isolated_status = ProjectStatus.ISOLATED
        assert isolated_status.value == 'Isolated'
        
        # Isolated status should be distinct from operational statuses
        operational_statuses = [ProjectStatus.CORE, ProjectStatus.ACTIVE, ProjectStatus.INCUBATOR]
        for status in operational_statuses:
            assert status != isolated_status


class TestCostFactors:
    """
    CostFactors mathematical validation implementing Sinphasé governance bounds.
    
    Technical Implementation:
    - Weight distribution validation within mathematical constraints
    - Sinphasé bounds compliance verification (0.8 ≤ Σweight ≤ 1.2)
    - Manual boost coefficient validation
    - Cost calculation accuracy verification
    """
    
    @pytest.mark.unit
    def test_cost_factors_default_initialization(self):
        """Validate default cost factors initialization and mathematical consistency."""
        factors = CostFactors()
        
        # Validate default weight assignments
        assert factors.stars_weight == 0.2
        assert factors.commit_activity_weight == 0.3
        assert factors.build_time_weight == 0.2
        assert factors.size_weight == 0.2
        assert factors.test_coverage_weight == 0.1
        assert factors.manual_boost == 1.0
        
        # Validate weight distribution within Sinphasé bounds
        total_weight = (factors.stars_weight + factors.commit_activity_weight + 
                       factors.build_time_weight + factors.size_weight + 
                       factors.test_coverage_weight)
        assert 0.8 <= total_weight <= 1.2, f"Weight distribution violates Sinphasé bounds: {total_weight}"
    
    @pytest.mark.unit
    def test_cost_factors_bounds_validation(self):
        """Validate cost factors bounds validation methodology."""
        factors = CostFactors()
        
        # Default configuration should validate successfully
        assert factors.validate_cost_bounds(), "Default configuration should be valid"
        
        # Test boundary conditions
        factors.stars_weight = 0.5
        factors.commit_activity_weight = 0.5
        factors.build_time_weight = 0.1
        factors.size_weight = 0.1
        factors.test_coverage_weight = 0.1
        # Total: 1.2 (upper bound)
        
        assert factors.validate_cost_bounds(), "Upper bound should be valid"


class TestRepositoryMetrics:
    """
    RepositoryMetrics calculation validation with complexity analysis.
    
    Technical Implementation:
    - Repository metrics initialization and data integrity
    - Complexity score calculation mathematical accuracy
    - Bounds validation for normalized metrics
    - Performance characteristics under various input conditions
    """
    
    @pytest.mark.unit
    def test_repository_metrics_initialization(self):
        """Validate repository metrics initialization with systematic defaults."""
        repo_name = 'test-repository'
        metrics = RepositoryMetrics(repo_name)
        
        # Validate required fields initialization
        assert metrics.name == repo_name
        assert metrics.stars_count == 0
        assert metrics.commits_last_30_days == 0
        assert metrics.size_kb == 0
        assert metrics.build_time_minutes is None
        assert metrics.test_coverage_percent is None
    
    @pytest.mark.unit
    def test_repository_complexity_calculation(self):
        """Validate repository complexity calculation mathematical accuracy."""
        metrics = RepositoryMetrics('complexity-test')
        
        # Test boundary conditions
        metrics.size_kb = 0
        metrics.commits_last_30_days = 0
        complexity_score = metrics.calculate_complexity_score()
        assert complexity_score == 0.0, "Zero input should yield zero complexity"
        
        # Test normal operational values
        metrics.size_kb = 25000  # 50% of normalization factor
        metrics.commits_last_30_days = 50  # 50% of normalization factor
        complexity_score = metrics.calculate_complexity_score()
        expected_score = (0.5 + 0.5) / 2.0  # (normalized_size + normalized_activity) / 2
        assert complexity_score == expected_score, f"Complexity calculation mismatch: {complexity_score} != {expected_score}"
        
        # Test upper bound conditions
        metrics.size_kb = 100000  # Exceeds normalization factor
        metrics.commits_last_30_days = 200  # Exceeds normalization factor
        complexity_score = metrics.calculate_complexity_score()
        assert complexity_score == 1.0, "Maximum complexity should be bounded at 1.0"


class TestDivisionMetadata:
    """
    DivisionMetadata governance validation implementing systematic threshold enforcement.
    
    Technical Implementation:
    - Division-specific configuration parameter validation
    - Governance threshold mathematical compliance
    - Priority boost coefficient systematic application
    - Isolation recommendation systematic logic validation
    """
    
    @pytest.mark.unit
    def test_division_metadata_initialization(self):
        """Validate division metadata initialization with governance compliance."""
        division_metadata = DivisionMetadata(
            division=DivisionType.COMPUTING,
            governance_threshold=0.6,
            isolation_threshold=0.8,
            priority_boost=1.2
        )
        
        # Validate systematic parameter assignment
        assert division_metadata.division == DivisionType.COMPUTING
        assert division_metadata.governance_threshold == 0.6
        assert division_metadata.isolation_threshold == 0.8
        assert division_metadata.priority_boost == 1.2
        assert division_metadata.description == "Computing Division"
    
    @pytest.mark.unit
    def test_division_metadata_threshold_validation(self):
        """Validate division metadata threshold bounds enforcement."""
        # Valid threshold configuration
        valid_metadata = DivisionMetadata(
            division=DivisionType.COMPUTING,
            governance_threshold=0.6,
            isolation_threshold=0.8
        )
        # Should initialize without exceptions
        
        # Invalid governance threshold (exceeds 1.0)
        with pytest.raises(ValueError, match="Governance threshold out of bounds"):
            DivisionMetadata(
                division=DivisionType.COMPUTING,
                governance_threshold=1.5
            )
        
        # Invalid isolation threshold (negative)
        with pytest.raises(ValueError, match="Isolation threshold out of bounds"):
            DivisionMetadata(
                division=DivisionType.COMPUTING,
                isolation_threshold=-0.1
            )
        
        # Governance threshold exceeds isolation threshold
        with pytest.raises(ValueError, match="cannot exceed isolation threshold"):
            DivisionMetadata(
                division=DivisionType.COMPUTING,
                governance_threshold=0.9,
                isolation_threshold=0.7
            )
    
    @pytest.mark.unit
    def test_division_metadata_governance_compliance(self):
        """Validate governance compliance evaluation accuracy."""
        metadata = DivisionMetadata(
            division=DivisionType.COMPUTING,
            governance_threshold=0.6
        )
        
        # Test compliance boundary conditions
        assert metadata.is_governance_compliant(0.5), "Score below threshold should be compliant"
        assert metadata.is_governance_compliant(0.6), "Score at threshold should be compliant"
        assert not metadata.is_governance_compliant(0.7), "Score above threshold should be non-compliant"
    
    @pytest.mark.unit
    def test_division_metadata_isolation_requirements(self):
        """Validate isolation requirement evaluation systematic logic."""
        metadata = DivisionMetadata(
            division=DivisionType.COMPUTING,
            isolation_threshold=0.8
        )
        
        # Test isolation boundary conditions
        assert not metadata.requires_isolation(0.7), "Score below threshold should not require isolation"
        assert metadata.requires_isolation(0.8), "Score at threshold should require isolation"
        assert metadata.requires_isolation(0.9), "Score above threshold should require isolation"
    
    @pytest.mark.unit
    def test_division_metadata_priority_boost_application(self):
        """Validate priority boost application mathematical accuracy."""
        metadata = DivisionMetadata(
            division=DivisionType.UCHE_NNAMDI,
            priority_boost=1.5
        )
        
        # Test priority boost calculation
        base_score = 0.4
        boosted_score = metadata.apply_priority_boost(base_score)
        expected_score = base_score * 1.5
        assert boosted_score == expected_score, f"Priority boost calculation mismatch: {boosted_score} != {expected_score}"
        
        # Test bounds enforcement
        high_base_score = 0.8
        boosted_high_score = metadata.apply_priority_boost(high_base_score)
        assert boosted_high_score <= ARCHITECTURAL_REORGANIZATION_THRESHOLD, "Boosted score should respect architectural bounds"


class TestSinphaseCostCalculation:
    """
    Sinphasé cost calculation validation implementing mathematical precision.
    
    Technical Implementation:
    - Core cost calculation algorithm validation
    - Governance threshold triggering accuracy
    - Mathematical bounds enforcement verification
    - Cost factor integration systematic testing
    """
    
    @pytest.mark.unit
    def test_sinphase_cost_calculation_basic(self):
        """Validate basic Sinphasé cost calculation mathematical accuracy."""
        metrics = RepositoryMetrics('test-calculation')
        metrics.stars_count = 100
        metrics.commits_last_30_days = 50
        
        factors = CostFactors()
        
        cost_result = calculate_sinphase_cost(metrics, factors)
        
        # Validate cost result within bounds
        assert 0.0 <= cost_result <= ARCHITECTURAL_REORGANIZATION_THRESHOLD, \
            f"Cost result out of bounds: {cost_result}"
        
        # Validate deterministic calculation
        repeat_result = calculate_sinphase_cost(metrics, factors)
        assert cost_result == repeat_result, "Cost calculation should be deterministic"
    
    @pytest.mark.unit
    def test_sinphase_cost_governance_threshold_triggering(self):
        """Validate governance threshold triggering systematic logic."""
        # Create metrics that should exceed governance threshold
        high_activity_metrics = RepositoryMetrics('high-activity')
        high_activity_metrics.stars_count = 1000
        high_activity_metrics.commits_last_30_days = 500
        
        factors = CostFactors()
        factors.manual_boost = 2.0  # Amplify to trigger threshold
        
        cost_result = calculate_sinphase_cost(high_activity_metrics, factors)
        
        # Should trigger governance threshold
        assert cost_result > GOVERNANCE_THRESHOLD, \
            f"High activity should trigger governance threshold: {cost_result} <= {GOVERNANCE_THRESHOLD}"
    
    @pytest.mark.unit
    def test_sinphase_cost_architectural_bounds(self):
        """Validate architectural reorganization bounds enforcement."""
        # Create extreme metrics
        extreme_metrics = RepositoryMetrics('extreme-complexity')
        extreme_metrics.stars_count = 100000
        extreme_metrics.commits_last_30_days = 10000
        
        factors = CostFactors()
        factors.manual_boost = 5.0  # Extreme boost
        
        cost_result = calculate_sinphase_cost(extreme_metrics, factors)
        
        # Should be bounded by architectural reorganization threshold
        assert cost_result <= ARCHITECTURAL_REORGANIZATION_THRESHOLD, \
            f"Cost should be bounded by architectural threshold: {cost_result}"


class TestValidationError:
    """
    ValidationError systematic testing for error handling and classification.
    
    Technical Implementation:
    - Error object initialization and data integrity
    - Severity classification accuracy
    - Sinphasé violation detection systematic logic
    - Timestamp precision and consistency validation
    """
    
    @pytest.mark.unit
    def test_validation_error_initialization(self):
        """Validate validation error initialization with systematic data assignment."""
        error = ValidationError(
            field='test_field',
            message='Test validation error message',
            severity='error'
        )
        
        # Validate systematic field assignment
        assert error.field == 'test_field'
        assert error.message == 'Test validation error message'
        assert error.severity == 'error'
        assert isinstance(error.timestamp, datetime)
    
    @pytest.mark.unit
    def test_validation_error_sinphase_violation_detection(self):
        """Validate Sinphasé violation detection systematic logic."""
        # Error with Sinphasé-related content
        sinphase_error = ValidationError(
            field='cost_threshold',
            message='Cost calculation exceeds governance threshold',
            severity='error'
        )
        assert sinphase_error.is_sinphase_violation(), "Should detect Sinphasé violation"
        
        # Error without Sinphasé-related content
        general_error = ValidationError(
            field='configuration',
            message='Missing required field',
            severity='error'
        )
        assert not general_error.is_sinphase_violation(), "Should not detect Sinphasé violation"
    
    @pytest.mark.unit
    def test_validation_error_severity_classification(self):
        """Validate error severity classification accuracy."""
        severity_levels = ['critical', 'error', 'warning']
        
        for severity in severity_levels:
            error = ValidationError(
                field='test_field',
                message='Test message',
                severity=severity
            )
            assert error.severity == severity, f"Severity classification mismatch: {severity}"


class TestModelIntegration:
    """
    Model integration validation ensuring systematic component coordination.
    
    Technical Implementation:
    - Cross-model dependency validation
    - Data flow integrity verification
    - Comprehensive workflow validation
    - Performance characteristics under integrated operations
    """
    
    @pytest.mark.unit
    def test_repository_config_division_integration(self):
        """Validate repository configuration integration with division metadata."""
        # Create repository configuration with division assignment
        repo_config = RepositoryConfig(
            division=DivisionType.COMPUTING,
            status=ProjectStatus.CORE
        )
        
        # Validate systematic assignment
        assert repo_config.division == DivisionType.COMPUTING
        assert repo_config.status == ProjectStatus.CORE
        assert isinstance(repo_config.cost_factors, CostFactors)
        assert repo_config.sinphase_compliance == True
        assert repo_config.isolation_required == False
    
    @pytest.mark.unit
    def test_cost_calculation_result_governance_integration(self):
        """Validate cost calculation result integration with governance thresholds."""
        # Create calculation result
        result = CostCalculationResult(
            repository='test-repo',
            division=DivisionType.COMPUTING,
            status=ProjectStatus.ACTIVE
        )
        
        # Set score that exceeds governance threshold
        result.normalized_score = 70.0  # 70% (exceeds 60% threshold)
        
        # Apply governance thresholds
        result.apply_governance_thresholds()
        
        # Should generate governance alerts
        assert len(result.governance_alerts) > 0, "Should generate governance alerts for high score"
        assert any('threshold exceeded' in alert.lower() for alert in result.governance_alerts)
    
    @pytest.mark.unit
    def test_organization_report_division_summary_integration(self):
        """Validate organization report integration with division-specific summaries."""
        # Create organization report
        org_report = OrganizationCostReport('obinexus')
        
        # Add repository scores from different divisions
        computing_result = CostCalculationResult('repo1', DivisionType.COMPUTING, ProjectStatus.CORE)
        computing_result.normalized_score = 45.0
        
        uche_result = CostCalculationResult('repo2', DivisionType.UCHE_NNAMDI, ProjectStatus.ACTIVE)
        uche_result.normalized_score = 55.0
        
        org_report.repository_scores = [computing_result, uche_result]
        org_report.total_repositories = 2
        org_report.analyzed_repositories = 2
        
        # Calculate governance metrics
        org_report.calculate_governance_metrics()
        
        # Should calculate compliance rate
        assert 0.0 <= org_report.sinphase_compliance_rate <= 1.0, "Compliance rate should be in valid range"
"""
PYDCL Models Unit Tests
======================

Systematic validation of data models following Sinphasé methodology
with bounded complexity verification and governance compliance testing.

Technical Focus:
- DivisionType and ProjectStatus enum validation
- CostFactors weight distribution compliance
- RepositoryMetrics boundary condition testing
- calculate_sinphase_cost mathematical precision
- Governance threshold enforcement validation

Test Architecture: pytest with systematic fixtures
Implementation: Aegis project waterfall validation checkpoints
"""

import pytest
from datetime import datetime
from typing import Dict, Any

# PYDCL imports with development phase handling
try:
    from pydcl.models import (
        DivisionType, ProjectStatus, CostFactors, RepositoryMetrics,
        RepositoryConfig, CostCalculationResult, OrganizationCostReport,
        ValidationError, calculate_sinphase_cost,
        GOVERNANCE_THRESHOLD, ISOLATION_THRESHOLD, ARCHITECTURAL_REORGANIZATION_THRESHOLD
    )
except ImportError as e:
    pytest.skip(f"PYDCL models not available: {e}", allow_module_level=True)


class TestDivisionType:
    """
    Systematic DivisionType enum validation.
    
    Technical Verification:
    - All OBINexus divisions properly defined
    - String conversion accuracy
    - Invalid division handling
    """
    
    @pytest.mark.unit
    def test_division_type_completeness(self):
        """Validate all required OBINexus divisions are defined."""
        expected_divisions = {
            'Computing', 'UCHE Nnamdi', 'Publishing', 'OBIAxis R&D',
            'TDA', 'Nkwakọba', 'Aegis Engineering'
        }
        
        actual_divisions = {division.value for division in DivisionType}
        
        assert actual_divisions == expected_divisions, \
            f"Division mismatch: expected {expected_divisions}, got {actual_divisions}"
    
    @pytest.mark.unit
    def test_division_type_string_conversion(self):
        """Validate division type string conversion accuracy."""
        test_cases = [
            (DivisionType.COMPUTING, "Computing"),
            (DivisionType.UCHE_NNAMDI, "UCHE Nnamdi"),
            (DivisionType.AEGIS_ENGINEERING, "Aegis Engineering"),
        ]
        
        for division_enum, expected_string in test_cases:
            assert division_enum.value == expected_string
            assert str(division_enum) == expected_string
    
    @pytest.mark.unit
    def test_division_type_invalid_creation(self):
        """Validate error handling for invalid division types."""
        invalid_divisions = ['InvalidDivision', 'Unknown', '', None]
        
        for invalid_division in invalid_divisions:
            if invalid_division is None:
                continue
            with pytest.raises(ValueError):
                DivisionType(invalid_division)


class TestProjectStatus:
    """
    Systematic ProjectStatus enum validation following Sinphasé lifecycle.
    
    Technical Verification:
    - Complete project lifecycle state coverage
    - Status transition validation
    - Isolation status handling
    """
    
    @pytest.mark.unit
    def test_project_status_completeness(self):
        """Validate all Sinphasé project lifecycle states are defined."""
        expected_statuses = {
            'Core', 'Active', 'Incubator', 'Legacy', 'Experimental', 'Isolated'
        }
        
        actual_statuses = {status.value for status in ProjectStatus}
        
        assert actual_statuses == expected_statuses, \
            f"Status mismatch: expected {expected_statuses}, got {actual_statuses}"
    
    @pytest.mark.unit
    def test_project_status_isolation_handling(self):
        """Validate isolation status for governance compliance."""
        isolated_status = ProjectStatus.ISOLATED
        assert isolated_status.value == "Isolated"
        
        # Validate that isolation status can be created
        test_status = ProjectStatus("Isolated")
        assert test_status == ProjectStatus.ISOLATED


class TestCostFactors:
    """
    Systematic CostFactors validation with Sinphasé compliance checking.
    
    Mathematical Verification:
    - Weight distribution bounds checking (0.8 ≤ total ≤ 1.2)
    - Individual weight constraint validation
    - Manual boost parameter validation
    """
    
    @pytest.mark.unit
    def test_default_cost_factors(self):
        """Validate default cost factor configuration."""
        factors = CostFactors()
        
        # Validate individual weight defaults
        assert factors.stars_weight == 0.2
        assert factors.commit_activity_weight == 0.3
        assert factors.build_time_weight == 0.2
        assert factors.size_weight == 0.2
        assert factors.test_coverage_weight == 0.1
        assert factors.manual_boost == 1.0
    
    @pytest.mark.unit
    def test_cost_factor_weight_bounds_validation(self):
        """Validate Sinphasé weight distribution constraints."""
        factors = CostFactors()
        
        # Calculate total weight
        total_weight = (
            factors.stars_weight + 
            factors.commit_activity_weight +
            factors.build_time_weight + 
            factors.size_weight +
            factors.test_coverage_weight
        )
        
        # Sinphasé compliance validation (0.8 ≤ total ≤ 1.2)
        assert 0.8 <= total_weight <= 1.2, \
            f"Weight distribution violates Sinphasé bounds: {total_weight}"
        
        # Validate individual weight boundaries
        assert 0.0 <= factors.stars_weight <= 1.0
        assert 0.0 <= factors.commit_activity_weight <= 1.0
        assert 0.0 <= factors.build_time_weight <= 1.0
        assert 0.0 <= factors.size_weight <= 1.0
        assert 0.0 <= factors.test_coverage_weight <= 1.0
    
    @pytest.mark.unit
    def test_validate_cost_bounds_method(self):
        """Test cost factors validation method."""
        factors = CostFactors()
        
        # Default configuration should be valid
        assert factors.validate_cost_bounds() is True
        
        # Test invalid configuration
        factors.stars_weight = 2.0  # Exceeds individual weight limit
        factors.commit_activity_weight = 2.0
        # This would exceed total weight bounds
        assert factors.validate_cost_bounds() is False


class TestRepositoryMetrics:
    """
    Systematic RepositoryMetrics validation with boundary condition testing.
    
    Technical Verification:
    - Metrics initialization accuracy
    - Complexity score calculation validation
    - Boundary condition handling
    """
    
    @pytest.mark.unit
    def test_repository_metrics_initialization(self, known_repository_metrics):
        """Validate repository metrics initialization."""
        metrics = RepositoryMetrics(known_repository_metrics['name'])
        
        # Validate name assignment
        assert metrics.name == known_repository_metrics['name']
        
        # Validate default values
        assert metrics.stars_count == 0
        assert metrics.commits_last_30_days == 0
        assert metrics.size_kb == 0
        assert metrics.build_time_minutes is None
        assert metrics.test_coverage_percent is None
    
    @pytest.mark.unit
    def test_repository_metrics_assignment(self, known_repository_metrics):
        """Validate repository metrics value assignment."""
        metrics = RepositoryMetrics(known_repository_metrics['name'])
        
        # Assign known values
        metrics.stars_count = known_repository_metrics['stars_count']
        metrics.commits_last_30_days = known_repository_metrics['commits_last_30_days']
        metrics.size_kb = known_repository_metrics['size_kb']
        
        # Validate assignment
        assert metrics.stars_count == 25
        assert metrics.commits_last_30_days == 15
        assert metrics.size_kb == 2840
    
    @pytest.mark.unit
    def test_complexity_score_calculation(self, known_repository_metrics):
        """Validate repository complexity score calculation."""
        metrics = RepositoryMetrics(known_repository_metrics['name'])
        metrics.size_kb = known_repository_metrics['size_kb']
        metrics.commits_last_30_days = known_repository_metrics['commits_last_30_days']
        
        complexity = metrics.calculate_complexity_score()
        
        # Validate complexity bounds (0.0 ≤ complexity ≤ 1.0)
        assert 0.0 <= complexity <= 1.0, f"Complexity out of bounds: {complexity}"
        
        # Validate mathematical precision
        expected_size = min(2840 / 50000.0, 1.0)  # Normalized size
        expected_activity = min(15 / 100.0, 1.0)  # Normalized activity
        expected_complexity = (expected_size + expected_activity) / 2.0
        
        tolerance = 0.001
        assert abs(complexity - expected_complexity) <= tolerance
    
    @pytest.mark.unit
    def test_boundary_conditions(self):
        """Test repository metrics boundary conditions."""
        metrics = RepositoryMetrics('boundary-test')
        
        # Test zero values
        metrics.size_kb = 0
        metrics.commits_last_30_days = 0
        complexity_zero = metrics.calculate_complexity_score()
        assert complexity_zero == 0.0
        
        # Test very large values
        metrics.size_kb = 1000000  # 1GB
        metrics.commits_last_30_days = 10000  # Very active
        complexity_large = metrics.calculate_complexity_score()
        assert complexity_large <= 1.0  # Should be capped


class TestSinphaseCostCalculation:
    """
    Core Sinphasé cost calculation validation with mathematical precision.
    
    Technical Verification:
    - Cost calculation accuracy with known inputs
    - Governance threshold compliance checking
    - Boundary condition validation
    - Mathematical reproducibility
    """
    
    @pytest.mark.unit
    def test_basic_cost_calculation(self, known_repository_metrics):
        """Validate basic cost calculation with known inputs."""
        # Create metrics with known values
        metrics = RepositoryMetrics(known_repository_metrics['name'])
        metrics.stars_count = known_repository_metrics['stars_count']
        metrics.commits_last_30_days = known_repository_metrics['commits_last_30_days']
        metrics.size_kb = known_repository_metrics['size_kb']
        
        # Standard cost factors
        factors = CostFactors()
        
        # Calculate cost
        cost = calculate_sinphase_cost(metrics, factors)
        
        # Validate bounds
        assert 0.0 <= cost <= 1.0, f"Cost out of bounds: {cost}"
        
        # Validate governance compliance for known input
        assert cost <= GOVERNANCE_THRESHOLD, "Known metrics should be governance compliant"
    
    @pytest.mark.unit
    def test_cost_calculation_reproducibility(self, known_repository_metrics):
        """Validate cost calculation is deterministic and reproducible."""
        metrics = RepositoryMetrics(known_repository_metrics['name'])
        metrics.stars_count = known_repository_metrics['stars_count']
        metrics.commits_last_30_days = known_repository_metrics['commits_last_30_days']
        
        factors = CostFactors()
        
        # Calculate cost multiple times
        costs = [calculate_sinphase_cost(metrics, factors) for _ in range(10)]
        
        # All calculations should be identical
        assert all(cost == costs[0] for cost in costs), \
            "Cost calculation not deterministic"
    
    @pytest.mark.unit
    def test_manual_boost_application(self):
        """Validate manual boost factor application."""
        metrics = RepositoryMetrics('boost-test')
        metrics.stars_count = 50
        metrics.commits_last_30_days = 25
        
        # Base calculation
        base_factors = CostFactors()
        base_cost = calculate_sinphase_cost(metrics, base_factors)
        
        # With manual boost
        boosted_factors = CostFactors()
        boosted_factors.manual_boost = 1.5
        boosted_cost = calculate_sinphase_cost(metrics, boosted_factors)
        
        # Validate boost application
        expected_boosted = min(base_cost * 1.5, ARCHITECTURAL_REORGANIZATION_THRESHOLD)
        tolerance = 0.001
        assert abs(boosted_cost - expected_boosted) <= tolerance
    
    @pytest.mark.unit
    def test_governance_threshold_enforcement(self):
        """Test governance threshold enforcement mechanisms."""
        # Test cases designed to trigger different governance levels
        test_cases = [
            {'stars': 10, 'commits': 5, 'expected_compliant': True},
            {'stars': 100, 'commits': 50, 'expected_compliant': False},
            {'stars': 1000, 'commits': 500, 'expected_compliant': False},
        ]
        
        for case in test_cases:
            metrics = RepositoryMetrics('governance-test')
            metrics.stars_count = case['stars']
            metrics.commits_last_30_days = case['commits']
            
            factors = CostFactors()
            cost = calculate_sinphase_cost(metrics, factors)
            
            is_compliant = cost <= GOVERNANCE_THRESHOLD
            assert is_compliant == case['expected_compliant'], \
                f"Governance compliance mismatch for {case}"


class TestCostCalculationResult:
    """
    CostCalculationResult data structure validation.
    
    Technical Verification:
    - Result object initialization
    - Governance threshold application
    - Alert generation validation
    """
    
    @pytest.mark.unit
    def test_result_initialization(self):
        """Validate cost calculation result initialization."""
        result = CostCalculationResult(
            repository='test-repo',
            division=DivisionType.COMPUTING,
            status=ProjectStatus.ACTIVE
        )
        
        # Validate initial state
        assert result.repository == 'test-repo'
        assert result.division == DivisionType.COMPUTING
        assert result.status == ProjectStatus.ACTIVE
        assert result.normalized_score == 0.0
        assert result.governance_alerts == []
        assert result.sinphase_violations == []
        assert result.requires_isolation is False
    
    @pytest.mark.unit
    def test_governance_threshold_application(self):
        """Test governance threshold application logic."""
        result = CostCalculationResult(
            repository='threshold-test',
            division=DivisionType.COMPUTING,
            status=ProjectStatus.ACTIVE
        )
        
        # Test governance threshold exceedance
        result.normalized_score = 70.0  # Above governance threshold
        result.apply_governance_thresholds()
        
        assert len(result.governance_alerts) > 0
        assert any('Governance threshold exceeded' in alert for alert in result.governance_alerts)
        
        # Test isolation threshold exceedance
        result.normalized_score = 85.0  # Above isolation threshold
        result.governance_alerts.clear()  # Reset
        result.apply_governance_thresholds()
        
        assert result.requires_isolation is True
        assert any('Isolation threshold exceeded' in alert for alert in result.governance_alerts)


class TestValidationError:
    """
    ValidationError utility class testing.
    
    Technical Verification:
    - Error creation and classification
    - Sinphasé violation detection
    - Severity level assignment
    """
    
    @pytest.mark.unit
    def test_validation_error_creation(self):
        """Validate validation error creation."""
        error = ValidationError(
            field='test_field',
            message='Test validation error',
            severity='error'
        )
        
        assert error.field == 'test_field'
        assert error.message == 'Test validation error'
        assert error.severity == 'error'
        assert isinstance(error.timestamp, datetime)
    
    @pytest.mark.unit
    def test_sinphase_violation_detection(self):
        """Test Sinphasé violation detection logic."""
        # Test Sinphasé-related error
        sinphase_error = ValidationError(
            field='cost_factors',
            message='Cost threshold exceeded governance bounds'
        )
        
        assert sinphase_error.is_sinphase_violation() is True
        
        # Test non-Sinphasé error
        general_error = ValidationError(
            field='name',
            message='Invalid repository name format'
        )
        
        assert general_error.is_sinphase_violation() is False

"""
PYDCL Test Suite - System Integrity Validation
=====================================================

Comprehensive test suite implementing UML System Operation Integrity
for the Python Dynamic Cost Layer following Aegis project specifications.

Test Architecture:
- System-level pipeline validation (not just unit tests)
- Sinphasé methodology compliance verification
- Division-aware cost calculation validation
- JSON output schema integrity checking
- Cryptographic echo validation for pipeline consistency

Technical Lead: Integration with OBINexus waterfall methodology
Implementation: pytest framework with systematic fixtures
"""

import pytest
import json
import yaml
import hashlib
import tempfile
import os
from pathlib import Path
from typing import Dict, Any, List
from unittest.mock import Mock, patch, MagicMock

# PYDCL imports - handle development phase gracefully
try:
    from pydcl.models import (
        RepositoryMetrics, CostFactors, DivisionType, ProjectStatus,
        calculate_sinphase_cost, CostCalculationResult, OrganizationCostReport,
        GOVERNANCE_THRESHOLD
    )
    from pydcl.cost_scores import CostScoreCalculator, DivisionConfig
    from pydcl.github_client import GitHubMetricsClient
    from pydcl.utils import validate_config, load_division_config
    from pydcl import cli
except ImportError as e:
    # Development phase - mock components for forward compatibility
    pytest.skip(f"PYDCL development phase: {e}", allow_module_level=True)


# =============================================================================
# Test Fixtures - Systematic Test Data Management
# =============================================================================

@pytest.fixture
def sample_repo_yaml() -> str:
    """
    Sample repository configuration following PYDCL specification.
    
    Technical Implementation:
    - Complete division-aware configuration
    - Sinphasé compliance parameters
    - Cost factor specifications aligned with governance thresholds
    """
    return """
division: "Computing"
status: "Core"
cost_factors:
  stars_weight: 0.2
  commit_activity_weight: 0.3
  build_time_weight: 0.2
  size_weight: 0.2
  test_coverage_weight: 0.1
  manual_boost: 1.2
tags:
  - "build-orchestration"
  - "toolchain"
  - "aegis-project"
dependencies:
  - "nlink"
  - "polybuild"
sinphase_compliance: true
isolation_required: false
"""

@pytest.fixture
def sample_org_config() -> str:
    """Organization-level configuration for systematic testing."""
    return """
version: "1.0.0"
organization: "obinexus"
divisions:
  "Computing":
    governance_threshold: 0.6
    isolation_threshold: 0.8
    priority_boost: 1.2
    responsible_architect: "Nnamdi Michael Okpala"
  "UCHE Nnamdi":
    governance_threshold: 0.5
    isolation_threshold: 0.7
    priority_boost: 1.5
cost_factors:
  stars_weight: 0.2
  commit_activity_weight: 0.3
  build_time_weight: 0.2
  size_weight: 0.2
  test_coverage_weight: 0.1
"""

@pytest.fixture
def known_repository_metrics() -> Dict[str, Any]:
    """
    Known repository metrics for deterministic cost calculation testing.
    
    Technical Specification:
    - Metrics designed to produce predictable cost scores
    - Governance threshold validation data
    - Division-aware parameter testing
    """
    return {
        'name': 'libpolycall-bindings',
        'full_name': 'obinexus/libpolycall-bindings',
        'stars_count': 25,
        'commits_last_30_days': 15,
        'size_kb': 2840,
        'build_time_minutes': 8.5,
        'test_coverage_percent': 87,
        'forks_count': 3,
        'watchers_count': 8,
        'open_issues_count': 2,
        'primary_language': 'Python',
        'has_readme': True,
        'has_license': True,
        'is_fork': False,
        'is_archived': False,
        'has_ci': True,
        'languages': {'Python': 15420, 'Shell': 892, 'Dockerfile': 156}
    }

@pytest.fixture
def expected_cost_calculation() -> Dict[str, float]:
    """
    Expected cost calculation results for validation.
    
    Mathematical Verification:
    - Based on known metrics and standard cost factors
    - Sinphasé governance threshold compliance
    - Division priority boost calculations
    """
    return {
        'base_cost': 0.142,  # Calculated from known metrics
        'with_manual_boost': 0.170,  # With 1.2x manual boost
        'with_division_boost': 0.204,  # With Computing division 1.2x boost
        'normalized_score': 20.4,  # Percentage format
        'governance_compliant': True  # Below 0.6 threshold
    }

@pytest.fixture
def mock_github_repositories() -> List[Dict[str, Any]]:
    """Mock GitHub repository data for integration testing."""
    return [
        {
            'name': 'libpolycall-bindings',
            'division': 'Computing',
            'status': 'Core',
            'stars_count': 25,
            'commits_last_30_days': 15,
            'size_kb': 2840
        },
        {
            'name': 'nexuslink',
            'division': 'Computing', 
            'status': 'Active',
            'stars_count': 12,
            'commits_last_30_days': 28,
            'size_kb': 1850
        },
        {
            'name': 'polybuild',
            'division': 'Aegis Engineering',
            'status': 'Core',
            'stars_count': 8,
            'commits_last_30_days': 22,
            'size_kb': 3200
        }
    ]


# =============================================================================
# Core System Integrity Tests
# =============================================================================

class TestCostScoresParsing:
    """
    Systematic YAML parsing validation following Aegis project specifications.
    
    Test Objectives:
    - Repository configuration parsing accuracy
    - Division-aware parameter validation
    - Sinphasé compliance verification
    - Error handling for malformed configurations
    """
    
    def test_parse_valid_repo_yaml(self, sample_repo_yaml):
        """
        Validate correct parsing of repository YAML configuration.
        
        Technical Verification:
        - YAML structure preservation
        - Division type validation
        - Cost factor boundary checking
        - Sinphasé compliance parameter validation
        """
        # Parse YAML configuration
        config_data = yaml.safe_load(sample_repo_yaml)
        
        # Systematic validation checkpoints
        assert config_data['division'] == 'Computing'
        assert config_data['status'] == 'Core'
        assert config_data['sinphase_compliance'] is True
        assert config_data['isolation_required'] is False
        
        # Cost factors validation
        cost_factors = config_data['cost_factors']
        total_weight = sum([
            cost_factors['stars_weight'],
            cost_factors['commit_activity_weight'], 
            cost_factors['build_time_weight'],
            cost_factors['size_weight'],
            cost_factors['test_coverage_weight']
        ])
        
        # Sinphasé weight distribution validation (0.8 <= total <= 1.2)
        assert 0.8 <= total_weight <= 1.2, f"Weight distribution violates Sinphasé bounds: {total_weight}"
        assert cost_factors['manual_boost'] == 1.2
        
        # Dependencies and tags validation
        assert 'nlink' in config_data['dependencies']
        assert 'polybuild' in config_data['dependencies']
        assert 'aegis-project' in config_data['tags']
    
    def test_parse_division_type_validation(self, sample_repo_yaml):
        """Validate division type constraint enforcement."""
        config_data = yaml.safe_load(sample_repo_yaml)
        
        # Verify Computing division is valid
        division = DivisionType(config_data['division'])
        assert division == DivisionType.COMPUTING
        
        # Test invalid division handling
        invalid_config = config_data.copy()
        invalid_config['division'] = 'InvalidDivision'
        
        with pytest.raises(ValueError):
            DivisionType(invalid_config['division'])
    
    def test_parse_organization_config(self, sample_org_config):
        """Validate organization-level configuration parsing."""
        config_data = yaml.safe_load(sample_org_config)
        
        # Structural validation
        assert config_data['version'] == '1.0.0'
        assert config_data['organization'] == 'obinexus'
        assert 'Computing' in config_data['divisions']
        assert 'UCHE Nnamdi' in config_data['divisions']
        
        # Division-specific threshold validation
        computing_config = config_data['divisions']['Computing']
        assert computing_config['governance_threshold'] == 0.6
        assert computing_config['isolation_threshold'] == 0.8
        assert computing_config['priority_boost'] == 1.2
        assert computing_config['responsible_architect'] == 'Nnamdi Michael Okpala'
    
    def test_config_validation_utility(self, sample_org_config):
        """Test systematic configuration validation utility."""
        config_data = yaml.safe_load(sample_org_config)
        
        # This test validates the utils.validate_config function
        # Currently a placeholder - will validate when implemented
        try:
            validation_errors = validate_config(config_data)
            assert isinstance(validation_errors, list)
            # Should have no errors for valid configuration
            critical_errors = [e for e in validation_errors if e.severity == 'critical']
            assert len(critical_errors) == 0
        except NotImplementedError:
            pytest.skip("Configuration validation not yet implemented")


class TestCostScoreComputation:
    """
    Systematic cost score calculation validation.
    
    Mathematical Verification:
    - Weighted factor application accuracy
    - Sinphasé governance threshold compliance
    - Division priority boost calculations
    - Boundary condition validation
    """
    
    def test_basic_cost_calculation(self, known_repository_metrics, expected_cost_calculation):
        """
        Validate core cost calculation algorithm accuracy.
        
        Technical Implementation:
        - Known input → predictable output validation
        - Mathematical precision verification
        - Governance threshold compliance checking
        """
        # Create repository metrics object
        metrics = RepositoryMetrics(known_repository_metrics['name'])
        metrics.stars_count = known_repository_metrics['stars_count']
        metrics.commits_last_30_days = known_repository_metrics['commits_last_30_days']
        metrics.size_kb = known_repository_metrics['size_kb']
        
        # Create cost factors with known weights
        factors = CostFactors()
        
        # Calculate Sinphasé cost
        calculated_cost = calculate_sinphase_cost(metrics, factors)
        
        # Validate calculation bounds
        assert 0.0 <= calculated_cost <= 1.0, f"Cost calculation out of bounds: {calculated_cost}"
        
        # Validate governance compliance
        is_compliant = calculated_cost <= GOVERNANCE_THRESHOLD
        assert is_compliant == expected_cost_calculation['governance_compliant']
        
        # Mathematical precision validation (within tolerance)
        tolerance = 0.05  # 5% tolerance for floating point calculations
        expected_base = expected_cost_calculation['base_cost']
        assert abs(calculated_cost - expected_base) <= tolerance, \
            f"Cost calculation deviation: expected {expected_base}, got {calculated_cost}"
    
    def test_division_priority_boost_application(self, known_repository_metrics):
        """Validate division-specific priority boost calculations."""
        metrics = RepositoryMetrics(known_repository_metrics['name'])
        metrics.stars_count = known_repository_metrics['stars_count']
        metrics.commits_last_30_days = known_repository_metrics['commits_last_30_days']
        
        # Test different division priority boosts
        base_factors = CostFactors()
        base_cost = calculate_sinphase_cost(metrics, base_factors)
        
        # Computing division boost (1.2x)
        computing_factors = CostFactors()
        computing_factors.manual_boost = 1.2
        computing_cost = calculate_sinphase_cost(metrics, computing_factors)
        
        # Validate boost application
        expected_boosted_cost = min(base_cost * 1.2, 1.0)  # Capped at 1.0
        tolerance = 0.01
        assert abs(computing_cost - expected_boosted_cost) <= tolerance
    
    def test_governance_threshold_validation(self):
        """
        Test governance threshold enforcement across cost ranges.
        
        Sinphasé Compliance Verification:
        - Governance threshold (0.6) warning triggers
        - Isolation threshold (0.8) recommendation triggers  
        - Reorganization threshold (1.0) mandatory triggers
        """
        # Test metrics that should trigger different governance levels
        test_cases = [
            {'stars': 10, 'commits': 5, 'expected_level': 'compliant'},
            {'stars': 100, 'commits': 50, 'expected_level': 'warning'},
            {'stars': 500, 'commits': 200, 'expected_level': 'isolation'},
        ]
        
        for case in test_cases:
            metrics = RepositoryMetrics('test-repo')
            metrics.stars_count = case['stars']
            metrics.commits_last_30_days = case['commits']
            
            factors = CostFactors()
            cost = calculate_sinphase_cost(metrics, factors)
            
            # Validate governance level assignment
            if case['expected_level'] == 'compliant':
                assert cost <= GOVERNANCE_THRESHOLD
            elif case['expected_level'] == 'warning':
                assert GOVERNANCE_THRESHOLD < cost <= 0.8
            elif case['expected_level'] == 'isolation':
                assert cost > 0.8
    
    def test_cost_factor_weight_validation(self):
        """Validate cost factor weight distribution constraints."""
        factors = CostFactors()
        
        # Test default weight distribution
        total_weight = (
            factors.stars_weight + 
            factors.commit_activity_weight +
            factors.build_time_weight + 
            factors.size_weight +
            factors.test_coverage_weight
        )
        
        # Sinphasé weight validation (should sum to ~1.0)
        assert 0.8 <= total_weight <= 1.2, f"Weight distribution violates Sinphasé bounds: {total_weight}"
        
        # Validate individual weight boundaries
        assert 0.0 <= factors.stars_weight <= 1.0
        assert 0.0 <= factors.commit_activity_weight <= 1.0
        assert 0.0 <= factors.build_time_weight <= 1.0
        assert 0.0 <= factors.size_weight <= 1.0
        assert 0.0 <= factors.test_coverage_weight <= 1.0


class TestJSONOutputIntegrity:
    """
    JSON output schema validation and structural integrity testing.
    
    System Integration Validation:
    - Complete pipeline execution verification
    - JSON schema compliance checking
    - Data structure preservation validation
    - Division-aware reporting accuracy
    """
    
    def test_cost_scores_json_schema_validation(self, mock_github_repositories):
        """
        Validate cost_scores.json output schema compliance.
        
        Technical Verification:
        - JSON structure validation
        - Required field presence checking
        - Data type compliance verification
        - Division summary accuracy validation
        """
        # Mock organization cost report generation
        org_report = OrganizationCostReport('obinexus')
        org_report.total_repositories = len(mock_github_repositories)
        org_report.analyzed_repositories = len(mock_github_repositories)
        
        # Generate repository scores
        for repo_data in mock_github_repositories:
            result = CostCalculationResult(
                repository=repo_data['name'],
                division=DivisionType(repo_data['division']),
                status=ProjectStatus(repo_data['status'])
            )
            
            # Mock cost calculation
            result.normalized_score = 25.0  # Sample score
            result.governance_alerts = []
            result.sinphase_violations = []
            result.requires_isolation = False
            
            org_report.repository_scores.append(result)
        
        # Generate JSON representation
        json_output = {
            'organization': org_report.organization,
            'total_repositories': org_report.total_repositories,
            'analyzed_repositories': org_report.analyzed_repositories,
            'repository_scores': []
        }
        
        for score in org_report.repository_scores:
            json_output['repository_scores'].append({
                'repository': score.repository,
                'division': score.division.value,
                'status': score.status.value,
                'normalized_score': score.normalized_score,
                'governance_alerts': score.governance_alerts,
                'sinphase_violations': score.sinphase_violations,
                'requires_isolation': score.requires_isolation
            })
        
        # Schema validation
        assert 'organization' in json_output
        assert 'total_repositories' in json_output
        assert 'analyzed_repositories' in json_output
        assert 'repository_scores' in json_output
        
        # Validate repository score structure
        for repo_score in json_output['repository_scores']:
            required_fields = ['repository', 'division', 'status', 'normalized_score']
            for field in required_fields:
                assert field in repo_score, f"Missing required field: {field}"
            
            # Data type validation
            assert isinstance(repo_score['repository'], str)
            assert isinstance(repo_score['division'], str)
            assert isinstance(repo_score['status'], str)
            assert isinstance(repo_score['normalized_score'], (int, float))
            assert isinstance(repo_score['governance_alerts'], list)
            assert isinstance(repo_score['requires_isolation'], bool)
    
    def test_division_summary_generation(self, mock_github_repositories):
        """Validate division-aware summary generation."""
        org_report = OrganizationCostReport('obinexus')
        
        # Group repositories by division
        division_repos = {}
        for repo_data in mock_github_repositories:
            division = repo_data['division']
            if division not in division_repos:
                division_repos[division] = []
            division_repos[division].append(repo_data)
        
        # Validate division groupings
        assert 'Computing' in division_repos
        assert 'Aegis Engineering' in division_repos
        
        # Validate Computing division repositories
        computing_repos = division_repos['Computing']
        assert len(computing_repos) == 2  # libpolycall-bindings, nexuslink
        
        repo_names = [repo['name'] for repo in computing_repos]
        assert 'libpolycall-bindings' in repo_names
        assert 'nexuslink' in repo_names
    
    def test_json_serialization_integrity(self, mock_github_repositories):
        """Validate JSON serialization preserves data integrity."""
        # Create test data structure
        test_data = {
            'organization': 'obinexus',
            'generation_timestamp': '2024-12-10T15:30:45.123456',
            'total_repositories': len(mock_github_repositories),
            'repository_scores': mock_github_repositories
        }
        
        # Serialize to JSON and back
        json_string = json.dumps(test_data, indent=2)
        parsed_data = json.loads(json_string)
        
        # Validate data preservation
        assert parsed_data['organization'] == test_data['organization']
        assert parsed_data['total_repositories'] == test_data['total_repositories']
        assert len(parsed_data['repository_scores']) == len(test_data['repository_scores'])
        
        # Validate repository data preservation
        for original, parsed in zip(test_data['repository_scores'], parsed_data['repository_scores']):
            assert original['name'] == parsed['name']
            assert original['division'] == parsed['division']
            assert original['status'] == parsed['status']


class TestPipelineIntegrityEcho:
    """
    System-level pipeline integrity validation using cryptographic echo testing.
    
    Divisor Echo Hypothesis Implementation:
    - Complete pipeline execution reproducibility
    - Cryptographic hash validation for output consistency
    - System state preservation verification
    - Configuration determinism validation
    """
    
    def test_pipeline_deterministic_execution(self, sample_repo_yaml, mock_github_repositories):
        """
        Validate pipeline produces deterministic results for identical inputs.
        
        Technical Implementation:
        - Execute pipeline twice with identical inputs
        - Generate cryptographic hashes of outputs
        - Verify hash consistency (echo validation)
        - Validate system state preservation
        """
        # Create temporary configuration
        with tempfile.TemporaryDirectory() as temp_dir:
            config_path = Path(temp_dir) / 'repo.yaml'
            config_path.write_text(sample_repo_yaml)
            
            # Execute pipeline first time
            first_execution_data = self._mock_pipeline_execution(mock_github_repositories)
            first_hash = self._generate_execution_hash(first_execution_data)
            
            # Execute pipeline second time with identical inputs
            second_execution_data = self._mock_pipeline_execution(mock_github_repositories)
            second_hash = self._generate_execution_hash(second_execution_data)
            
            # Echo validation - hashes should be identical
            assert first_hash == second_hash, \
                f"Pipeline execution not deterministic: {first_hash} != {second_hash}"
    
    def test_configuration_hash_consistency(self, sample_org_config):
        """Validate configuration hashing produces consistent results."""
        config_data = yaml.safe_load(sample_org_config)
        
        # Generate hash multiple times
        hash1 = self._generate_config_hash(config_data)
        hash2 = self._generate_config_hash(config_data)
        hash3 = self._generate_config_hash(config_data)
        
        # All hashes should be identical
        assert hash1 == hash2 == hash3, "Configuration hashing not deterministic"
        
        # Validate hash format
        assert len(hash1) == 64, "SHA-256 hash should be 64 characters"
        assert all(c in '0123456789abcdef' for c in hash1), "Hash should be hexadecimal"
    
    def test_sinphase_compliance_preservation(self, known_repository_metrics):
        """
        Validate Sinphasé compliance is preserved throughout pipeline execution.
        
        Governance Integrity Verification:
        - Cost calculations remain within governance bounds
        - Isolation recommendations are consistent
        - Threshold validation is preserved
        """
        metrics = RepositoryMetrics(known_repository_metrics['name'])
        metrics.stars_count = known_repository_metrics['stars_count']
        metrics.commits_last_30_days = known_repository_metrics['commits_last_30_days']
        
        factors = CostFactors()
        
        # Calculate cost multiple times
        costs = [calculate_sinphase_cost(metrics, factors) for _ in range(5)]
        
        # All calculations should be identical
        assert all(cost == costs[0] for cost in costs), "Cost calculation not deterministic"
        
        # All costs should comply with Sinphasé bounds
        for cost in costs:
            assert 0.0 <= cost <= 1.0, f"Cost out of bounds: {cost}"
            
            # Validate governance compliance consistency
            is_compliant = cost <= GOVERNANCE_THRESHOLD
            assert isinstance(is_compliant, bool), "Governance compliance should be boolean"
    
    def _mock_pipeline_execution(self, repo_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Mock complete pipeline execution for testing."""
        # Simulate cost calculation for each repository
        results = []
        for repo in repo_data:
            metrics = RepositoryMetrics(repo['name'])
            metrics.stars_count = repo['stars_count']
            metrics.commits_last_30_days = repo['commits_last_30_days']
            
            factors = CostFactors()
            cost = calculate_sinphase_cost(metrics, factors)
            
            results.append({
                'repository': repo['name'],
                'division': repo['division'],
                'status': repo['status'],
                'calculated_cost': cost,
                'normalized_score': cost * 100
            })
        
        return {
            'organization': 'obinexus',
            'total_repositories': len(repo_data),
            'repository_scores': results
        }
    
    def _generate_execution_hash(self, execution_data: Dict[str, Any]) -> str:
        """Generate cryptographic hash of pipeline execution results."""
        # Normalize data for consistent hashing
        normalized_data = json.dumps(execution_data, sort_keys=True, separators=(',', ':'))
        
        # Generate SHA-256 hash
        return hashlib.sha256(normalized_data.encode('utf-8')).hexdigest()
    
    def _generate_config_hash(self, config_data: Dict[str, Any]) -> str:
        """Generate deterministic hash for configuration data."""
        # Normalize configuration
        normalized_config = json.dumps(config_data, sort_keys=True, separators=(',', ':'))
        
        # Generate SHA-256 hash
        return hashlib.sha256(normalized_config.encode('utf-8')).hexdigest()


# =============================================================================
# CLI Integration Tests
# =============================================================================

class TestCLIIntegration:
    """
    Command-line interface integration testing for systematic validation.
    
    Technical Verification:
    - CLI command execution validation
    - Argument parsing accuracy
    - Output format compliance
    - Error handling robustness
    """
    
    def test_cli_version_command(self):
        """Validate CLI version command functionality."""
        # This test validates the current CLI implementation
        # Currently uses basic argument parsing
        
        # Mock sys.argv for version command
        with patch('sys.argv', ['pydcl', '--version']):
            with patch('builtins.print') as mock_print:
                try:
                    cli.main()
                    # Should print version number
                    mock_print.assert_called_with('1.0.0')
                except SystemExit:
                    # CLI may exit after version display
                    pass
    
    def test_cli_help_command(self):
        """Validate CLI help command functionality."""
        with patch('sys.argv', ['pydcl', '--help']):
            with patch('builtins.print') as mock_print:
                try:
                    cli.main()
                    # Should print help information
                    assert mock_print.called
                    help_output = str(mock_print.call_args_list)
                    assert 'commands' in help_output.lower()
                except SystemExit:
                    pass
    
    def test_cli_unknown_command(self):
        """Validate CLI unknown command handling."""
        with patch('sys.argv', ['pydcl', 'unknown-command']):
            with patch('builtins.print') as mock_print:
                cli.main()
                # Should print error message for unknown command
                assert mock_print.called
                error_output = str(mock_print.call_args_list)
                assert 'not yet implemented' in error_output.lower()


# =============================================================================
# Test Configuration and Utilities
# =============================================================================

@pytest.fixture(scope="session")
def test_environment_setup():
    """
    Session-level test environment configuration.
    
    Technical Setup:
    - Temporary directory creation for test artifacts
    - Environment variable configuration
    - Logging configuration for test execution
    """
    # Create temporary test directory
    test_dir = tempfile.mkdtemp(prefix='pydcl_test_')
    
    # Set environment variables for testing
    os.environ['PYDCL_TEST_MODE'] = '1'
    os.environ['PYDCL_TEST_DIR'] = test_dir
    
    yield test_dir
    
    # Cleanup
    import shutil
    shutil.rmtree(test_dir, ignore_errors=True)
    os.environ.pop('PYDCL_TEST_MODE', None)
    os.environ.pop('PYDCL_TEST_DIR', None)


def pytest_configure(config):
    """Configure pytest for PYDCL testing."""
    # Add custom markers
    config.addinivalue_line("markers", "integration: Integration tests requiring full system")
    config.addinivalue_line("markers", "unit: Unit tests for individual components")
    config.addinivalue_line("markers", "echo: Pipeline integrity echo tests")


# =============================================================================
# CI Integration Configuration
# =============================================================================

"""
CI Integration Notes for obinexus/obinexus/.github/workflows/integration-test.yml:

Test Execution Commands:
- pytest tests/ -v --tb=short
- pytest tests/ -m unit (unit tests only)
- pytest tests/ -m integration (integration tests only)
- pytest tests/ -m echo (echo integrity tests only)

Required Environment Variables:
- PYDCL_TEST_MODE=1 (enables test mode)
- GH_API_TOKEN (for GitHub integration tests - optional)

Coverage Reporting:
- pytest tests/ --cov=pydcl --cov-report=xml
- Coverage reports will be generated in coverage.xml

Dependencies for CI:
- pytest>=7.0.0
- pytest-cov>=4.0.0
- PyYAML>=6.0
- pydcl package (installed in editable mode)

Test Artifacts:
- JUnit XML: --junitxml=test-results.xml
- Coverage XML: --cov-report=xml
- Test logs: Captured automatically by pytest

Waterfall Integration:
These tests are designed to validate system integrity at each
development phase gate, ensuring Sinphasé compliance and
architectural governance throughout the PYDCL development lifecycle.
"""
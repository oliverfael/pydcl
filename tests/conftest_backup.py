"""
PYDCL Test Configuration - Shared Fixtures
==========================================

Centralized test fixtures and configuration following Aegis project
waterfall methodology with systematic validation checkpoints.

Technical Architecture:
- Session-level configuration management
- Shared test data fixtures for deterministic testing
- Environment setup for CI/CD integration
- Mock data generation for systematic validation

Implementation: pytest fixtures with scope management
Technical Lead: Integration with OBINexus testing framework
"""

import pytest
import tempfile
import os
import yaml
import json
from pathlib import Path
from typing import Dict, Any, List
import shutil

# =============================================================================
# Session-Level Configuration
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
    shutil.rmtree(test_dir, ignore_errors=True)
    os.environ.pop('PYDCL_TEST_MODE', None)
    os.environ.pop('PYDCL_TEST_DIR', None)


def pytest_configure(config):
    """Configure pytest for PYDCL testing with custom markers."""
    # Add custom markers for test categorization
    config.addinivalue_line("markers", "unit: Unit tests for individual components")
    config.addinivalue_line("markers", "integration: Integration tests requiring full system")
    config.addinivalue_line("markers", "echo: Pipeline integrity echo tests")
    config.addinivalue_line("markers", "cli: Command-line interface tests")
    config.addinivalue_line("markers", "slow: Tests that take significant time to execute")


# =============================================================================
# Configuration Fixtures
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
  "Aegis Engineering":
    governance_threshold: 0.6
    isolation_threshold: 0.8
    priority_boost: 1.3
cost_factors:
  stars_weight: 0.2
  commit_activity_weight: 0.3
  build_time_weight: 0.2
  size_weight: 0.2
  test_coverage_weight: 0.1
"""

@pytest.fixture
def invalid_repo_yaml() -> str:
    """Invalid repository configuration for error handling testing."""
    return """
division: "InvalidDivision"
status: "InvalidStatus" 
cost_factors:
  stars_weight: 1.5  # Invalid: exceeds 1.0
  total_weight_violation: 3.0  # Invalid: would exceed Sinphasé bounds
sinphase_compliance: "not_boolean"  # Invalid: should be boolean
"""

# =============================================================================
# Repository Metrics Fixtures
# =============================================================================

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
def high_cost_repository_metrics() -> Dict[str, Any]:
    """Repository metrics designed to trigger governance thresholds."""
    return {
        'name': 'high-complexity-repo',
        'full_name': 'obinexus/high-complexity-repo',
        'stars_count': 500,  # High activity
        'commits_last_30_days': 200,  # Very active
        'size_kb': 50000,  # Large repository
        'build_time_minutes': 45.0,  # Long build time
        'test_coverage_percent': 45,  # Lower coverage
        'forks_count': 25,
        'watchers_count': 150,
        'open_issues_count': 30,
        'primary_language': 'C++',
        'has_readme': True,
        'has_license': True,
        'is_fork': False,
        'is_archived': False,
        'has_ci': True,
        'languages': {'C++': 45000, 'Python': 3000, 'CMake': 2000}
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

# =============================================================================
# Mock GitHub Data Fixtures
# =============================================================================

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
        },
        {
            'name': 'experimental-feature',
            'division': 'UCHE Nnamdi',
            'status': 'Experimental',
            'stars_count': 3,
            'commits_last_30_days': 5,
            'size_kb': 450
        }
    ]

@pytest.fixture
def mock_organization_data() -> Dict[str, Any]:
    """Mock GitHub organization data for testing."""
    return {
        'login': 'obinexus',
        'name': 'OBINexus Computing',
        'description': 'Advanced computing infrastructure and toolchain development',
        'public_repos': 42,
        'total_private_repos': 8,
        'owned_private_repos': 8,
        'private_gists': 0,
        'disk_usage': 125000,
        'collaborators': 12,
        'billing_email': 'support@obinexuscomputing.com',
        'plan': 'team'
    }

# =============================================================================
# File System Fixtures
# =============================================================================

@pytest.fixture
def temp_config_dir(test_environment_setup):
    """Create temporary configuration directory with sample files."""
    config_dir = Path(test_environment_setup) / 'config'
    config_dir.mkdir(exist_ok=True)
    
    # Create sample configuration files
    repo_config = config_dir / 'repo.yaml'
    org_config = config_dir / '.github' / 'pydcl.yaml'
    org_config.parent.mkdir(exist_ok=True)
    
    yield config_dir
    
    # Cleanup handled by session fixture

@pytest.fixture
def mock_git_repository(temp_config_dir, sample_repo_yaml):
    """Create mock git repository structure with configuration."""
    repo_dir = temp_config_dir / 'mock_repo'
    repo_dir.mkdir()
    
    # Create .github directory and configuration
    github_dir = repo_dir / '.github'
    github_dir.mkdir()
    
    repo_config_path = github_dir / 'repo.yaml'
    repo_config_path.write_text(sample_repo_yaml)
    
    # Create README and other standard files
    (repo_dir / 'README.md').write_text('# Mock Repository\n\nTest repository for PYDCL validation.')
    (repo_dir / 'LICENSE').write_text('MIT License\n\nCopyright (c) 2024 OBINexus Computing')
    (repo_dir / 'pyproject.toml').write_text('[build-system]\nrequires = ["setuptools"]\n')
    
    return repo_dir

# =============================================================================
# CLI Testing Fixtures
# =============================================================================

@pytest.fixture
def mock_cli_args():
    """Standard CLI arguments for testing."""
    return {
        'version': ['pydcl', '--version'],
        'help': ['pydcl', '--help'],
        'analyze_basic': ['pydcl', 'analyze', '--org', 'obinexus'],
        'analyze_division': ['pydcl', 'analyze', '--org', 'obinexus', '--division', 'Computing'],
        'analyze_output': ['pydcl', 'analyze', '--org', 'obinexus', '--output', 'cost_scores.json'],
        'init_config': ['pydcl', 'init', '--template', 'enterprise'],
        'display_results': ['pydcl', 'display', '--input', 'cost_scores.json', '--format', 'table']
    }

# =============================================================================
# Validation Fixtures
# =============================================================================

@pytest.fixture
def expected_json_schema() -> Dict[str, Any]:
    """Expected JSON schema for cost_scores.json validation."""
    return {
        'type': 'object',
        'required': ['organization', 'total_repositories', 'analyzed_repositories', 'repository_scores'],
        'properties': {
            'organization': {'type': 'string'},
            'generation_timestamp': {'type': 'string'},
            'total_repositories': {'type': 'integer', 'minimum': 0},
            'analyzed_repositories': {'type': 'integer', 'minimum': 0},
            'sinphase_compliance_rate': {'type': 'number', 'minimum': 0.0, 'maximum': 1.0},
            'division_summaries': {'type': 'object'},
            'repository_scores': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'required': ['repository', 'division', 'status', 'normalized_score'],
                    'properties': {
                        'repository': {'type': 'string'},
                        'division': {'type': 'string'},
                        'status': {'type': 'string'},
                        'calculated_score': {'type': 'number', 'minimum': 0.0, 'maximum': 1.0},
                        'normalized_score': {'type': 'number', 'minimum': 0.0, 'maximum': 100.0},
                        'governance_alerts': {'type': 'array'},
                        'sinphase_violations': {'type': 'array'},
                        'requires_isolation': {'type': 'boolean'}
                    }
                }
            }
        }
    }

# =============================================================================
# Performance Testing Fixtures
# =============================================================================

@pytest.fixture
def performance_test_data() -> Dict[str, Any]:
    """Large dataset for performance testing."""
    return {
        'large_organization_repos': [
            {
                'name': f'repo_{i:03d}',
                'division': ['Computing', 'Aegis Engineering', 'UCHE Nnamdi'][i % 3],
                'status': ['Core', 'Active', 'Experimental'][i % 3],
                'stars_count': (i * 7) % 100,
                'commits_last_30_days': (i * 3) % 50,
                'size_kb': (i * 100) % 10000
            }
            for i in range(100)  # Large test dataset
        ]
    }

# =============================================================================
# Error Handling Fixtures
# =============================================================================

@pytest.fixture
def github_api_error_responses():
    """Mock GitHub API error responses for testing error handling."""
    return {
        'rate_limit_exceeded': {
            'status_code': 403,
            'message': 'API rate limit exceeded',
            'documentation_url': 'https://docs.github.com/rest/overview/resources-in-the-rest-api#rate-limiting'
        },
        'repository_not_found': {
            'status_code': 404,
            'message': 'Not Found',
            'documentation_url': 'https://docs.github.com/rest'
        },
        'organization_access_denied': {
            'status_code': 403,
            'message': 'Organization access denied',
            'documentation_url': 'https://docs.github.com/rest/orgs'
        },
        'invalid_token': {
            'status_code': 401,
            'message': 'Bad credentials',
            'documentation_url': 'https://docs.github.com/rest'
        }
    }
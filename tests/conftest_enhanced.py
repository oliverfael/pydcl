#!/usr/bin/env python3
"""
PYDCL Test Environment Enforcement
==================================

Systematic test environment validation and virtual environment enforcement
following Aegis project waterfall methodology standards.

Technical Implementation:
- Virtual environment validation with systematic checks
- Test dependency verification and isolation
- Mock infrastructure standardization
- GitHub API client mock configuration
- Test data fixture standardization

Architecture: Test infrastructure with deterministic execution
Technical Lead: Nnamdi Michael Okpala - OBINexus Computing
"""

import os
import sys
import subprocess
import venv
from pathlib import Path
from typing import Dict, List, Optional, Any
import pytest
from unittest.mock import Mock, MagicMock, patch


def enforce_virtual_environment() -> bool:
    """
    Enforce virtual environment execution for test isolation.
    
    Technical Implementation:
    - Detect current virtual environment status
    - Validate PYDCL dependencies availability
    - Ensure test isolation from system packages
    - Generate activation warnings for non-venv execution
    
    Returns:
        Boolean indicating successful venv validation
    """
    
    # Check if running in virtual environment
    in_venv = (
        hasattr(sys, 'real_prefix') or 
        (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)
    )
    
    if not in_venv:
        print("=" * 70)
        print("PYDCL TEST ENVIRONMENT VIOLATION")
        print("=" * 70)
        print("Tests must be executed within a virtual environment for proper isolation.")
        print("Please activate your virtual environment before running tests:")
        print()
        print("  python -m venv pydcl_test_env")
        print("  source pydcl_test_env/bin/activate  # Linux/macOS")
        print("  # or")
        print("  pydcl_test_env\\Scripts\\activate.bat  # Windows")
        print()
        print("Then install test dependencies:")
        print("  pip install -e .")
        print("  pip install pytest pytest-cov pytest-mock")
        print("=" * 70)
        return False
    
    # Validate critical test dependencies
    required_packages = [
        'pytest', 'pytest-cov', 'pytest-mock', 'PyGithub', 
        'PyYAML', 'pydantic', 'click', 'rich'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_').lower())
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"Missing test dependencies: {', '.join(missing_packages)}")
        print("Install with: pip install " + " ".join(missing_packages))
        return False
    
    print(f"✓ Virtual environment validated: {sys.prefix}")
    return True


def create_standardized_github_mock() -> Mock:
    """
    Create standardized GitHub API mock with comprehensive attribute coverage.
    
    Technical Implementation:
    - Complete repository mock with all required attributes
    - Organization mock with systematic pagination support
    - Rate limiting mock with realistic behavior simulation
    - Commit and content mocks for metrics extraction
    
    Returns:
        Configured GitHub API mock for systematic testing
    """
    
    # Create comprehensive repository mock
    mock_repo = Mock()
    
    # Basic repository attributes
    mock_repo.name = "test-repository"
    mock_repo.full_name = "obinexus/test-repository"
    mock_repo.stargazers_count = 25
    mock_repo.forks_count = 3
    mock_repo.watchers_count = 8
    mock_repo.size = 2840
    mock_repo.open_issues_count = 2
    mock_repo.language = "Python"
    mock_repo.fork = False
    mock_repo.archived = False
    mock_repo.private = False
    
    # License mock
    mock_license = Mock()
    mock_license.name = "MIT License"
    mock_repo.license = mock_license
    
    # Timestamps
    from datetime import datetime, timedelta
    mock_repo.created_at = datetime.utcnow() - timedelta(days=365)
    mock_repo.updated_at = datetime.utcnow() - timedelta(days=1)
    mock_repo.pushed_at = datetime.utcnow() - timedelta(hours=6)
    
    # Commits mock with pagination support
    mock_commits = Mock()
    mock_commits.totalCount = 15
    mock_commits.__iter__ = lambda self: iter([Mock() for _ in range(15)])
    mock_commits.__getitem__ = lambda self, idx: Mock()
    mock_repo.get_commits = Mock(return_value=mock_commits)
    
    # Languages mock
    mock_repo.get_languages = Mock(return_value={
        'Python': 15420, 
        'Shell': 892, 
        'Dockerfile': 156
    })
    
    # Contents mock for README and CI detection
    mock_readme = Mock()
    mock_readme.name = "README.md"
    mock_readme.type = "file"
    
    mock_setup = Mock()
    mock_setup.name = "setup.py"
    mock_setup.type = "file"
    
    mock_repo.get_contents = Mock(return_value=[mock_readme, mock_setup])
    
    # Organization mock
    mock_org = Mock()
    mock_org.name = "OBINexus Computing"
    mock_org.login = "obinexus"
    mock_org.public_repos = 4
    mock_org.get_repos = Mock(return_value=[mock_repo])
    
    # GitHub client mock
    mock_github = Mock()
    mock_github.get_organization = Mock(return_value=mock_org)
    mock_github.get_repo = Mock(return_value=mock_repo)
    
    # User mock for authentication
    mock_user = Mock()
    mock_user.login = "test-user"
    mock_github.get_user = Mock(return_value=mock_user)
    
    # Rate limit mock
    mock_rate_limit = Mock()
    mock_rate_limit.core.remaining = 5000
    mock_rate_limit.core.limit = 5000
    mock_rate_limit.core.reset = datetime.utcnow() + timedelta(hours=1)
    mock_github.get_rate_limit = Mock(return_value=mock_rate_limit)
    
    return mock_github


def setup_pydcl_test_fixtures() -> Dict[str, Any]:
    """
    Setup comprehensive PYDCL test fixtures for systematic testing.
    
    Technical Implementation:
    - Repository metrics test data generation
    - Division configuration test scenarios
    - Cost calculation validation datasets
    - Governance threshold test cases
    
    Returns:
        Dictionary of standardized test fixtures
    """
    
    fixtures = {
        'sample_repositories': [
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
                'stars_count': 18,
                'commits_last_30_days': 35,
                'size_kb': 3200
            }
        ],
        
        'division_configs': {
            'Computing': {
                'governance_threshold': 0.6,
                'isolation_threshold': 0.8,
                'priority_boost': 1.2
            },
            'UCHE Nnamdi': {
                'governance_threshold': 0.5,
                'isolation_threshold': 0.7,
                'priority_boost': 1.5
            },
            'Aegis Engineering': {
                'governance_threshold': 0.6,
                'isolation_threshold': 0.8,
                'priority_boost': 1.3
            }
        },
        
        'cost_calculation_scenarios': [
            {
                'scenario': 'baseline_compliance',
                'stars_count': 50,
                'commits_last_30_days': 25,
                'size_kb': 5000,
                'expected_score_range': (15.0, 25.0),
                'governance_compliant': True
            },
            {
                'scenario': 'governance_threshold',
                'stars_count': 200,
                'commits_last_30_days': 150,
                'size_kb': 25000,
                'expected_score_range': (55.0, 70.0),
                'governance_compliant': False
            },
            {
                'scenario': 'isolation_candidate',
                'stars_count': 500,
                'commits_last_30_days': 300,
                'size_kb': 50000,
                'expected_score_range': (75.0, 90.0),
                'governance_compliant': False
            }
        ]
    }
    
    return fixtures


def patch_github_imports() -> None:
    """
    Systematically patch GitHub-related imports for testing isolation.
    
    Technical Implementation:
    - Mock PyGithub module imports
    - Provide fallback implementations for missing components
    - Ensure test execution continues with proper mocking
    """
    
    try:
        import github
        from github import Github, Repository, Organization
        from github.GithubException import GithubException, RateLimitExceededException
    except ImportError:
        # Create mock GitHub module structure
        github_mock = Mock()
        
        # Mock exception classes
        class MockGithubException(Exception):
            def __init__(self, status, message):
                self.status = status
                self.message = message
                super().__init__(f"{status}: {message}")
        
        class MockRateLimitExceededException(MockGithubException):
            pass
        
        # Inject mocks into sys.modules
        sys.modules['github'] = github_mock
        sys.modules['github.GithubException'] = Mock()
        
        # Configure mock attributes
        github_mock.Github = Mock
        github_mock.Repository = Mock
        github_mock.Organization = Mock
        github_mock.GithubException = MockGithubException
        github_mock.RateLimitExceededException = MockRateLimitExceededException


def configure_test_logging() -> None:
    """Configure systematic test logging for debugging and validation."""
    
    import logging
    
    # Configure test-specific logging
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s | %(name)-20s | %(levelname)-8s | %(message)s',
        datefmt='%H:%M:%S'
    )
    
    # Suppress verbose third-party logging
    logging.getLogger('urllib3').setLevel(logging.WARNING)
    logging.getLogger('github').setLevel(logging.WARNING)
    
    # Configure PYDCL-specific loggers
    logging.getLogger('pydcl').setLevel(logging.DEBUG)
    
    print("✓ Test logging configured for systematic debugging")


def run_systematic_test_validation() -> bool:
    """
    Execute systematic test environment validation.
    
    Technical Implementation:
    - Virtual environment enforcement
    - Dependency validation
    - Mock infrastructure setup
    - Test fixture preparation
    
    Returns:
        Boolean indicating successful test environment setup
    """
    
    print("PYDCL Test Environment Validation - Aegis Project")
    print("=" * 60)
    
    # Phase 1: Virtual Environment Enforcement
    print("Phase 1: Virtual Environment Validation...")
    if not enforce_virtual_environment():
        return False
    
    # Phase 2: Import and Mock Setup
    print("Phase 2: GitHub API Mock Configuration...")
    patch_github_imports()
    
    # Phase 3: Test Infrastructure
    print("Phase 3: Test Infrastructure Setup...")
    configure_test_logging()
    
    # Phase 4: Fixture Preparation
    print("Phase 4: Test Fixture Generation...")
    fixtures = setup_pydcl_test_fixtures()
    print(f"✓ {len(fixtures)} test fixture categories prepared")
    
    print("=" * 60)
    print("✓ PYDCL test environment validation completed successfully")
    print("Execute tests with: pytest tests/ -v --tb=short")
    print("=" * 60)
    
    return True


# Test execution hook for pytest
def pytest_configure(config):
    """Pytest configuration hook for systematic test setup."""
    
    if not run_systematic_test_validation():
        pytest.exit("Test environment validation failed", returncode=1)


# Mock patch decorators for systematic testing
def mock_github_client(func):
    """Decorator for GitHub client mocking in tests."""
    
    def wrapper(*args, **kwargs):
        mock_github = create_standardized_github_mock()
        
        with patch('pydcl.github_client.Github', return_value=mock_github):
            with patch('github.Github', return_value=mock_github):
                return func(*args, **kwargs)
    
    return wrapper


def mock_cost_calculator(func):
    """Decorator for cost calculator mocking in tests."""
    
    def wrapper(*args, **kwargs):
        mock_calculator = Mock()
        mock_calculator.calculate_repository_cost.return_value = {
            'normalized_score': 25.0,
            'governance_alerts': [],
            'sinphase_violations': [],
            'requires_isolation': False
        }
        
        with patch('pydcl.cost_scores.CostScoreCalculator', return_value=mock_calculator):
            return func(*args, **kwargs)
    
    return wrapper


if __name__ == "__main__":
    """Direct execution for test environment validation."""
    
    success = run_systematic_test_validation()
    sys.exit(0 if success else 1)

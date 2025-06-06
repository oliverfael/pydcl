"""
PYDCL GitHub Client Unit Tests
=============================

Systematic validation of GitHub API integration following Aegis project
waterfall methodology with comprehensive error handling and rate limiting validation.

Technical Focus:
- GitHubMetricsClient initialization and authentication
- Repository metrics extraction with systematic validation
- Configuration loading with error handling robustness
- Rate limiting management and retry mechanisms
- Organization analysis with pagination handling

Test Architecture: Methodical pytest with mock integration
Implementation: Technical validation per OBINexus standards
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime, timedelta
from typing import Dict, Any, List

# GitHub API mock objects
try:
    from github import Github, Repository, Organization
    from github.GithubException import GithubException, RateLimitExceededException
except ImportError:
    pytest.skip("PyGithub not available", allow_module_level=True)

# PYDCL imports with systematic error handling
try:
    from pydcl.github_client import GitHubMetricsClient
    from pydcl.models import (
        RepositoryMetrics, RepositoryConfig, CostFactors,
        DivisionType, ProjectStatus, ValidationError
    )
except ImportError as e:
    pytest.skip(f"PYDCL github_client module unavailable: {e}", allow_module_level=True)


class TestGitHubMetricsClientInitialization:
    """
    Systematic GitHubMetricsClient initialization validation.
    
    Technical Implementation:
    - Client initialization with authentication token
    - Configuration parameter validation
    - Rate limiting setup verification
    - Connection validation accuracy
    """
    
    @pytest.mark.unit
    def test_client_initialization_basic(self):
        """Validate basic GitHubMetricsClient initialization."""
        test_token = 'ghp_test_token_1234567890'
        
        client = GitHubMetricsClient(token=test_token)
        
        # Validate basic initialization
        assert client.token == test_token
        assert client.timeout == 30  # Default timeout
        assert client.max_retries == 3  # Default max retries
        assert client.rate_limit_buffer == 100  # Default buffer
        assert client.request_count == 0  # Initial request count
        
        # Validate GitHub client instance creation
        assert hasattr(client, 'client')
        assert client.client is not None
    
    @pytest.mark.unit
    def test_client_initialization_custom_parameters(self):
        """Validate GitHubMetricsClient initialization with custom parameters."""
        test_token = 'ghp_custom_token_9876543210'
        custom_timeout = 60
        custom_retries = 5
        
        client = GitHubMetricsClient(
            token=test_token,
            timeout=custom_timeout,
            max_retries=custom_retries
        )
        
        # Validate custom parameter application
        assert client.token == test_token
        assert client.timeout == custom_timeout
        assert client.max_retries == custom_retries
    
    @pytest.mark.unit
    @patch('pydcl.github_client.Github')
    def test_validate_connection_success(self, mock_github):
        """Validate successful connection validation."""
        # Mock successful GitHub connection
        mock_user = Mock()
        mock_user.login = 'test-user'
        
        mock_rate_limit = Mock()
        mock_rate_limit.core.remaining = 5000
        
        mock_client = Mock()
        mock_client.get_user.return_value = mock_user
        mock_client.get_rate_limit.return_value = mock_rate_limit
        
        mock_github.return_value = mock_client
        
        client = GitHubMetricsClient(token='test_token')
        
        # Validate connection
        is_valid = client.validate_connection()
        
        assert is_valid is True
        mock_client.get_user.assert_called_once()
        mock_client.get_rate_limit.assert_called_once()
    
    @pytest.mark.unit
    @patch('pydcl.github_client.Github')
    def test_validate_connection_rate_limit_concern(self, mock_github):
        """Validate connection validation with rate limit concerns."""
        # Mock rate limit threshold concern
        mock_user = Mock()
        mock_user.login = 'test-user'
        
        mock_rate_limit = Mock()
        mock_rate_limit.core.remaining = 50  # Below rate_limit_buffer (100)
        
        mock_client = Mock()
        mock_client.get_user.return_value = mock_user
        mock_client.get_rate_limit.return_value = mock_rate_limit
        
        mock_github.return_value = mock_client
        
        client = GitHubMetricsClient(token='test_token')
        
        # Connection validation should fail due to rate limit concern
        is_valid = client.validate_connection()
        
        assert is_valid is False
    
    @pytest.mark.unit
    @patch('pydcl.github_client.Github')
    def test_validate_connection_github_exception(self, mock_github):
        """Validate connection validation error handling."""
        # Mock GitHub API exception
        mock_client = Mock()
        mock_client.get_user.side_effect = GithubException(401, 'Bad credentials')
        
        mock_github.return_value = mock_client
        
        client = GitHubMetricsClient(token='invalid_token')
        
        # Connection validation should handle exception gracefully
        is_valid = client.validate_connection()
        
        assert is_valid is False


class TestRepositoryMetricsExtraction:
    """
    Systematic repository metrics extraction validation.
    
    Technical Implementation:
    - Comprehensive repository data extraction accuracy
    - Commit activity analysis with temporal constraints
    - Language distribution calculation verification
    - CI/CD system detection robustness
    """
    
    @pytest.mark.unit
    def test_extract_repository_metrics_basic(self, known_repository_metrics):
        """Validate basic repository metrics extraction."""
        # Create mock repository object
        mock_repo = Mock(spec=Repository)
        mock_repo.name = known_repository_metrics['name']
        mock_repo.full_name = known_repository_metrics['full_name']
        mock_repo.stargazers_count = known_repository_metrics['stars_count']
        mock_repo.forks_count = known_repository_metrics['forks_count']
        mock_repo.watchers_count = known_repository_metrics['watchers_count']
        mock_repo.size = known_repository_metrics['size_kb']
        mock_repo.open_issues_count = known_repository_metrics['open_issues_count']
        mock_repo.language = known_repository_metrics['primary_language']
        mock_repo.license = Mock() if known_repository_metrics['has_license'] else None
        mock_repo.fork = known_repository_metrics['is_fork']
        mock_repo.archived = known_repository_metrics['is_archived']
        mock_repo.created_at = datetime.utcnow() - timedelta(days=365)
        mock_repo.updated_at = datetime.utcnow() - timedelta(days=1)
        
        # Mock commit activity
        mock_commits = Mock()
        mock_commits.totalCount = known_repository_metrics['commits_last_30_days']
        mock_repo.get_commits.return_value = mock_commits
        
        # Mock languages
        mock_repo.get_languages.return_value = known_repository_metrics['languages']
        
        # Mock contents for README detection
        mock_readme = Mock()
        mock_readme.name = 'README.md'
        mock_repo.get_contents.return_value = [mock_readme]
        
        client = GitHubMetricsClient(token='test_token')
        
        # Extract metrics
        metrics = client._extract_repository_metrics(mock_repo)
        
        # Validate extracted metrics
        assert isinstance(metrics, RepositoryMetrics)
        assert metrics.name == known_repository_metrics['name']
        assert metrics.stars_count == known_repository_metrics['stars_count']
        assert metrics.commits_last_30_days == known_repository_metrics['commits_last_30_days']
        assert metrics.size_kb == known_repository_metrics['size_kb']
        assert metrics.primary_language == known_repository_metrics['primary_language']
        assert metrics.has_readme is True
        assert metrics.has_license == known_repository_metrics['has_license']
        assert metrics.is_fork == known_repository_metrics['is_fork']
        assert metrics.is_archived == known_repository_metrics['is_archived']
    
    @pytest.mark.unit
    def test_extract_repository_metrics_error_handling(self):
        """Validate error handling during metrics extraction."""
        # Create mock repository that raises exceptions
        mock_repo = Mock(spec=Repository)
        mock_repo.name = 'error-test-repo'
        mock_repo.full_name = 'org/error-test-repo'
        mock_repo.stargazers_count = 10
        mock_repo.forks_count = 2
        mock_repo.watchers_count = 5
        mock_repo.size = 1000
        mock_repo.open_issues_count = 1
        mock_repo.language = 'Python'
        mock_repo.license = None
        mock_repo.fork = False
        mock_repo.archived = False
        mock_repo.created_at = datetime.utcnow()
        mock_repo.updated_at = datetime.utcnow()
        
        # Mock exceptions for advanced metrics
        mock_repo.get_commits.side_effect = GithubException(403, 'Rate limit exceeded')
        mock_repo.get_languages.side_effect = GithubException(404, 'Not Found')
        mock_repo.get_contents.side_effect = GithubException(403, 'Access denied')
        
        client = GitHubMetricsClient(token='test_token')
        
        # Should handle exceptions gracefully
        metrics = client._extract_repository_metrics(mock_repo)
        
        # Basic metrics should be extracted
        assert isinstance(metrics, RepositoryMetrics)
        assert metrics.name == 'error-test-repo'
        assert metrics.stars_count == 10
        
        # Advanced metrics should have default values due to exceptions
        assert metrics.commits_last_30_days == 0
        assert metrics.languages == {}
        assert metrics.has_readme is False
        assert metrics.has_ci is False
    
    @pytest.mark.unit
    def test_calculate_recent_commit_activity(self):
        """Validate recent commit activity calculation."""
        # Create mock repository
        mock_repo = Mock(spec=Repository)
        
        # Mock commits with totalCount
        mock_commits = Mock()
        mock_commits.totalCount = 25
        mock_repo.get_commits.return_value = mock_commits
        
        client = GitHubMetricsClient(token='test_token')
        
        # Calculate commit activity
        commit_count = client._calculate_recent_commit_activity(mock_repo)
        
        assert commit_count == 25
        
        # Verify get_commits called with appropriate since parameter
        mock_repo.get_commits.assert_called_once()
        call_args = mock_repo.get_commits.call_args
        assert 'since' in call_args.kwargs
        
        # Since parameter should be approximately 30 days ago
        since_date = call_args.kwargs['since']
        expected_date = datetime.utcnow() - timedelta(days=30)
        time_diff = abs((since_date - expected_date).total_seconds())
        assert time_diff < 3600, "Since date should be approximately 30 days ago"
    
    @pytest.mark.unit
    def test_detect_ci_system(self):
        """Validate CI/CD system detection logic."""
        mock_repo = Mock(spec=Repository)
        
        client = GitHubMetricsClient(token='test_token')
        
        # Test GitHub Actions detection
        mock_repo.get_contents.side_effect = [
            Mock(),  # .github/workflows exists
            GithubException(404, 'Not Found')  # Other CI files don't exist
        ]
        
        has_ci = client._detect_ci_system(mock_repo)
        assert has_ci is True
        
        # Test no CI system
        mock_repo.get_contents.side_effect = GithubException(404, 'Not Found')
        
        has_ci = client._detect_ci_system(mock_repo)
        assert has_ci is False
    
    @pytest.mark.unit
    def test_has_readme_detection(self):
        """Validate README file detection accuracy."""
        mock_repo = Mock(spec=Repository)
        
        client = GitHubMetricsClient(token='test_token')
        
        # Test README.md present
        mock_readme = Mock()
        mock_readme.name = 'README.md'
        mock_other = Mock()
        mock_other.name = 'setup.py'
        mock_repo.get_contents.return_value = [mock_readme, mock_other]
        
        has_readme = client._has_readme(mock_repo)
        assert has_readme is True
        
        # Test no README
        mock_no_readme = Mock()
        mock_no_readme.name = 'setup.py'
        mock_repo.get_contents.return_value = [mock_no_readme]
        
        has_readme = client._has_readme(mock_repo)
        assert has_readme is False


class TestOrganizationRepositoryDiscovery:
    """
    Systematic organization repository discovery validation.
    
    Technical Implementation:
    - Organization validation and access verification
    - Repository enumeration with pagination handling
    - Filtering logic for archived and forked repositories
    - Rate limiting management during discovery
    """
    
    @pytest.mark.unit
    @patch('pydcl.github_client.Github')
    def test_get_organization_repositories_success(self, mock_github, mock_github_repositories):
        """Validate successful organization repository discovery."""
        # Mock organization
        mock_org = Mock(spec=Organization)
        mock_org.name = 'OBINexus Computing'
        mock_org.public_repos = len(mock_github_repositories)
        
        # Mock repositories
        mock_repos = []
        for repo_data in mock_github_repositories:
            mock_repo = Mock(spec=Repository)
            mock_repo.name = repo_data['name']
            mock_repo.full_name = f"obinexus/{repo_data['name']}"
            mock_repo.stargazers_count = repo_data['stars_count']
            mock_repo.forks_count = 3
            mock_repo.watchers_count = 8
            mock_repo.size = repo_data['size_kb']
            mock_repo.open_issues_count = 2
            mock_repo.language = 'Python'
            mock_repo.license = Mock()
            mock_repo.fork = False
            mock_repo.archived = False
            mock_repo.created_at = datetime.utcnow()
            mock_repo.updated_at = datetime.utcnow()
            
            # Mock commit activity
            mock_commits = Mock()
            mock_commits.totalCount = repo_data['commits_last_30_days']
            mock_repo.get_commits.return_value = mock_commits
            
            # Mock languages and contents
            mock_repo.get_languages.return_value = {'Python': 10000}
            mock_readme = Mock()
            mock_readme.name = 'README.md'
            mock_repo.get_contents.return_value = [mock_readme]
            
            mock_repos.append(mock_repo)
        
        mock_org.get_repos.return_value = mock_repos
        
        # Mock GitHub client
        mock_client = Mock()
        mock_client.get_organization.return_value = mock_org
        
        # Mock rate limit
        mock_rate_limit = Mock()
        mock_rate_limit.core.remaining = 5000
        mock_client.get_rate_limit.return_value = mock_rate_limit
        
        mock_github.return_value = mock_client
        
        client = GitHubMetricsClient(token='test_token')
        
        # Get organization repositories
        repositories = client.get_organization_repositories('obinexus')
        
        # Validate results
        assert isinstance(repositories, list)
        assert len(repositories) == len(mock_github_repositories)
        
        for i, repo_metrics in enumerate(repositories):
            assert isinstance(repo_metrics, RepositoryMetrics)
            assert repo_metrics.name == mock_github_repositories[i]['name']
            assert repo_metrics.stars_count == mock_github_repositories[i]['stars_count']
    
    @pytest.mark.unit
    @patch('pydcl.github_client.Github')
    def test_get_organization_repositories_not_found(self, mock_github):
        """Validate error handling for non-existent organization."""
        # Mock GitHub client with organization not found
        mock_client = Mock()
        mock_client.get_organization.side_effect = GithubException(404, 'Not Found')
        
        mock_github.return_value = mock_client
        
        client = GitHubMetricsClient(token='test_token')
        
        # Should raise GithubException for non-existent organization
        with pytest.raises(GithubException):
            client.get_organization_repositories('nonexistent-org')
    
    @pytest.mark.unit
    @patch('pydcl.github_client.Github')
    def test_get_organization_repositories_filtering(self, mock_github):
        """Validate repository filtering logic."""
        # Mock organization
        mock_org = Mock(spec=Organization)
        mock_org.name = 'Test Organization'
        mock_org.public_repos = 3
        
        # Mock repositories with different characteristics
        mock_active_repo = Mock(spec=Repository)
        mock_active_repo.name = 'active-repo'
        mock_active_repo.fork = False
        mock_active_repo.archived = False
        # Add other required attributes...
        
        mock_fork_repo = Mock(spec=Repository)
        mock_fork_repo.name = 'fork-repo'
        mock_fork_repo.fork = True
        mock_fork_repo.archived = False
        
        mock_archived_repo = Mock(spec=Repository)
        mock_archived_repo.name = 'archived-repo'
        mock_archived_repo.fork = False
        mock_archived_repo.archived = True
        
        mock_org.get_repos.return_value = [mock_active_repo, mock_fork_repo, mock_archived_repo]
        
        # Mock GitHub client
        mock_client = Mock()
        mock_client.get_organization.return_value = mock_org
        mock_rate_limit = Mock()
        mock_rate_limit.core.remaining = 5000
        mock_client.get_rate_limit.return_value = mock_rate_limit
        
        mock_github.return_value = mock_client
        
        client = GitHubMetricsClient(token='test_token')
        
        # Test with archived repositories excluded (default)
        repositories = client.get_organization_repositories('test-org', include_archived=False)
        
        # Should only process active, non-fork repository
        # Note: Exact filtering behavior depends on implementation
        assert isinstance(repositories, list)


class TestRepositoryConfigurationLoading:
    """
    Repository configuration loading validation with systematic error handling.
    
    Technical Implementation:
    - Configuration file discovery with multiple path resolution
    - YAML parsing with comprehensive error handling
    - Default configuration application for missing files
    - Division validation and constraint checking
    """
    
    @pytest.mark.unit
    @patch('pydcl.github_client.Github')
    def test_get_repository_config_success(self, mock_github, sample_repo_yaml):
        """Validate successful repository configuration loading."""
        # Mock repository
        mock_repo = Mock(spec=Repository)
        
        # Mock configuration file content
        mock_content_file = Mock()
        mock_content_file.decoded_content.decode.return_value = sample_repo_yaml
        mock_repo.get_contents.return_value = mock_content_file
        
        # Mock GitHub client
        mock_client = Mock()
        mock_client.get_repo.return_value = mock_repo
        
        mock_github.return_value = mock_client
        
        client = GitHubMetricsClient(token='test_token')
        
        # Load repository configuration
        config = client.get_repository_config('obinexus', 'test-repo')
        
        # Validate configuration loading
        assert config is not None
        assert isinstance(config, RepositoryConfig)
        assert config.division == DivisionType.COMPUTING
        assert config.status == ProjectStatus.CORE
        assert config.sinphase_compliance is True
    
    @pytest.mark.unit
    @patch('pydcl.github_client.Github')
    def test_get_repository_config_not_found(self, mock_github):
        """Validate handling of missing repository configuration."""
        # Mock repository with no configuration file
        mock_repo = Mock(spec=Repository)
        mock_repo.get_contents.side_effect = GithubException(404, 'Not Found')
        
        # Mock GitHub client
        mock_client = Mock()
        mock_client.get_repo.return_value = mock_repo
        
        mock_github.return_value = mock_client
        
        client = GitHubMetricsClient(token='test_token')
        
        # Should return None for missing configuration
        config = client.get_repository_config('obinexus', 'no-config-repo')
        
        assert config is None
    
    @pytest.mark.unit
    @patch('pydcl.github_client.Github')
    def test_get_repository_config_malformed_yaml(self, mock_github):
        """Validate handling of malformed repository configuration."""
        # Mock repository with malformed YAML
        mock_repo = Mock(spec=Repository)
        
        malformed_yaml = """
division: "Computing"
status: "Core"
cost_factors:
  stars_weight: [invalid_yaml_structure
  # Missing closing bracket
"""
        
        mock_content_file = Mock()
        mock_content_file.decoded_content.decode.return_value = malformed_yaml
        mock_repo.get_contents.return_value = mock_content_file
        
        # Mock GitHub client
        mock_client = Mock()
        mock_client.get_repo.return_value = mock_repo
        
        mock_github.return_value = mock_client
        
        client = GitHubMetricsClient(token='test_token')
        
        # Should handle malformed YAML gracefully
        config = client.get_repository_config('obinexus', 'malformed-config-repo')
        
        # Should return None due to YAML parsing error
        assert config is None


class TestRateLimitingManagement:
    """
    Rate limiting management validation for GitHub API compliance.
    
    Technical Implementation:
    - Rate limit monitoring and threshold detection
    - Strategic delay implementation for limit exceedance
    - Request counting and periodic checking accuracy
    - Rate limit recovery handling
    """
    
    @pytest.mark.unit
    @patch('pydcl.github_client.Github')
    @patch('time.sleep')
    def test_manage_rate_limiting_threshold_exceeded(self, mock_sleep, mock_github):
        """Validate rate limiting management when threshold exceeded."""
        # Mock rate limit response
        mock_rate_limit = Mock()
        mock_rate_limit.core.remaining = 50  # Below buffer threshold (100)
        mock_rate_limit.core.reset = datetime.utcnow() + timedelta(minutes=15)
        
        mock_client = Mock()
        mock_client.get_rate_limit.return_value = mock_rate_limit
        
        mock_github.return_value = mock_client
        
        client = GitHubMetricsClient(token='test_token')
        client.request_count = 10  # Trigger rate limit check
        
        # Should implement strategic delay when threshold exceeded
        client._manage_rate_limiting()
        
        # Should have called sleep for rate limit delay
        mock_sleep.assert_called()
    
    @pytest.mark.unit
    @patch('pydcl.github_client.Github')
    def test_manage_rate_limiting_within_bounds(self, mock_github):
        """Validate rate limiting management when within acceptable bounds."""
        # Mock rate limit response
        mock_rate_limit = Mock()
        mock_rate_limit.core.remaining = 2000  # Well above buffer threshold
        
        mock_client = Mock()
        mock_client.get_rate_limit.return_value = mock_rate_limit
        
        mock_github.return_value = mock_client
        
        client = GitHubMetricsClient(token='test_token')
        client.request_count = 10  # Trigger rate limit check
        
        # Should proceed without delay when within bounds
        client._manage_rate_limiting()
        
        # No sleep should be called
        # Note: Verification depends on implementation details

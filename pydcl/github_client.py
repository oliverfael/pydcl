"""
PYDCL GitHub API Integration Client

Technical implementation of systematic GitHub API interaction following
waterfall methodology for comprehensive repository metrics extraction.

Key Technical Features:
- Structured API authentication with systematic validation
- Comprehensive repository metrics collection with error handling
- Division-aware configuration loading and validation
- Methodical rate limiting and pagination handling
- Strategic error recovery and retry mechanisms

Architecture: Deterministic API client with validation checkpoints
Technical Lead: Implementation aligned with Aegis project specifications
"""

import logging
import time
import yaml
from typing import Dict, List, Optional, Iterator, Any
from datetime import datetime, timedelta

from github import Github, Repository, Organization
from github.GithubException import GithubException, RateLimitExceededException

from .models import (
    RepositoryMetrics, RepositoryConfig, CostFactors, 
    DivisionType, ProjectStatus, ValidationError
)

logger = logging.getLogger(__name__)


class GitHubMetricsClient:
    """
    Technical GitHub API client implementing systematic repository analysis.
    
    Provides methodical interaction with GitHub API following waterfall
    methodology principles:
    - Structured validation and authentication
    - Comprehensive error handling and retry logic
    - Systematic metrics extraction with validation checkpoints
    - Division-aware configuration resolution
    """
    
    def __init__(self, token: str, timeout: int = 30, max_retries: int = 3):
        """
        Initialize GitHub client with systematic configuration.
        
        Args:
            token: GitHub API personal access token
            timeout: Request timeout in seconds
            max_retries: Maximum retry attempts for failed requests
        """
        self.token = token
        self.timeout = timeout
        self.max_retries = max_retries
        
        # Initialize GitHub API client
        self.client = Github(
            login_or_token=token,
            timeout=timeout,
            retry=max_retries
        )
        
        # Rate limiting parameters
        self.rate_limit_buffer = 100  # Minimum requests to maintain
        self.rate_limit_check_interval = 10  # Check every N requests
        self.request_count = 0
        
        logger.info("GitHubMetricsClient initialized with systematic configuration")
    
    def validate_connection(self) -> bool:
        """
        Systematic validation of GitHub API connectivity and authentication.
        
        Technical Implementation:
        - API authentication verification
        - Rate limit status assessment
        - Permissions validation for organization access
        
        Returns:
            Boolean indicating successful connection validation
        """
        try:
            # Validate authentication
            user = self.client.get_user()
            logger.info(f"GitHub API authenticated as: {user.login}")
            
            # Check rate limiting status
            rate_limit = self.client.get_rate_limit()
            core_remaining = rate_limit.core.remaining
            
            if core_remaining < self.rate_limit_buffer:
                logger.warning(
                    f"Rate limit concern: {core_remaining} requests remaining"
                )
                return False
            
            logger.info(f"Rate limit validated: {core_remaining} requests available")
            return True
            
        except GithubException as e:
            logger.error(f"GitHub API validation failed: {e}")
            return False
        except Exception as e:
            logger.error(f"Connection validation error: {e}")
            return False
    
    def get_organization_repositories(
        self, 
        org_name: str, 
        include_archived: bool = False
    ) -> List[RepositoryMetrics]:
        """
        Systematic repository discovery and metrics extraction.
        
        Technical Implementation:
        - Organization validation and access verification
        - Comprehensive repository enumeration with pagination
        - Systematic metrics extraction with error handling
        - Rate limiting management and progress tracking
        
        Args:
            org_name: GitHub organization name
            include_archived: Include archived repositories in analysis
            
        Returns:
            List of comprehensive repository metrics
        """
        try:
            # Phase 1: Organization Validation
            organization = self.client.get_organization(org_name)
            logger.info(f"Organization validated: {organization.name}")
            
            # Phase 2: Repository Discovery
            repositories = []
            total_repos = organization.public_repos
            
            logger.info(f"Discovering {total_repos} repositories...")
            
            # Systematic repository enumeration
            for repo in self._paginate_repositories(organization, include_archived):
                try:
                    # Rate limiting checkpoint
                    self._manage_rate_limiting()
                    
                    # Extract comprehensive metrics
                    metrics = self._extract_repository_metrics(repo)
                    repositories.append(metrics)
                    
                    logger.debug(f"Metrics extracted: {repo.name}")
                    
                except Exception as e:
                    logger.warning(f"Failed to extract metrics for {repo.name}: {e}")
                    continue
            
            logger.info(f"Repository discovery completed: {len(repositories)} analyzed")
            return repositories
            
        except GithubException as e:
            logger.error(f"Organization access failed: {e}")
            raise
        except Exception as e:
            logger.error(f"Repository discovery error: {e}")
            raise
    
    def get_repository_config(
        self, 
        org_name: str, 
        repo_name: str
    ) -> Optional[RepositoryConfig]:
        """
        Systematic repository configuration loading with validation.
        
        Technical Implementation:
        - Configuration file discovery (.github/repo.yaml)
        - YAML parsing with structured validation
        - Default configuration application for missing files
        - Division validation and constraint checking
        
        Args:
            org_name: GitHub organization name
            repo_name: Repository name
            
        Returns:
            Validated repository configuration or None if not found
        """
        try:
            repository = self.client.get_repo(f"{org_name}/{repo_name}")
            
            # Attempt to load .github/repo.yaml configuration
            config_paths = [
                ".github/repo.yaml",
                ".github/pydcl.yaml", 
                "repo.yaml",
                "pydcl.yaml"
            ]
            
            for config_path in config_paths:
                try:
                    content_file = repository.get_contents(config_path)
                    config_content = content_file.decoded_content.decode('utf-8')
                    
                    # Parse and validate YAML configuration
                    config_data = yaml.safe_load(config_content)
                    return self._validate_repository_config(config_data, repo_name)
                    
                except GithubException:
                    # Configuration file not found, try next path
                    continue
                except yaml.YAMLError as e:
                    logger.warning(f"YAML parsing error in {repo_name}: {e}")
                    continue
            
            # No configuration found - return None for default handling
            logger.debug(f"No configuration found for {repo_name}")
            return None
            
        except GithubException as e:
            logger.warning(f"Repository access failed for {repo_name}: {e}")
            return None
        except Exception as e:
            logger.error(f"Configuration loading error for {repo_name}: {e}")
            return None
    
    def _paginate_repositories(
        self, 
        organization: Organization, 
        include_archived: bool
    ) -> Iterator[Repository]:
        """Systematic repository pagination with filtering."""
        
        try:
            for repository in organization.get_repos():
                # Apply archived filter
                if not include_archived and repository.archived:
                    continue
                
                # Skip forks unless explicitly configured
                if repository.fork:
                    logger.debug(f"Skipping fork: {repository.name}")
                    continue
                
                yield repository
                
        except GithubException as e:
            logger.error(f"Repository pagination failed: {e}")
            raise
    
    def _extract_repository_metrics(self, repository: Repository) -> RepositoryMetrics:
        """
        Comprehensive repository metrics extraction with systematic validation.
        
        Technical Implementation:
        - Basic repository metadata extraction
        - Commit activity analysis (last 30 days)
        - Language distribution calculation
        - CI/CD system detection
        - Build and test metrics integration
        """
        
        # Basic repository metrics
        basic_metrics = {
            'name': repository.name,
            'full_name': repository.full_name,
            'stars_count': repository.stargazers_count,
            'forks_count': repository.forks_count,
            'watchers_count': repository.watchers_count,
            'size_kb': repository.size,
            'open_issues_count': repository.open_issues_count,
            'primary_language': repository.language,
            'has_readme': self._has_readme(repository),
            'has_license': repository.license is not None,
            'is_fork': repository.fork,
            'is_archived': repository.archived,
            'created_at': repository.created_at,
            'updated_at': repository.updated_at
        }
        
        # Advanced metrics with error handling
        advanced_metrics = {}
        
        try:
            # Commit activity analysis
            commits_30_days = self._calculate_recent_commit_activity(repository)
            advanced_metrics['commits_last_30_days'] = commits_30_days
            
            # Last commit timestamp
            try:
                commits = repository.get_commits()
                latest_commit = commits[0] if commits.totalCount > 0 else None
                advanced_metrics['last_commit_date'] = (
                    latest_commit.commit.committer.date if latest_commit else None
                )
            except (GithubException, IndexError):
                advanced_metrics['last_commit_date'] = None
            
        except GithubException as e:
            logger.warning(f"Advanced metrics extraction failed for {repository.name}: {e}")
            advanced_metrics.update({
                'commits_last_30_days': 0,
                'last_commit_date': None
            })
        
        try:
            # Language distribution
            languages = repository.get_languages()
            advanced_metrics['languages'] = dict(languages)
            
        except GithubException:
            advanced_metrics['languages'] = {}
        
        try:
            # CI/CD detection
            advanced_metrics['has_ci'] = self._detect_ci_system(repository)
            
            # Build metrics (placeholder - would integrate with CI systems)
            advanced_metrics['build_time_minutes'] = None
            advanced_metrics['test_coverage_percent'] = None
            
        except GithubException:
            advanced_metrics.update({
                'has_ci': False,
                'build_time_minutes': None,
                'test_coverage_percent': None
            })
        
        # Combine all metrics
        all_metrics = {**basic_metrics, **advanced_metrics}
        
        return RepositoryMetrics(**all_metrics)
    
    def _calculate_recent_commit_activity(self, repository: Repository) -> int:
        """Calculate commit activity in the last 30 days."""
        
        cutoff_date = datetime.utcnow() - timedelta(days=30)
        commit_count = 0
        
        try:
            commits = repository.get_commits(since=cutoff_date)
            # Use totalCount for efficiency if available
            if hasattr(commits, 'totalCount'):
                commit_count = commits.totalCount
            else:
                # Fallback to enumeration with limit
                for i, _ in enumerate(commits):
                    if i >= 1000:  # Reasonable limit for activity calculation
                        break
                    commit_count += 1
                    
        except GithubException as e:
            logger.debug(f"Commit activity calculation failed: {e}")
            commit_count = 0
        
        return commit_count
    
    def _has_readme(self, repository: Repository) -> bool:
        """Systematic README file detection."""
        
        readme_variants = ['README.md', 'README.rst', 'README.txt', 'README']
        
        try:
            contents = repository.get_contents("")
            if isinstance(contents, list):
                file_names = [item.name.upper() for item in contents]
                return any(variant.upper() in file_names for variant in readme_variants)
            
        except GithubException:
            pass
        
        return False
    
    def _detect_ci_system(self, repository: Repository) -> bool:
        """Systematic CI/CD system detection."""
        
        ci_indicators = [
            '.github/workflows',      # GitHub Actions
            '.gitlab-ci.yml',         # GitLab CI
            '.travis.yml',            # Travis CI
            'circle.yml',             # CircleCI
            'appveyor.yml',           # AppVeyor
            'azure-pipelines.yml',    # Azure DevOps
            'Jenkinsfile'             # Jenkins
        ]
        
        try:
            for indicator in ci_indicators:
                try:
                    repository.get_contents(indicator)
                    return True
                except GithubException:
                    continue
                    
        except Exception:
            pass
        
        return False
    
    def _validate_repository_config(
        self, 
        config_data: Dict[str, Any], 
        repo_name: str
    ) -> RepositoryConfig:
        """Systematic repository configuration validation."""
        
        try:
            # Division validation
            division_str = config_data.get('division', 'Computing')
            try:
                division = DivisionType(division_str)
            except ValueError:
                logger.warning(f"Invalid division '{division_str}' for {repo_name}, defaulting to Computing")
                division = DivisionType.COMPUTING
            
            # Status validation
            status_str = config_data.get('status', 'Active')
            try:
                status = ProjectStatus(status_str)
            except ValueError:
                logger.warning(f"Invalid status '{status_str}' for {repo_name}, defaulting to Active")
                status = ProjectStatus.ACTIVE
            
            # Cost factors validation
            cost_factors_data = config_data.get('cost_factors', {})
            cost_factors = CostFactors(**cost_factors_data)
            
            # Additional configuration parameters
            config = RepositoryConfig(
                division=division,
                status=status,
                cost_factors=cost_factors,
                tags=config_data.get('tags', []),
                dependencies=config_data.get('dependencies', []),
                sinphase_compliance=config_data.get('sinphase_compliance', True),
                isolation_required=config_data.get('isolation_required', False),
                manual_override=config_data.get('manual_override')
            )
            
            logger.debug(f"Configuration validated for {repo_name}")
            return config
            
        except Exception as e:
            logger.error(f"Configuration validation failed for {repo_name}: {e}")
            raise
    
    def _manage_rate_limiting(self) -> None:
        """Systematic rate limiting management with strategic delays."""
        
        self.request_count += 1
        
        # Check rate limit periodically
        if self.request_count % self.rate_limit_check_interval == 0:
            try:
                rate_limit = self.client.get_rate_limit()
                remaining = rate_limit.core.remaining
                reset_time = rate_limit.core.reset
                
                if remaining < self.rate_limit_buffer:
                    # Calculate wait time until reset
                    wait_seconds = (reset_time - datetime.utcnow()).total_seconds()
                    wait_seconds = max(0, min(wait_seconds, 3600))  # Cap at 1 hour
                    
                    logger.warning(
                        f"Rate limit threshold reached. Waiting {wait_seconds:.0f} seconds..."
                    )
                    time.sleep(wait_seconds + 60)  # Additional buffer
                
                logger.debug(f"Rate limit status: {remaining} requests remaining")
                
            except RateLimitExceededException:
                logger.warning("Rate limit exceeded. Implementing strategic delay...")
                time.sleep(900)  # 15-minute delay
                
            except GithubException as e:
                logger.warning(f"Rate limit check failed: {e}")

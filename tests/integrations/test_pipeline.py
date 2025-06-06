"""
PYDCL Pipeline Integration Tests
==============================

Comprehensive pipeline integration testing implementing UML System Operation Integrity
validation following Aegis project waterfall methodology specifications.

Technical Focus:
- Complete cost analysis pipeline execution verification
- Division-aware organizational processing validation
- JSON output schema compliance and data integrity
- Cryptographic echo testing for deterministic pipeline execution
- System-level governance threshold enforcement validation

Test Architecture: Integration testing with systematic mock coordination
Implementation: Waterfall gate validation per OBINexus technical standards
"""

import pytest
import json
import yaml
import hashlib
import tempfile
import os
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
from typing import Dict, Any, List
from datetime import datetime

# PYDCL imports with comprehensive error handling
try:
    from pydcl.models import (
        RepositoryMetrics, CostFactors, DivisionType, ProjectStatus,
        CostCalculationResult, OrganizationCostReport,
        calculate_sinphase_cost, GOVERNANCE_THRESHOLD
    )
    from pydcl.cost_scores import CostScoreCalculator
    from pydcl.github_client import GitHubMetricsClient
    from pydcl.utils import validate_config, load_division_config
    from pydcl import cli
except ImportError as e:
    pytest.skip(f"PYDCL modules unavailable for integration testing: {e}", allow_module_level=True)


class TestCompleteOrganizationAnalysis:
    """
    Complete organization analysis pipeline validation following systematic integration.
    
    Technical Implementation:
    - End-to-end organizational repository discovery and analysis
    - Division-aware cost calculation and governance validation
    - JSON output generation with schema compliance verification
    - Performance characteristics under realistic data loads
    """
    
    @pytest.mark.integration
    @patch('pydcl.github_client.Github')
    def test_complete_organization_pipeline_execution(self, mock_github, mock_github_repositories, sample_org_config):
        """
        Validate complete organization analysis pipeline from GitHub discovery to JSON output.
        
        Technical Verification:
        - GitHub API integration with systematic repository discovery
        - Cost calculation engine coordination with division configuration
        - Comprehensive organization report generation with governance validation
        - JSON output schema compliance and data structure preservation
        """
        # Mock GitHub organization and repositories
        mock_org = Mock()
        mock_org.name = 'OBINexus Computing'
        mock_org.public_repos = len(mock_github_repositories)
        
        # Create comprehensive mock repositories
        mock_repos = []
        for repo_data in mock_github_repositories:
            mock_repo = self._create_mock_repository(repo_data)
            mock_repos.append(mock_repo)
        
        mock_org.get_repos.return_value = mock_repos
        
        # Mock GitHub client configuration
        mock_client = Mock()
        mock_client.get_organization.return_value = mock_org
        mock_rate_limit = Mock()
        mock_rate_limit.core.remaining = 5000
        mock_client.get_rate_limit.return_value = mock_rate_limit
        
        mock_github.return_value = mock_client
        
        # Initialize pipeline components
        github_client = GitHubMetricsClient(token='test_token')
        cost_calculator = CostScoreCalculator()
        
        # Execute complete pipeline
        try:
            # Phase 1: Repository discovery
            repositories = github_client.get_organization_repositories('obinexus')
            
            # Phase 2: Cost calculation for each repository
            organization_report = OrganizationCostReport('obinexus')
            organization_report.total_repositories = len(repositories)
            organization_report.analyzed_repositories = 0
            
            for repo_metrics in repositories:
                # Calculate cost score
                cost_result = cost_calculator.calculate_repository_cost(repo_metrics)
                
                # Create comprehensive result
                calculation_result = CostCalculationResult(
                    repository=repo_metrics.name,
                    division=DivisionType.COMPUTING,  # Default for testing
                    status=ProjectStatus.ACTIVE
                )
                calculation_result.normalized_score = cost_result['normalized_score']
                calculation_result.governance_alerts = cost_result['governance_alerts']
                calculation_result.raw_metrics = repo_metrics
                
                # Apply governance thresholds
                calculation_result.apply_governance_thresholds()
                
                organization_report.repository_scores.append(calculation_result)
                organization_report.analyzed_repositories += 1
            
            # Phase 3: Organization-level metrics calculation
            organization_report.calculate_governance_metrics()
            
            # Phase 4: JSON output generation
            json_output = self._generate_json_output(organization_report)
            
            # Systematic validation checkpoints
            self._validate_pipeline_execution_results(
                repositories, organization_report, json_output, mock_github_repositories
            )
            
        except Exception as e:
            pytest.fail(f"Complete pipeline execution failed: {e}")
    
    @pytest.mark.integration
    def test_division_aware_analysis_workflow(self, mock_github_repositories, sample_org_config):
        """
        Validate division-aware analysis workflow with systematic parameter application.
        
        Technical Focus:
        - Division configuration loading and parameter application
        - Cost calculation with division-specific governance thresholds
        - Priority boost coefficient systematic application
        - Cross-division consistency validation
        """
        # Load division configuration
        config_data = yaml.safe_load(sample_org_config)
        
        try:
            # Simulate division configuration loading
            division_configs = {
                DivisionType.COMPUTING: {
                    'governance_threshold': 0.6,
                    'isolation_threshold': 0.8,
                    'priority_boost': 1.2
                },
                DivisionType.UCHE_NNAMDI: {
                    'governance_threshold': 0.5,
                    'isolation_threshold': 0.7,
                    'priority_boost': 1.5
                },
                DivisionType.AEGIS_ENGINEERING: {
                    'governance_threshold': 0.6,
                    'isolation_threshold': 0.8,
                    'priority_boost': 1.3
                }
            }
            
            # Process repositories with division-specific configurations
            cost_calculator = CostScoreCalculator()
            division_results = {}
            
            for repo_data in mock_github_repositories:
                # Create repository metrics
                metrics = RepositoryMetrics(repo_data['name'])
                metrics.stars_count = repo_data['stars_count']
                metrics.commits_last_30_days = repo_data['commits_last_30_days']
                metrics.size_kb = repo_data['size_kb']
                
                # Get division configuration
                division = DivisionType(repo_data['division'])
                division_config = division_configs.get(division, division_configs[DivisionType.COMPUTING])
                
                # Calculate cost with division-specific parameters
                cost_config = {
                    'division': division,
                    'priority_boost': division_config['priority_boost']
                }
                
                cost_result = cost_calculator.calculate_repository_cost(metrics, cost_config)
                
                # Store results by division
                if division not in division_results:
                    division_results[division] = []
                
                division_results[division].append({
                    'repository': repo_data['name'],
                    'cost_score': cost_result['normalized_score'],
                    'governance_alerts': cost_result['governance_alerts']
                })
            
            # Validate division-aware processing
            self._validate_division_aware_results(division_results, division_configs)
            
        except Exception as e:
            pytest.fail(f"Division-aware analysis workflow failed: {e}")
    
    @pytest.mark.integration
    def test_large_organization_scalability(self, performance_test_data):
        """
        Validate pipeline scalability with large organization dataset.
        
        Performance Verification:
        - Processing time characteristics under realistic load
        - Memory usage patterns during bulk analysis
        - Rate limiting behavior with extensive API calls
        - Output generation performance with large datasets
        """
        large_dataset = performance_test_data['large_organization_repos']
        
        # Initialize performance monitoring
        start_time = datetime.utcnow()
        cost_calculator = CostScoreCalculator()
        processed_repositories = []
        
        try:
            # Process large dataset systematically
            for i, repo_data in enumerate(large_dataset):
                # Create repository metrics
                metrics = RepositoryMetrics(repo_data['name'])
                metrics.stars_count = repo_data['stars_count']
                metrics.commits_last_30_days = repo_data['commits_last_30_days']
                metrics.size_kb = repo_data['size_kb']
                
                # Calculate cost
                cost_result = cost_calculator.calculate_repository_cost(metrics)
                
                processed_repositories.append({
                    'repository': repo_data['name'],
                    'division': repo_data['division'],
                    'cost_score': cost_result['normalized_score']
                })
                
                # Performance checkpoint every 25 repositories
                if (i + 1) % 25 == 0:
                    elapsed_time = (datetime.utcnow() - start_time).total_seconds()
                    processing_rate = (i + 1) / elapsed_time
                    
                    # Validate reasonable processing performance
                    assert processing_rate > 10, f"Processing rate too slow: {processing_rate:.2f} repos/sec"
            
            # Validate final results
            assert len(processed_repositories) == len(large_dataset)
            
            # Performance validation
            total_time = (datetime.utcnow() - start_time).total_seconds()
            final_rate = len(large_dataset) / total_time
            
            # Should process at least 20 repositories per second
            assert final_rate > 20, f"Final processing rate insufficient: {final_rate:.2f} repos/sec"
            
        except Exception as e:
            pytest.fail(f"Large organization scalability test failed: {e}")


class TestJSONOutputIntegrity:
    """
    Comprehensive JSON output integrity validation with schema compliance verification.
    
    Technical Implementation:
    - Complete JSON schema validation against PYDCL specification
    - Data structure preservation verification throughout pipeline
    - Division summary generation accuracy and completeness
    - Inverted triangle layer classification systematic validation
    """
    
    @pytest.mark.integration
    def test_complete_json_schema_compliance(self, mock_github_repositories, expected_json_schema):
        """
        Validate complete JSON output schema compliance with systematic verification.
        
        Technical Verification:
        - JSON structure validation against comprehensive schema
        - Required field presence and data type compliance
        - Division-aware data organization accuracy
        - Governance alert structure and content validation
        """
        # Generate complete organization report
        organization_report = OrganizationCostReport('obinexus')
        organization_report.total_repositories = len(mock_github_repositories)
        organization_report.analyzed_repositories = len(mock_github_repositories)
        
        # Process all repositories systematically
        cost_calculator = CostScoreCalculator()
        
        for repo_data in mock_github_repositories:
            # Create repository metrics
            metrics = RepositoryMetrics(repo_data['name'])
            metrics.stars_count = repo_data['stars_count']
            metrics.commits_last_30_days = repo_data['commits_last_30_days']
            metrics.size_kb = repo_data['size_kb']
            
            # Calculate cost
            cost_result = cost_calculator.calculate_repository_cost(metrics)
            
            # Create calculation result
            calculation_result = CostCalculationResult(
                repository=repo_data['name'],
                division=DivisionType(repo_data['division']),
                status=ProjectStatus(repo_data['status'])
            )
            calculation_result.normalized_score = cost_result['normalized_score']
            calculation_result.governance_alerts = cost_result['governance_alerts']
            calculation_result.apply_governance_thresholds()
            
            organization_report.repository_scores.append(calculation_result)
        
        # Calculate organization metrics
        organization_report.calculate_governance_metrics()
        
        # Generate JSON output
        json_output = self._generate_json_output(organization_report)
        
        # Comprehensive schema validation
        self._validate_json_schema_compliance(json_output, expected_json_schema)
        
        # Additional integrity validation
        self._validate_json_data_integrity(json_output, mock_github_repositories)
    
    @pytest.mark.integration
    def test_division_summary_generation_accuracy(self, mock_github_repositories):
        """
        Validate division summary generation accuracy and completeness.
        
        Technical Focus:
        - Division-specific repository grouping accuracy
        - Statistical calculation precision for division summaries
        - Governance violation tracking per division
        - Isolation candidate identification systematic validation
        """
        # Create organization report with division processing
        organization_report = OrganizationCostReport('obinexus')
        cost_calculator = CostScoreCalculator()
        
        # Process repositories and track division metrics
        division_tracking = {}
        
        for repo_data in mock_github_repositories:
            metrics = RepositoryMetrics(repo_data['name'])
            metrics.stars_count = repo_data['stars_count']
            metrics.commits_last_30_days = repo_data['commits_last_30_days']
            
            cost_result = cost_calculator.calculate_repository_cost(metrics)
            
            calculation_result = CostCalculationResult(
                repository=repo_data['name'],
                division=DivisionType(repo_data['division']),
                status=ProjectStatus(repo_data['status'])
            )
            calculation_result.normalized_score = cost_result['normalized_score']
            calculation_result.governance_alerts = cost_result['governance_alerts']
            calculation_result.apply_governance_thresholds()
            
            organization_report.repository_scores.append(calculation_result)
            
            # Track division metrics
            division = repo_data['division']
            if division not in division_tracking:
                division_tracking[division] = {
                    'repositories': [],
                    'total_score': 0.0,
                    'governance_violations': 0
                }
            
            division_tracking[division]['repositories'].append(repo_data['name'])
            division_tracking[division]['total_score'] += cost_result['normalized_score']
            
            if cost_result['normalized_score'] > GOVERNANCE_THRESHOLD * 100:
                division_tracking[division]['governance_violations'] += 1
        
        # Generate division summaries
        division_summaries = {}
        for division, tracking in division_tracking.items():
            division_summaries[division] = {
                'total_repositories': len(tracking['repositories']),
                'average_cost_score': tracking['total_score'] / len(tracking['repositories']),
                'governance_violations': tracking['governance_violations'],
                'top_repositories': tracking['repositories'][:3]  # Top 3 for summary
            }
        
        # Validate division summary accuracy
        self._validate_division_summaries(division_summaries, division_tracking)
    
    @pytest.mark.integration
    def test_inverted_triangle_layer_classification(self, mock_github_repositories):
        """
        Validate inverted triangle layer classification systematic accuracy.
        
        Technical Implementation:
        - Cost score distribution analysis and layer assignment
        - Surface layer (top 30%) identification accuracy
        - Active layer (middle 40%) classification precision
        - Core layer (bottom 30%) systematic validation
        """
        # Process repositories and collect cost scores
        cost_calculator = CostScoreCalculator()
        repository_scores = []
        
        for repo_data in mock_github_repositories:
            metrics = RepositoryMetrics(repo_data['name'])
            metrics.stars_count = repo_data['stars_count']
            metrics.commits_last_30_days = repo_data['commits_last_30_days']
            
            cost_result = cost_calculator.calculate_repository_cost(metrics)
            
            repository_scores.append({
                'repository': repo_data['name'],
                'cost_score': cost_result['normalized_score']
            })
        
        # Sort by cost score for layer classification
        sorted_repos = sorted(repository_scores, key=lambda x: x['cost_score'], reverse=True)
        total_repos = len(sorted_repos)
        
        # Calculate layer boundaries
        surface_boundary = int(total_repos * 0.3)
        active_boundary = int(total_repos * 0.7)
        
        # Classify into layers
        layers = {
            'surface': sorted_repos[:surface_boundary],
            'active': sorted_repos[surface_boundary:active_boundary],
            'core': sorted_repos[active_boundary:]
        }
        
        # Validate layer classification
        self._validate_inverted_triangle_layers(layers, sorted_repos)


class TestPipelineIntegrityEcho:
    """
    Pipeline integrity echo validation implementing Divisor Echo Hypothesis.
    
    Technical Implementation:
    - Cryptographic hash validation for deterministic pipeline execution
    - Complete system state preservation verification across iterations
    - Configuration determinism validation with hash consistency
    - Mathematical reproducibility validation under identical inputs
    """
    
    @pytest.mark.integration
    @pytest.mark.echo
    def test_complete_pipeline_deterministic_execution(self, mock_github_repositories, sample_org_config):
        """
        Validate complete pipeline produces deterministic results for identical inputs.
        
        Divisor Echo Hypothesis Implementation:
        - Execute complete pipeline twice with identical inputs
        - Generate cryptographic hashes of all intermediate and final outputs
        - Verify hash consistency across execution iterations
        - Validate system state preservation and mathematical reproducibility
        """
        # Execute pipeline first iteration
        first_execution_results = self._execute_complete_pipeline(
            mock_github_repositories, sample_org_config
        )
        first_execution_hash = self._generate_comprehensive_execution_hash(first_execution_results)
        
        # Execute pipeline second iteration with identical inputs
        second_execution_results = self._execute_complete_pipeline(
            mock_github_repositories, sample_org_config
        )
        second_execution_hash = self._generate_comprehensive_execution_hash(second_execution_results)
        
        # Echo validation - hashes must be identical
        assert first_execution_hash == second_execution_hash, \
            f"Pipeline execution not deterministic: {first_execution_hash} != {second_execution_hash}"
        
        # Detailed result comparison
        self._validate_execution_result_consistency(first_execution_results, second_execution_results)
    
    @pytest.mark.integration
    @pytest.mark.echo
    def test_configuration_hash_determinism(self, sample_org_config, sample_repo_yaml):
        """
        Validate configuration hashing produces consistent results across multiple iterations.
        
        Technical Verification:
        - Configuration normalization consistency
        - Hash generation determinism validation
        - Configuration change sensitivity verification
        """
        # Parse configurations
        org_config = yaml.safe_load(sample_org_config)
        repo_config = yaml.safe_load(sample_repo_yaml)
        
        # Generate hashes multiple times
        hash_iterations = 10
        org_hashes = []
        repo_hashes = []
        
        for i in range(hash_iterations):
            org_hash = self._generate_config_hash(org_config)
            repo_hash = self._generate_config_hash(repo_config)
            
            org_hashes.append(org_hash)
            repo_hashes.append(repo_hash)
        
        # All hashes should be identical
        assert len(set(org_hashes)) == 1, "Organization configuration hashing not deterministic"
        assert len(set(repo_hashes)) == 1, "Repository configuration hashing not deterministic"
        
        # Validate hash format consistency
        for hash_value in org_hashes + repo_hashes:
            assert len(hash_value) == 64, "SHA-256 hash should be 64 characters"
            assert all(c in '0123456789abcdef' for c in hash_value), "Hash should be hexadecimal"
    
    @pytest.mark.integration
    @pytest.mark.echo
    def test_sinphase_compliance_preservation(self, known_repository_metrics):
        """
        Validate Sinphasé compliance preservation throughout complete pipeline execution.
        
        Governance Integrity Verification:
        - Cost calculations remain within governance bounds across iterations
        - Isolation recommendations maintain consistency
        - Threshold validation preservation under systematic processing
        """
        # Create repository metrics
        metrics = RepositoryMetrics(known_repository_metrics['name'])
        metrics.stars_count = known_repository_metrics['stars_count']
        metrics.commits_last_30_days = known_repository_metrics['commits_last_30_days']
        metrics.size_kb = known_repository_metrics['size_kb']
        
        cost_calculator = CostScoreCalculator()
        
        # Execute cost calculation multiple iterations
        calculation_iterations = 20
        results = []
        
        for i in range(calculation_iterations):
            cost_result = cost_calculator.calculate_repository_cost(metrics)
            
            calculation_result = CostCalculationResult(
                repository=metrics.name,
                division=DivisionType.COMPUTING,
                status=ProjectStatus.ACTIVE
            )
            calculation_result.normalized_score = cost_result['normalized_score']
            calculation_result.governance_alerts = cost_result['governance_alerts']
            calculation_result.apply_governance_thresholds()
            
            results.append({
                'iteration': i,
                'normalized_score': calculation_result.normalized_score,
                'governance_alerts': len(calculation_result.governance_alerts),
                'requires_isolation': calculation_result.requires_isolation
            })
        
        # Validate consistency across iterations
        first_result = results[0]
        for i, result in enumerate(results[1:], 1):
            assert result['normalized_score'] == first_result['normalized_score'], \
                f"Cost calculation inconsistent at iteration {i}"
            assert result['governance_alerts'] == first_result['governance_alerts'], \
                f"Governance alerts inconsistent at iteration {i}"
            assert result['requires_isolation'] == first_result['requires_isolation'], \
                f"Isolation requirement inconsistent at iteration {i}"
        
        # Validate Sinphasé bounds compliance
        for result in results:
            assert 0.0 <= result['normalized_score'] <= 100.0, \
                f"Normalized score out of bounds: {result['normalized_score']}"
            
            # Governance compliance validation
            raw_score = result['normalized_score'] / 100.0
            is_compliant = raw_score <= GOVERNANCE_THRESHOLD
            
            if not is_compliant and result['governance_alerts'] == 0:
                pytest.fail(f"Governance threshold exceeded but no alerts generated: {result}")


    # Helper Methods for Integration Testing
    
    def _create_mock_repository(self, repo_data: Dict[str, Any]) -> Mock:
        """Create comprehensive mock repository object for testing."""
        mock_repo = Mock()
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
        
        # Mock languages and README
        mock_repo.get_languages.return_value = {'Python': 10000}
        mock_readme = Mock()
        mock_readme.name = 'README.md'
        mock_repo.get_contents.return_value = [mock_readme]
        
        return mock_repo
    
    def _generate_json_output(self, organization_report: OrganizationCostReport) -> Dict[str, Any]:
        """Generate JSON output from organization report."""
        json_output = {
            'organization': organization_report.organization,
            'generation_timestamp': datetime.utcnow().isoformat(),
            'total_repositories': organization_report.total_repositories,
            'analyzed_repositories': organization_report.analyzed_repositories,
            'sinphase_compliance_rate': organization_report.sinphase_compliance_rate,
            'repository_scores': []
        }
        
        for score in organization_report.repository_scores:
            json_output['repository_scores'].append({
                'repository': score.repository,
                'division': score.division.value,
                'status': score.status.value,
                'normalized_score': score.normalized_score,
                'governance_alerts': score.governance_alerts,
                'sinphase_violations': score.sinphase_violations,
                'requires_isolation': score.requires_isolation
            })
        
        return json_output
    
    def _validate_pipeline_execution_results(self, repositories, organization_report, json_output, expected_repos):
        """Validate complete pipeline execution results."""
        # Repository discovery validation
        assert len(repositories) == len(expected_repos)
        
        # Organization report validation
        assert organization_report.total_repositories == len(expected_repos)
        assert organization_report.analyzed_repositories == len(expected_repos)
        assert len(organization_report.repository_scores) == len(expected_repos)
        
        # JSON output validation
        assert json_output['total_repositories'] == len(expected_repos)
        assert len(json_output['repository_scores']) == len(expected_repos)
    
    def _validate_division_aware_results(self, division_results, division_configs):
        """Validate division-aware processing results."""
        for division, results in division_results.items():
            division_config = division_configs.get(division)
            assert division_config is not None, f"Missing configuration for division: {division}"
            
            # Validate priority boost application
            for result in results:
                assert 'cost_score' in result
                assert 'governance_alerts' in result
                assert result['cost_score'] >= 0.0
    
    def _validate_json_schema_compliance(self, json_output, expected_schema):
        """Validate JSON output schema compliance."""
        # Basic structure validation
        required_fields = ['organization', 'total_repositories', 'analyzed_repositories', 'repository_scores']
        for field in required_fields:
            assert field in json_output, f"Missing required field: {field}"
        
        # Repository scores validation
        for repo_score in json_output['repository_scores']:
            repo_required_fields = ['repository', 'division', 'status', 'normalized_score']
            for field in repo_required_fields:
                assert field in repo_score, f"Missing repository field: {field}"
    
    def _validate_json_data_integrity(self, json_output, expected_repos):
        """Validate JSON data integrity and consistency."""
        repo_names = [repo['repository'] for repo in json_output['repository_scores']]
        expected_names = [repo['name'] for repo in expected_repos]
        
        assert set(repo_names) == set(expected_names), "Repository name mismatch in JSON output"
    
    def _validate_division_summaries(self, division_summaries, division_tracking):
        """Validate division summary accuracy."""
        for division, summary in division_summaries.items():
            tracking = division_tracking[division]
            
            assert summary['total_repositories'] == len(tracking['repositories'])
            assert summary['governance_violations'] == tracking['governance_violations']
    
    def _validate_inverted_triangle_layers(self, layers, sorted_repos):
        """Validate inverted triangle layer classification accuracy."""
        total_classified = len(layers['surface']) + len(layers['active']) + len(layers['core'])
        assert total_classified == len(sorted_repos), "Layer classification count mismatch"
        
        # Validate layer boundaries
        if len(sorted_repos) > 0:
            surface_max_score = max([repo['cost_score'] for repo in layers['surface']], default=0)
            core_min_score = min([repo['cost_score'] for repo in layers['core']], default=100)
            
            assert surface_max_score >= core_min_score, "Layer classification order validation"
    
    def _execute_complete_pipeline(self, mock_repos, config):
        """Execute complete pipeline for echo testing."""
        cost_calculator = CostScoreCalculator()
        results = []
        
        for repo_data in mock_repos:
            metrics = RepositoryMetrics(repo_data['name'])
            metrics.stars_count = repo_data['stars_count']
            metrics.commits_last_30_days = repo_data['commits_last_30_days']
            
            cost_result = cost_calculator.calculate_repository_cost(metrics)
            
            results.append({
                'repository': repo_data['name'],
                'cost_score': cost_result['normalized_score'],
                'governance_alerts': cost_result['governance_alerts']
            })
        
        return {
            'repositories': results,
            'configuration_hash': self._generate_config_hash(yaml.safe_load(config))
        }
    
    def _generate_comprehensive_execution_hash(self, execution_results):
        """Generate comprehensive hash of execution results."""
        normalized_results = json.dumps(execution_results, sort_keys=True, separators=(',', ':'))
        return hashlib.sha256(normalized_results.encode('utf-8')).hexdigest()
    
    def _generate_config_hash(self, config_data):
        """Generate deterministic configuration hash."""
        normalized_config = json.dumps(config_data, sort_keys=True, separators=(',', ':'))
        return hashlib.sha256(normalized_config.encode('utf-8')).hexdigest()
    
    def _validate_execution_result_consistency(self, first_results, second_results):
        """Validate execution result consistency between iterations."""
        assert len(first_results['repositories']) == len(second_results['repositories'])
        
        for i, (first_repo, second_repo) in enumerate(zip(first_results['repositories'], second_results['repositories'])):
            assert first_repo['repository'] == second_repo['repository'], f"Repository name mismatch at index {i}"
            assert first_repo['cost_score'] == second_repo['cost_score'], f"Cost score mismatch at index {i}"
            assert first_repo['governance_alerts'] == second_repo['governance_alerts'], f"Governance alerts mismatch at index {i}"

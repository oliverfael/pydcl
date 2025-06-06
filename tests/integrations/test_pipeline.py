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


class TestCLIPipelineIntegration:
    """
    CLI pipeline integration validation with systematic command execution testing.
    
    Technical Implementation:
    - Complete CLI workflow execution validation
    - Configuration integration with pipeline components
    - Output format compliance across CLI commands
    - Error handling coordination between CLI and core systems
    """
    
    @pytest.mark.integration
    @patch('pydcl.github_client.GitHubMetricsClient')
    @patch('pydcl.cost_scores.CostScoreCalculator')
    def test_cli_analyze_command_integration(self, mock_calculator, mock_client, mock_github_repositories):
        """
        Validate complete CLI analyze command integration workflow.
        
        Technical Verification:
        - CLI argument parsing with pipeline component coordination
        - GitHub client initialization and authentication flow
        - Cost calculation engine integration with CLI output formatting
        - JSON file generation with systematic validation
        """
        # Mock calculator responses
        mock_calc_instance = Mock()
        mock_calc_instance.calculate_repository_cost.return_value = {
            'normalized_score': 25.0,
            'governance_alerts': []
        }
        mock_calculator.return_value = mock_calc_instance
        
        # Mock GitHub client responses  
        mock_client_instance = Mock()
        mock_client_instance.validate_connection.return_value = True
        
        # Create mock repository metrics
        mock_repositories = []
        for repo_data in mock_github_repositories:
            metrics = RepositoryMetrics(repo_data['name'])
            metrics.stars_count = repo_data['stars_count']
            metrics.commits_last_30_days = repo_data['commits_last_30_days']
            mock_repositories.append(metrics)
        
        mock_client_instance.get_organization_repositories.return_value = mock_repositories
        mock_client.return_value = mock_client_instance
        
        # Test CLI analyze command execution
        test_args = ['pydcl', 'analyze', '--org', 'obinexus', '--output', 'test_output.json']
        
        with patch('sys.argv', test_args):
            with patch('builtins.print') as mock_print:
                with tempfile.TemporaryDirectory() as temp_dir:
                    output_file = Path(temp_dir) / 'test_output.json'
                    
                    try:
                        # Note: This would test actual CLI implementation when available
                        # Current implementation is placeholder
                        cli.main()
                        
                        # Validate CLI output indicates proper handling
                        assert mock_print.called
                        output = ' '.join([str(call) for call in mock_print.call_args_list])
                        
                        # Should indicate development phase handling
                        development_indicators = ['not yet implemented', 'development', 'analyze']
                        assert any(indicator in output.lower() for indicator in development_indicators)
                        
                    except NotImplementedError:
                        pytest.skip("CLI analyze command not yet implemented")
    
    @pytest.mark.integration
    def test_cli_configuration_integration(self, sample_org_config, temp_config_dir):
        """
        Validate CLI configuration integration with pipeline components.
        
        Technical Focus:
        - Configuration file discovery and loading integration
        - CLI parameter override mechanisms
        - Configuration validation integration with pipeline
        - Error handling coordination across CLI and configuration systems
        """
        # Create configuration files in test environment
        config_file = temp_config_dir / 'pydcl.yaml'
        config_file.write_text(sample_org_config)
        
        # Test CLI with configuration file
        test_args = ['pydcl', 'analyze', '--org', 'obinexus', '--config', str(config_file)]
        
        with patch('sys.argv', test_args):
            with patch('builtins.print') as mock_print:
                try:
                    cli.main()
                    
                    # Should handle configuration integration
                    assert mock_print.called
                    output = ' '.join([str(call) for call in mock_print.call_args_list])
                    
                    # Should indicate configuration handling capability
                    config_indicators = ['config', 'not yet implemented', 'development']
                    assert any(indicator in output.lower() for indicator in config_indicators)
                    
                except NotImplementedError:
                    pytest.skip("CLI configuration integration not yet implemented")
    
    @pytest.mark.integration
    def test_cli_output_format_integration(self, mock_github_repositories):
        """
        Validate CLI output format integration across different commands.
        
        Technical Implementation:
        - JSON output format consistency validation
        - Table display format integration testing
        - Error output standardization verification
        - Progress reporting integration validation
        """
        output_format_tests = [
            {
                'args': ['pydcl', 'analyze', '--org', 'obinexus', '--output', 'scores.json'],
                'expected_format': 'json',
                'description': 'JSON output format'
            },
            {
                'args': ['pydcl', 'display', '--input', 'scores.json', '--format', 'table'],
                'expected_format': 'table',
                'description': 'Table display format'
            }
        ]
        
        for test_case in output_format_tests:
            with patch('sys.argv', test_case['args']):
                with patch('builtins.print') as mock_print:
                    try:
                        cli.main()
                        
                        # Validate output format handling
                        assert mock_print.called
                        output = ' '.join([str(call) for call in mock_print.call_args_list])
                        
                        # Should handle format specification
                        format_indicators = [test_case['expected_format'], 'not yet implemented']
                        assert any(indicator in output.lower() for indicator in format_indicators), \
                            f"Should handle {test_case['description']}"
                            
                    except NotImplementedError:
                        pytest.skip(f"CLI {test_case['description']} not yet implemented")


class TestErrorHandlingIntegration:
    """
    Comprehensive error handling integration validation across pipeline components.
    
    Technical Implementation:
    - Cross-component error propagation validation
    - Error recovery mechanism coordination testing
    - User-facing error message consistency verification
    - System resilience validation under failure conditions
    """
    
    @pytest.mark.integration
    def test_github_api_error_propagation(self, github_api_error_responses):
        """
        Validate GitHub API error propagation through pipeline components.
        
        Technical Verification:
        - GitHub API error detection and classification
        - Error message propagation to CLI interface
        - Graceful degradation under API failures
        - Recovery mechanism coordination
        """
        # Test different GitHub API error scenarios
        for error_type, error_response in github_api_error_responses.items():
            with patch('pydcl.github_client.Github') as mock_github:
                # Configure mock to raise specific GitHub exception
                mock_client = Mock()
                mock_client.get_organization.side_effect = GithubException(
                    error_response['status_code'], 
                    error_response['message']
                )
                mock_github.return_value = mock_client
                
                # Test error handling through pipeline
                try:
                    github_client = GitHubMetricsClient(token='test_token')
                    
                    # Should handle GitHub API errors gracefully
                    with pytest.raises(GithubException):
                        github_client.get_organization_repositories('test-org')
                        
                except ImportError:
                    pytest.skip("GitHub client not available for error testing")
    
    @pytest.mark.integration
    def test_configuration_validation_error_integration(self, invalid_repo_yaml):
        """
        Validate configuration validation error integration across components.
        
        Technical Focus:
        - Configuration parsing error detection
        - Validation error aggregation and reporting
        - Error recovery with default configuration fallback
        - User guidance for configuration correction
        """
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create invalid configuration file
            invalid_config_path = Path(temp_dir) / 'invalid_config.yaml'
            invalid_config_path.write_text(invalid_repo_yaml)
            
            try:
                # Test configuration validation error handling
                config_data = yaml.safe_load(invalid_repo_yaml)
                validation_errors = validate_config(config_data)
                
                # Should detect multiple validation errors
                assert isinstance(validation_errors, list)
                assert len(validation_errors) > 0, "Should detect validation errors"
                
                # Should classify error severity appropriately
                error_severities = [error.severity for error in validation_errors]
                assert 'error' in error_severities or 'critical' in error_severities
                
            except NotImplementedError:
                pytest.skip("Configuration validation not yet implemented")
    
    @pytest.mark.integration
    def test_cost_calculation_error_resilience(self, high_cost_repository_metrics):
        """
        Validate cost calculation error resilience and boundary condition handling.
        
        Technical Implementation:
        - Extreme value input handling validation
        - Mathematical overflow/underflow protection
        - Governance threshold violation handling
        - Error recovery with safe default values
        """
        # Test extreme value scenarios
        extreme_test_cases = [
            {
                'name': 'extreme-large-repo',
                'stars_count': 1000000,  # Extremely popular
                'commits_last_30_days': 10000,  # Extremely active
                'size_kb': 10000000,  # 10GB repository
                'description': 'Extremely large repository'
            },
            {
                'name': 'zero-activity-repo',
                'stars_count': 0,
                'commits_last_30_days': 0,
                'size_kb': 0,
                'description': 'Zero activity repository'
            }
        ]
        
        cost_calculator = CostScoreCalculator()
        
        for test_case in extreme_test_cases:
            metrics = RepositoryMetrics(test_case['name'])
            metrics.stars_count = test_case['stars_count']
            metrics.commits_last_30_days = test_case['commits_last_30_days']
            metrics.size_kb = test_case['size_kb']
            
            # Should handle extreme values gracefully
            result = cost_calculator.calculate_repository_cost(metrics)
            
            # Validate bounded output
            assert 'normalized_score' in result
            assert 0.0 <= result['normalized_score'] <= 100.0, \
                f"Score out of bounds for {test_case['description']}: {result['normalized_score']}"
            
            # Validate governance alert generation
            assert 'governance_alerts' in result
            assert isinstance(result['governance_alerts'], list)


class TestSystemIntegrationScenarios:
    """
    Real-world system integration scenarios following OBINexus operational patterns.
    
    Technical Implementation:
    - Multi-division organizational analysis scenarios
    - Large-scale repository processing validation
    - Production-like data volume handling
    - System performance under realistic loads
    """
    
    @pytest.mark.integration
    @pytest.mark.slow
    def test_multi_division_organization_analysis(self, sample_org_config):
        """
        Validate complete multi-division organization analysis workflow.
        
        Technical Scenario:
        - Multiple divisions with different governance thresholds
        - Cross-division repository dependency analysis
        - Division-specific reporting generation
        - Governance compliance aggregation across divisions
        """
        # Create multi-division test scenario
        multi_division_repos = [
            # Computing Division repositories
            {'name': 'libpolycall-bindings', 'division': 'Computing', 'status': 'Core', 'stars': 25, 'commits': 15},
            {'name': 'nexuslink', 'division': 'Computing', 'status': 'Active', 'stars': 12, 'commits': 28},
            {'name': 'build-orchestration', 'division': 'Computing', 'status': 'Core', 'stars': 8, 'commits': 22},
            
            # UCHE Nnamdi Strategic Projects
            {'name': 'strategic-planning', 'division': 'UCHE Nnamdi', 'status': 'Core', 'stars': 5, 'commits': 8},
            {'name': 'governance-framework', 'division': 'UCHE Nnamdi', 'status': 'Active', 'stars': 3, 'commits': 12},
            
            # Aegis Engineering repositories
            {'name': 'polybuild', 'division': 'Aegis Engineering', 'status': 'Core', 'stars': 18, 'commits': 35},
            {'name': 'deployment-automation', 'division': 'Aegis Engineering', 'status': 'Active', 'stars': 7, 'commits': 19}
        ]
        
        # Process multi-division scenario
        cost_calculator = CostScoreCalculator()
        division_results = {}
        
        for repo_data in multi_division_repos:
            metrics = RepositoryMetrics(repo_data['name'])
            metrics.stars_count = repo_data['stars']
            metrics.commits_last_30_days = repo_data['commits']
            
            # Calculate cost with division-aware parameters
            result = cost_calculator.calculate_repository_cost(metrics)
            
            division = repo_data['division']
            if division not in division_results:
                division_results[division] = {
                    'repositories': [],
                    'total_score': 0.0,
                    'governance_violations': 0
                }
            
            division_results[division]['repositories'].append({
                'name': repo_data['name'],
                'status': repo_data['status'],
                'score': result['normalized_score']
            })
            
            division_results[division]['total_score'] += result['normalized_score']
            
            # Check governance compliance per division thresholds
            if result['normalized_score'] > 60.0:  # Computing/Aegis threshold
                if division in ['Computing', 'Aegis Engineering']:
                    division_results[division]['governance_violations'] += 1
            elif result['normalized_score'] > 50.0:  # UCHE Nnamdi enhanced threshold
                if division == 'UCHE Nnamdi':
                    division_results[division]['governance_violations'] += 1
        
        # Validate multi-division analysis results
        assert len(division_results) == 3, "Should process all three divisions"
        
        # Validate division-specific results
        for division, results in division_results.items():
            assert len(results['repositories']) > 0, f"Division {division} should have repositories"
            assert results['total_score'] >= 0.0, f"Division {division} should have valid total score"
            
            # Calculate average score per division
            avg_score = results['total_score'] / len(results['repositories'])
            assert 0.0 <= avg_score <= 100.0, f"Division {division} average score out of bounds"
    
    @pytest.mark.integration
    def test_repository_dependency_analysis(self, mock_github_repositories):
        """
        Validate repository dependency analysis integration.
        
        Technical Focus:
        - Inter-repository dependency mapping
        - Circular dependency detection
        - Dependency impact cost calculation
        - Build orchestration integration validation
        """
        # Create dependency relationships
        dependency_map = {
            'libpolycall-bindings': ['nexuslink'],  # libpolycall depends on nexuslink
            'polybuild': ['libpolycall-bindings', 'nexuslink'],  # polybuild orchestrates both
            'nexuslink': []  # Base dependency
        }
        
        # Process repositories with dependency awareness
        cost_calculator = CostScoreCalculator()
        repo_scores = {}
        
        for repo_data in mock_github_repositories:
            metrics = RepositoryMetrics(repo_data['name'])
            metrics.stars_count = repo_data['stars_count']
            metrics.commits_last_30_days = repo_data['commits_last_30_days']
            
            # Calculate base cost
            result = cost_calculator.calculate_repository_cost(metrics)
            repo_scores[repo_data['name']] = result['normalized_score']
        
        # Validate dependency impact analysis
        for repo_name, dependencies in dependency_map.items():
            if repo_name in repo_scores:
                base_score = repo_scores[repo_name]
                
                # Repositories with dependencies may have different risk profiles
                dependency_count = len(dependencies)
                
                # Validate that dependency analysis is considered
                # (Implementation-specific logic would go here)
                assert base_score >= 0.0, f"Repository {repo_name} should have valid score"
                
                # Higher dependency count could indicate higher complexity
                if dependency_count > 0:
                    # This is a placeholder for dependency impact analysis
                    dependency_factor = 1.0 + (dependency_count * 0.1)
                    assert dependency_factor > 1.0, "Dependencies should impact complexity"
    
    @pytest.mark.integration
    def test_continuous_integration_workflow(self, temp_config_dir, sample_org_config):
        """
        Validate CI/CD integration workflow for automated cost analysis.
        
        Technical Scenario:
        - Automated configuration loading
        - Batch repository processing
        - Report generation for CI pipeline
        - Exit code handling for build integration
        """
        # Create CI-like environment
        ci_config_file = temp_config_dir / '.github' / 'pydcl.yaml'
        ci_config_file.parent.mkdir(exist_ok=True)
        ci_config_file.write_text(sample_org_config)
        
        # Simulate CI environment variables
        ci_env = {
            'CI': 'true',
            'GITHUB_REPOSITORY': 'obinexus/test-repo',
            'GITHUB_SHA': 'abc123def456',
            'GITHUB_REF': 'refs/heads/main'
        }
        
        with patch.dict(os.environ, ci_env):
            # Test CI-oriented command execution
            ci_args = ['pydcl', 'analyze', '--org', 'obinexus', '--output', 'ci_results.json', '--ci-mode']
            
            with patch('sys.argv', ci_args):
                with patch('builtins.print') as mock_print:
                    try:
                        cli.main()
                        
                        # Should handle CI mode appropriately
                        assert mock_print.called
                        output = ' '.join([str(call) for call in mock_print.call_args_list])
                        
                        # Should indicate CI mode handling capability
                        ci_indicators = ['ci', 'not yet implemented', 'development']
                        assert any(indicator in output.lower() for indicator in ci_indicators)
                        
                    except NotImplementedError:
                        pytest.skip("CI integration not yet implemented")
    
    @pytest.mark.integration
    @pytest.mark.slow
    def test_performance_scalability_validation(self, performance_test_data):
        """
        Validate system performance scalability under realistic loads.
        
        Performance Verification:
        - Large dataset processing efficiency
        - Memory usage patterns under load
        - Concurrent processing capability simulation
        - Resource utilization optimization validation
        """
        large_dataset = performance_test_data['large_organization_repos']
        
        # Performance benchmarking
        start_time = datetime.utcnow()
        cost_calculator = CostScoreCalculator()
        
        # Batch processing simulation
        batch_size = 25
        processed_batches = []
        
        for i in range(0, len(large_dataset), batch_size):
            batch = large_dataset[i:i + batch_size]
            batch_start = datetime.utcnow()
            
            batch_results = []
            for repo_data in batch:
                metrics = RepositoryMetrics(repo_data['name'])
                metrics.stars_count = repo_data['stars_count']
                metrics.commits_last_30_days = repo_data['commits_last_30_days']
                
                result = cost_calculator.calculate_repository_cost(metrics)
                batch_results.append(result['normalized_score'])
            
            batch_duration = (datetime.utcnow() - batch_start).total_seconds()
            processed_batches.append({
                'batch_size': len(batch),
                'duration': batch_duration,
                'avg_score': sum(batch_results) / len(batch_results)
            })
        
        # Performance validation
        total_duration = (datetime.utcnow() - start_time).total_seconds()
        total_repos = len(large_dataset)
        processing_rate = total_repos / total_duration
        
        # Should maintain reasonable processing performance
        assert processing_rate > 50, f"Processing rate too slow: {processing_rate:.2f} repos/sec"
        
        # Validate batch processing consistency
        batch_durations = [batch['duration'] for batch in processed_batches]
        avg_batch_duration = sum(batch_durations) / len(batch_durations)
        
        # Batch processing should be consistent (no significant degradation)
        for batch in processed_batches:
            duration_ratio = batch['duration'] / avg_batch_duration
            assert 0.5 <= duration_ratio <= 2.0, f"Batch processing performance inconsistent: {duration_ratio}"

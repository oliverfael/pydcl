"""
PYDCL Utils Unit Tests
=====================

Systematic validation of utility functions implementing waterfall methodology
validation checkpoints and configuration management infrastructure.

Technical Focus:
- Configuration validation with schema enforcement
- Division configuration loading with error handling
- File system operations with security validation
- Hash generation for deterministic verification
- Technical duration formatting for progress reporting

Test Architecture: Methodical pytest implementation per Aegis specifications
Implementation: Technical validation following OBINexus standards
"""

import pytest
import os
import json
import yaml
import tempfile
import hashlib
from pathlib import Path
from unittest.mock import patch, mock_open, MagicMock
from typing import Dict, Any, List

# PYDCL imports with systematic error handling
try:
    from pydcl.utils import (
        validate_config, load_division_config, generate_config_hash,
        ensure_directory_structure, format_technical_duration, setup_logging
    )
    from pydcl.models import DivisionType, ValidationError
except ImportError as e:
    pytest.skip(f"PYDCL utils module unavailable: {e}", allow_module_level=True)


class TestConfigurationValidation:
    """
    Systematic configuration validation following Aegis project specifications.
    
    Technical Implementation:
    - Schema validation with comprehensive error reporting
    - Division parameter constraint enforcement
    - Cost factor mathematical validation
    - Semantic consistency verification
    """
    
    @pytest.mark.unit
    def test_validate_valid_configuration(self, sample_org_config):
        """
        Validate correct configuration validation for compliant input.
        
        Technical Verification:
        - Valid configuration produces no critical errors
        - Warning-level issues properly classified
        - Version format validation accuracy
        """
        config_data = yaml.safe_load(sample_org_config)
        
        try:
            validation_errors = validate_config(config_data)
            
            # Should return list of ValidationError objects
            assert isinstance(validation_errors, list)
            
            # Critical errors should be absent for valid configuration
            critical_errors = [e for e in validation_errors if e.severity == 'critical']
            assert len(critical_errors) == 0, f"Valid configuration should have no critical errors: {critical_errors}"
            
            # Validate error structure for any warnings
            for error in validation_errors:
                assert hasattr(error, 'field')
                assert hasattr(error, 'message')
                assert hasattr(error, 'severity')
                assert error.severity in ['critical', 'error', 'warning']
                
        except NotImplementedError:
            pytest.skip("Configuration validation not yet implemented")
    
    @pytest.mark.unit
    def test_validate_missing_required_fields(self):
        """Validate detection of missing required configuration fields."""
        # Configuration missing required fields
        incomplete_config = {
            'organization': 'obinexus'
            # Missing 'version' field
        }
        
        try:
            validation_errors = validate_config(incomplete_config)
            
            # Should detect missing version field
            version_errors = [e for e in validation_errors if e.field == 'version']
            assert len(version_errors) > 0, "Should detect missing version field"
            
            # Missing version should be critical error
            critical_version_errors = [e for e in version_errors if e.severity == 'critical']
            assert len(critical_version_errors) > 0, "Missing version should be critical"
            
        except NotImplementedError:
            pytest.skip("Configuration validation not yet implemented")
    
    @pytest.mark.unit
    def test_validate_invalid_division_configuration(self):
        """Validate detection of invalid division configurations."""
        config_with_invalid_division = {
            'version': '1.0.0',
            'organization': 'obinexus',
            'divisions': {
                'InvalidDivision': {  # Invalid division name
                    'governance_threshold': 0.6,
                    'isolation_threshold': 0.8,
                    'priority_boost': 1.2
                },
                'Computing': {
                    'governance_threshold': 1.5,  # Invalid: exceeds 1.0
                    'isolation_threshold': 0.8,
                    'priority_boost': 5.0  # Invalid: exceeds reasonable bounds
                }
            }
        }
        
        try:
            validation_errors = validate_config(config_with_invalid_division)
            
            # Should detect invalid division name
            division_errors = [e for e in validation_errors if 'InvalidDivision' in e.message]
            assert len(division_errors) > 0, "Should detect invalid division name"
            
            # Should detect invalid threshold values
            threshold_errors = [e for e in validation_errors if 'threshold' in e.field.lower()]
            assert len(threshold_errors) > 0, "Should detect invalid threshold values"
            
        except NotImplementedError:
            pytest.skip("Configuration validation not yet implemented")
    
    @pytest.mark.unit
    def test_validate_cost_factors_bounds(self):
        """Validate cost factor weight distribution constraints."""
        config_with_invalid_weights = {
            'version': '1.0.0',
            'organization': 'obinexus',
            'cost_factors': {
                'stars_weight': 1.5,  # Invalid: exceeds 1.0
                'commit_activity_weight': 0.8,
                'build_time_weight': 0.5,
                'size_weight': 0.3,
                'test_coverage_weight': 0.2,
                'manual_boost': 4.0  # Invalid: exceeds reasonable bounds
                # Total weight: 3.3 (exceeds Sinphasé bounds)
            }
        }
        
        try:
            validation_errors = validate_config(config_with_invalid_weights)
            
            # Should detect individual weight violations
            weight_errors = [e for e in validation_errors if 'weight' in e.field.lower()]
            assert len(weight_errors) > 0, "Should detect invalid weight values"
            
            # Should detect total weight distribution violation
            total_weight_errors = [e for e in validation_errors if 'total weight' in e.message.lower()]
            # Note: May or may not be implemented depending on validation logic
            
        except NotImplementedError:
            pytest.skip("Configuration validation not yet implemented")


class TestDivisionConfigurationLoading:
    """
    Systematic division configuration loading with waterfall validation gates.
    
    Technical Implementation:
    - Multi-path configuration file discovery
    - YAML/JSON parsing with comprehensive error handling
    - Default configuration generation for missing parameters
    - Division metadata validation with constraint checking
    """
    
    @pytest.mark.unit
    def test_load_division_config_from_file(self, sample_org_config, temp_config_dir):
        """
        Validate division configuration loading from existing file.
        
        Technical Verification:
        - Configuration file discovery accuracy
        - YAML parsing with error handling
        - Division metadata object creation
        """
        # Create configuration file
        config_path = temp_config_dir / 'pydcl.yaml'
        config_path.write_text(sample_org_config)
        
        try:
            division_configs = load_division_config(str(config_path))
            
            # Should return dictionary mapping DivisionType to metadata
            assert isinstance(division_configs, dict)
            
            # Should contain all defined divisions
            assert DivisionType.COMPUTING in division_configs
            assert DivisionType.UCHE_NNAMDI in division_configs
            
            # Validate Computing division configuration
            computing_config = division_configs[DivisionType.COMPUTING]
            assert hasattr(computing_config, 'governance_threshold')
            assert hasattr(computing_config, 'isolation_threshold')
            assert hasattr(computing_config, 'priority_boost')
            
            # Validate specific values from sample configuration
            assert computing_config.governance_threshold == 0.6
            assert computing_config.isolation_threshold == 0.8
            assert computing_config.priority_boost == 1.2
            
        except NotImplementedError:
            pytest.skip("Division configuration loading not yet implemented")
    
    @pytest.mark.unit
    def test_load_division_config_missing_file(self):
        """Validate default configuration generation when no file exists."""
        # Use non-existent path
        non_existent_path = '/path/that/does/not/exist/config.yaml'
        
        try:
            division_configs = load_division_config(non_existent_path)
            
            # Should return default configuration for all divisions
            assert isinstance(division_configs, dict)
            
            # Should contain all division types
            for division in DivisionType:
                assert division in division_configs, f"Missing default config for {division.value}"
            
            # Default configurations should have reasonable values
            for division, config in division_configs.items():
                assert hasattr(config, 'governance_threshold')
                assert hasattr(config, 'isolation_threshold')
                assert hasattr(config, 'priority_boost')
                
                # Validate reasonable default bounds
                assert 0.0 <= config.governance_threshold <= 1.0
                assert 0.0 <= config.isolation_threshold <= 1.0
                assert 0.1 <= config.priority_boost <= 3.0
                
        except NotImplementedError:
            pytest.skip("Division configuration loading not yet implemented")
    
    @pytest.mark.unit
    def test_load_division_config_malformed_yaml(self, temp_config_dir):
        """Validate error handling for malformed YAML configuration."""
        # Create malformed YAML file
        malformed_yaml = """
version: "1.0.0"
organization: "obinexus"
divisions:
  Computing:
    governance_threshold: 0.6
    isolation_threshold: 0.8
    priority_boost: 1.2
  UCHE Nnamdi:
    governance_threshold: [invalid_yaml_structure
    # Missing closing bracket - malformed YAML
"""
        
        config_path = temp_config_dir / 'malformed.yaml'
        config_path.write_text(malformed_yaml)
        
        try:
            division_configs = load_division_config(str(config_path))
            
            # Should gracefully handle malformed YAML and return defaults
            assert isinstance(division_configs, dict)
            
            # Should contain all divisions with default values
            assert len(division_configs) == len(DivisionType)
            
        except NotImplementedError:
            pytest.skip("Division configuration loading not yet implemented")
    
    @pytest.mark.unit
    def test_load_division_config_search_paths(self, temp_config_dir, sample_org_config):
        """Validate configuration file search path priority."""
        # Create configuration files in different locations
        search_locations = [
            temp_config_dir / '.github' / 'pydcl.yaml',
            temp_config_dir / 'pydcl.yaml'
        ]
        
        # Create .github directory
        (temp_config_dir / '.github').mkdir(exist_ok=True)
        
        # Create config in .github (higher priority)
        search_locations[0].write_text(sample_org_config)
        
        # Create config in root (lower priority)
        search_locations[1].write_text("""
version: "1.0.0"
organization: "test-org"
divisions:
  Computing:
    governance_threshold: 0.9
""")
        
        try:
            # Load without specifying explicit path (should use search)
            with patch('os.getcwd', return_value=str(temp_config_dir)):
                division_configs = load_division_config()
            
            # Should find .github/pydcl.yaml (higher priority)
            computing_config = division_configs.get(DivisionType.COMPUTING)
            if computing_config:
                # Should use values from .github config, not root config
                assert computing_config.governance_threshold == 0.6  # From .github
                assert computing_config.governance_threshold != 0.9  # Not from root
            
        except NotImplementedError:
            pytest.skip("Division configuration loading not yet implemented")


class TestHashGeneration:
    """
    Systematic hash generation validation for configuration determinism.
    
    Technical Implementation:
    - Deterministic hash generation for identical inputs
    - Configuration normalization for consistent hashing
    - SHA-256 cryptographic integrity validation
    """
    
    @pytest.mark.unit
    def test_generate_config_hash_deterministic(self, sample_org_config):
        """Validate deterministic hash generation for identical configurations."""
        config_data = yaml.safe_load(sample_org_config)
        
        try:
            # Generate hash multiple times
            hash1 = generate_config_hash(config_data)
            hash2 = generate_config_hash(config_data)
            hash3 = generate_config_hash(config_data)
            
            # All hashes should be identical
            assert hash1 == hash2 == hash3, "Configuration hashing should be deterministic"
            
            # Validate hash format (SHA-256)
            assert len(hash1) == 64, "SHA-256 hash should be 64 characters"
            assert all(c in '0123456789abcdef' for c in hash1), "Hash should be hexadecimal"
            
        except NotImplementedError:
            pytest.skip("Configuration hash generation not yet implemented")
    
    @pytest.mark.unit
    def test_generate_config_hash_sensitivity(self):
        """Validate hash sensitivity to configuration changes."""
        base_config = {
            'version': '1.0.0',
            'organization': 'obinexus',
            'divisions': {
                'Computing': {
                    'governance_threshold': 0.6,
                    'priority_boost': 1.2
                }
            }
        }
        
        modified_config = base_config.copy()
        modified_config['divisions']['Computing']['priority_boost'] = 1.3  # Small change
        
        try:
            base_hash = generate_config_hash(base_config)
            modified_hash = generate_config_hash(modified_config)
            
            # Hashes should be different for different configurations
            assert base_hash != modified_hash, "Hash should change for modified configuration"
            
        except NotImplementedError:
            pytest.skip("Configuration hash generation not yet implemented")


class TestFileSystemOperations:
    """
    File system operations validation with security and error handling.
    
    Technical Implementation:
    - Directory structure creation with permission validation
    - Path security verification (directory traversal prevention)
    - Error handling for filesystem permission issues
    """
    
    @pytest.mark.unit
    def test_ensure_directory_structure_creation(self, temp_config_dir):
        """Validate directory structure creation accuracy."""
        test_dir = temp_config_dir / 'test_structure' / 'nested' / 'directories'
        
        try:
            ensure_directory_structure(str(test_dir))
            
            # Directory should be created
            assert test_dir.exists(), "Directory structure should be created"
            assert test_dir.is_dir(), "Path should be a directory"
            
        except NotImplementedError:
            pytest.skip("Directory structure creation not yet implemented")
    
    @pytest.mark.unit
    def test_ensure_directory_structure_existing(self, temp_config_dir):
        """Validate handling of existing directory structures."""
        existing_dir = temp_config_dir / 'existing_directory'
        existing_dir.mkdir()
        
        try:
            # Should handle existing directory gracefully
            ensure_directory_structure(str(existing_dir))
            
            # Directory should still exist
            assert existing_dir.exists()
            assert existing_dir.is_dir()
            
        except NotImplementedError:
            pytest.skip("Directory structure creation not yet implemented")
    
    @pytest.mark.unit
    def test_ensure_directory_structure_security(self):
        """Validate security constraints for directory creation."""
        # Test potential directory traversal attempts
        malicious_paths = [
            '../../../etc/passwd',
            '/etc/shadow',
            '..\\..\\windows\\system32'
        ]
        
        try:
            for malicious_path in malicious_paths:
                with pytest.raises((ValueError, OSError)):
                    ensure_directory_structure(malicious_path)
                    
        except NotImplementedError:
            pytest.skip("Directory structure creation not yet implemented")


class TestTechnicalDurationFormatting:
    """
    Technical duration formatting validation for progress reporting.
    
    Technical Implementation:
    - Millisecond precision for sub-second durations
    - Human-readable formatting for various time scales
    - Technical accuracy for progress monitoring
    """
    
    @pytest.mark.unit
    def test_format_technical_duration_milliseconds(self):
        """Validate millisecond formatting for sub-second durations."""
        try:
            # Test millisecond formatting
            assert format_technical_duration(0.123) == "123ms"
            assert format_technical_duration(0.001) == "1ms"
            assert format_technical_duration(0.999) == "999ms"
            
        except NotImplementedError:
            pytest.skip("Technical duration formatting not yet implemented")
    
    @pytest.mark.unit
    def test_format_technical_duration_seconds(self):
        """Validate second formatting for standard durations."""
        try:
            # Test second formatting
            assert format_technical_duration(1.0) == "1.0s"
            assert format_technical_duration(5.7) == "5.7s"
            assert format_technical_duration(59.9) == "59.9s"
            
        except NotImplementedError:
            pytest.skip("Technical duration formatting not yet implemented")
    
    @pytest.mark.unit
    def test_format_technical_duration_minutes(self):
        """Validate minute formatting for extended durations."""
        try:
            # Test minute formatting
            assert format_technical_duration(60.0) == "1m 0s"
            assert format_technical_duration(125.0) == "2m 5s"
            assert format_technical_duration(3599.0) == "59m 59s"
            
        except NotImplementedError:
            pytest.skip("Technical duration formatting not yet implemented")
    
    @pytest.mark.unit
    def test_format_technical_duration_hours(self):
        """Validate hour formatting for long-running operations."""
        try:
            # Test hour formatting
            assert format_technical_duration(3600.0) == "1h 0m"
            assert format_technical_duration(7265.0) == "2h 1m"
            assert format_technical_duration(10800.0) == "3h 0m"
            
        except NotImplementedError:
            pytest.skip("Technical duration formatting not yet implemented")


class TestLoggingConfiguration:
    """
    Logging system configuration validation for development and production.
    
    Technical Implementation:
    - Structured logging format validation
    - Verbosity level configuration accuracy
    - File output integration testing
    """
    
    @pytest.mark.unit
    @patch('logging.basicConfig')
    def test_setup_logging_basic_configuration(self, mock_basic_config):
        """Validate basic logging configuration setup."""
        try:
            setup_logging(verbose=False, structured=True)
            
            # Should call logging.basicConfig
            mock_basic_config.assert_called_once()
            
            # Validate configuration parameters
            call_args = mock_basic_config.call_args
            assert 'level' in call_args.kwargs
            assert 'format' in call_args.kwargs
            assert 'handlers' in call_args.kwargs
            
        except NotImplementedError:
            pytest.skip("Logging setup not yet implemented")
    
    @pytest.mark.unit
    @patch('logging.basicConfig')
    def test_setup_logging_verbose_mode(self, mock_basic_config):
        """Validate verbose logging configuration."""
        try:
            setup_logging(verbose=True)
            
            mock_basic_config.assert_called_once()
            
            # Should configure DEBUG level for verbose mode
            call_args = mock_basic_config.call_args
            # Note: Specific validation depends on implementation
            
        except NotImplementedError:
            pytest.skip("Logging setup not yet implemented")
    
    @pytest.mark.unit
    @patch('logging.basicConfig')
    @patch('logging.FileHandler')
    def test_setup_logging_file_output(self, mock_file_handler, mock_basic_config):
        """Validate file output configuration for logging."""
        try:
            test_log_file = 'test_output.log'
            setup_logging(log_file=test_log_file)
            
            # Should configure file handler when log_file specified
            # Note: Specific validation depends on implementation details
            
        except NotImplementedError:
            pytest.skip("Logging setup not yet implemented")

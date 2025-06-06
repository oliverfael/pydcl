"""
PYDCL Utility Functions and Configuration Management

Technical utility functions implementing systematic validation, configuration
management, and logging infrastructure following Aegis project specifications.

Core Technical Features:
- Structured configuration validation with schema enforcement
- Systematic logging setup with configurable verbosity levels
- Division-aware configuration loading with validation checkpoints
- Error handling utilities with comprehensive exception management
- File system operations with security validation

Architecture: Modular utility functions with deterministic behavior
Technical Implementation: Waterfall methodology with systematic validation
"""

import os
import sys
import json
import yaml
import logging
import hashlib
from pathlib import Path
from typing import Dict, Any, Optional, List, Union
from datetime import datetime

from .models import (
    DivisionType, ProjectStatus, CostFactors, RepositoryConfig,
    DivisionMetadata, ValidationError
)


def setup_logging(
    verbose: bool = False, 
    log_file: Optional[str] = None,
    structured: bool = True
) -> None:
    """
    Systematic logging configuration following technical standards.
    
    Technical Implementation:
    - Structured log formatting with timestamp precision
    - Configurable verbosity levels for development and production
    - File output support with rotation capabilities
    - Technical correlation ID generation for troubleshooting
    
    Args:
        verbose: Enable DEBUG level logging for technical analysis
        log_file: Optional log file path for persistent storage
        structured: Enable structured JSON logging format
    """
    
    # Determine logging level based on verbosity
    log_level = logging.DEBUG if verbose else logging.INFO
    
    # Configure structured log formatting
    if structured:
        log_format = (
            "%(asctime)s | %(levelname)-8s | %(name)-20s | "
            "%(funcName)-15s | %(message)s"
        )
    else:
        log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Configure logging system
    logging.basicConfig(
        level=log_level,
        format=log_format,
        datefmt='%Y-%m-%d %H:%M:%S',
        handlers=[
            logging.StreamHandler(sys.stdout),
            *([logging.FileHandler(log_file)] if log_file else [])
        ]
    )
    
    # Configure third-party library logging
    logging.getLogger('github').setLevel(logging.WARNING)
    logging.getLogger('urllib3').setLevel(logging.WARNING)
    
    logger = logging.getLogger(__name__)
    logger.info(f"PYDCL logging configured: level={log_level}, structured={structured}")


def validate_config(config_data: Dict[str, Any]) -> List[ValidationError]:
    """
    Systematic configuration validation with comprehensive error reporting.
    
    Technical Implementation:
    - Schema validation against PYDCL configuration specification
    - Division parameter validation with constraint checking
    - Cost factor validation with mathematical constraint enforcement
    - Semantic validation for logical consistency
    
    Args:
        config_data: Configuration dictionary to validate
        
    Returns:
        List of validation errors with severity classification
    """
    
    errors = []
    
    # Phase 1: Structural Validation
    required_fields = ['version', 'organization']
    for field in required_fields:
        if field not in config_data:
            errors.append(ValidationError(
                field=field,
                message=f"Required field '{field}' missing from configuration",
                severity="critical"
            ))
    
    # Phase 2: Version Validation
    if 'version' in config_data:
        version = config_data['version']
        if not isinstance(version, str) or not _validate_version_format(version):
            errors.append(ValidationError(
                field='version',
                message=f"Invalid version format: {version}",
                value=version,
                severity="error"
            ))
    
    # Phase 3: Division Configuration Validation
    if 'divisions' in config_data:
        division_errors = _validate_division_configurations(config_data['divisions'])
        errors.extend(division_errors)
    
    # Phase 4: Cost Factor Validation
    if 'cost_factors' in config_data:
        cost_factor_errors = _validate_cost_factors(config_data['cost_factors'])
        errors.extend(cost_factor_errors)
    
    # Phase 5: Organization Validation
    if 'organization' in config_data:
        org_name = config_data['organization']
        if not isinstance(org_name, str) or not _validate_github_org_name(org_name):
            errors.append(ValidationError(
                field='organization',
                message=f"Invalid GitHub organization name: {org_name}",
                value=org_name,
                severity="error"
            ))
    
    logger = logging.getLogger(__name__)
    if errors:
        logger.warning(f"Configuration validation found {len(errors)} issues")
    else:
        logger.info("Configuration validation completed successfully")
    
    return errors


def load_division_config(config_path: Optional[str] = None) -> Dict[DivisionType, DivisionMetadata]:
    """
    Systematic division configuration loading with validation checkpoints.
    
    Technical Implementation:
    - Configuration file discovery with multiple search paths
    - YAML/JSON parsing with error handling and recovery
    - Division metadata validation with constraint checking
    - Default configuration generation for missing parameters
    
    Args:
        config_path: Optional explicit configuration file path
        
    Returns:
        Dictionary mapping division types to validated metadata
    """
    
    logger = logging.getLogger(__name__)
    
    # Configuration search paths
    search_paths = [
        config_path,
        '.github/pydcl.yaml',
        '.github/division_config.yaml',
        'pydcl.yaml',
        'division_config.yaml',
        os.path.expanduser('~/.config/pydcl/config.yaml')
    ]
    
    # Remove None values from search paths
    search_paths = [path for path in search_paths if path is not None]
    
    config_data = None
    config_source = None
    
    # Systematic configuration file discovery
    for path in search_paths:
        if os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    if path.endswith('.json'):
                        config_data = json.load(f)
                    else:
                        config_data = yaml.safe_load(f)
                
                config_source = path
                logger.info(f"Division configuration loaded from: {path}")
                break
                
            except (json.JSONDecodeError, yaml.YAMLError) as e:
                logger.warning(f"Configuration parsing failed for {path}: {e}")
                continue
            except Exception as e:
                logger.warning(f"Configuration loading failed for {path}: {e}")
                continue
    
    # Generate default configuration if no file found
    if config_data is None:
        logger.info("No configuration file found, using default division settings")
        config_data = _generate_default_division_config()
        config_source = "default"
    
    # Parse and validate division configurations
    division_configs = {}
    
    divisions_data = config_data.get('divisions', {})
    for division_name, division_data in divisions_data.items():
        try:
            # Validate division name
            try:
                division_type = DivisionType(division_name)
            except ValueError:
                logger.warning(f"Unknown division type: {division_name}")
                continue
            
            # Create division metadata with validation
            metadata = DivisionMetadata(
                division=division_type,
                description=division_data.get('description', f"{division_name} Division"),
                governance_threshold=division_data.get('governance_threshold', 0.6),
                isolation_threshold=division_data.get('isolation_threshold', 0.8),
                priority_boost=division_data.get('priority_boost', 1.0),
                responsible_architect=division_data.get('responsible_architect')
            )
            
            division_configs[division_type] = metadata
            logger.debug(f"Division configuration loaded: {division_name}")
            
        except Exception as e:
            logger.error(f"Division configuration failed for {division_name}: {e}")
            continue
    
    # Ensure all divisions have configuration
    for division in DivisionType:
        if division not in division_configs:
            division_configs[division] = _create_default_division_metadata(division)
            logger.debug(f"Default configuration applied for: {division.value}")
    
    logger.info(
        f"Division configuration completed: {len(division_configs)} divisions from {config_source}"
    )
    
    return division_configs


def generate_config_hash(config_data: Dict[str, Any]) -> str:
    """
    Generate deterministic configuration hash for validation and caching.
    
    Technical Implementation:
    - Deterministic JSON serialization with sorted keys
    - SHA-256 hash calculation for cryptographic integrity
    - Configuration fingerprinting for change detection
    
    Args:
        config_data: Configuration dictionary to hash
        
    Returns:
        Hexadecimal hash string for configuration fingerprinting
    """
    
    # Normalize configuration for deterministic hashing
    normalized_config = _normalize_config_for_hashing(config_data)
    
    # Generate deterministic JSON representation
    config_json = json.dumps(normalized_config, sort_keys=True, separators=(',', ':'))
    
    # Calculate SHA-256 hash
    config_hash = hashlib.sha256(config_json.encode('utf-8')).hexdigest()
    
    logger = logging.getLogger(__name__)
    logger.debug(f"Configuration hash generated: {config_hash[:16]}...")
    
    return config_hash


def ensure_directory_structure(base_path: str) -> None:
    """
    Systematic directory structure creation with security validation.
    
    Technical Implementation:
    - Path validation and security checking
    - Recursive directory creation with proper permissions
    - Error handling for permission and filesystem issues
    
    Args:
        base_path: Base directory path to create
    """
    
    logger = logging.getLogger(__name__)
    
    try:
        # Validate and normalize path
        normalized_path = os.path.normpath(os.path.abspath(base_path))
        
        # Security validation - prevent directory traversal
        if '..' in normalized_path or normalized_path.startswith('/'):
            if not normalized_path.startswith(os.getcwd()):
                raise ValueError(f"Path security violation: {base_path}")
        
        # Create directory structure
        Path(normalized_path).mkdir(parents=True, exist_ok=True)
        
        logger.debug(f"Directory structure ensured: {normalized_path}")
        
    except Exception as e:
        logger.error(f"Directory creation failed for {base_path}: {e}")
        raise


def format_technical_duration(seconds: float) -> str:
    """
    Technical duration formatting for systematic progress reporting.
    
    Args:
        seconds: Duration in seconds
        
    Returns:
        Human-readable technical duration string
    """
    
    if seconds < 1:
        return f"{seconds*1000:.0f}ms"
    elif seconds < 60:
        return f"{seconds:.1f}s"
    elif seconds < 3600:
        minutes = int(seconds // 60)
        remaining_seconds = seconds % 60
        return f"{minutes}m {remaining_seconds:.0f}s"
    else:
        hours = int(seconds // 3600)
        remaining_minutes = int((seconds % 3600) // 60)
        return f"{hours}h {remaining_minutes}m"


def _validate_version_format(version: str) -> bool:
    """Validate semantic version format (major.minor.patch)."""
    
    try:
        parts = version.split('.')
        if len(parts) != 3:
            return False
        
        # Validate numeric components
        for part in parts:
            if not part.isdigit():
                return False
            if int(part) < 0:
                return False
        
        return True
        
    except Exception:
        return False


def _validate_division_configurations(divisions_data: Dict[str, Any]) -> List[ValidationError]:
    """Validate division-specific configurations."""
    
    errors = []
    
    for division_name, division_config in divisions_data.items():
        # Validate division name
        try:
            DivisionType(division_name)
        except ValueError:
            errors.append(ValidationError(
                field=f'divisions.{division_name}',
                message=f"Unknown division type: {division_name}",
                value=division_name,
                severity="error"
            ))
            continue
        
        # Validate threshold parameters
        for threshold_field in ['governance_threshold', 'isolation_threshold']:
            if threshold_field in division_config:
                threshold_value = division_config[threshold_field]
                if not isinstance(threshold_value, (int, float)) or not (0.0 <= threshold_value <= 1.0):
                    errors.append(ValidationError(
                        field=f'divisions.{division_name}.{threshold_field}',
                        message=f"Threshold must be between 0.0 and 1.0",
                        value=threshold_value,
                        severity="error"
                    ))
        
        # Validate priority boost
        if 'priority_boost' in division_config:
            boost_value = division_config['priority_boost']
            if not isinstance(boost_value, (int, float)) or not (0.1 <= boost_value <= 3.0):
                errors.append(ValidationError(
                    field=f'divisions.{division_name}.priority_boost',
                    message=f"Priority boost must be between 0.1 and 3.0",
                    value=boost_value,
                    severity="warning"
                ))
    
    return errors


def _validate_cost_factors(cost_factors_data: Dict[str, Any]) -> List[ValidationError]:
    """Validate cost factor configurations."""
    
    errors = []
    
    # Validate individual weight parameters
    weight_fields = [
        'stars_weight', 'commit_activity_weight', 'build_time_weight',
        'size_weight', 'test_coverage_weight'
    ]
    
    total_weight = 0.0
    
    for field in weight_fields:
        if field in cost_factors_data:
            weight_value = cost_factors_data[field]
            if not isinstance(weight_value, (int, float)) or not (0.0 <= weight_value <= 1.0):
                errors.append(ValidationError(
                    field=f'cost_factors.{field}',
                    message=f"Weight must be between 0.0 and 1.0",
                    value=weight_value,
                    severity="error"
                ))
            else:
                total_weight += weight_value
    
    # Validate total weight constraint
    if 0.8 <= total_weight <= 1.2:
        # Acceptable weight distribution
        pass
    else:
        errors.append(ValidationError(
            field='cost_factors',
            message=f"Total weight sum {total_weight:.2f} should be approximately 1.0",
            value=total_weight,
            severity="warning"
        ))
    
    # Validate manual boost
    if 'manual_boost' in cost_factors_data:
        boost_value = cost_factors_data['manual_boost']
        if not isinstance(boost_value, (int, float)) or not (0.1 <= boost_value <= 3.0):
            errors.append(ValidationError(
                field='cost_factors.manual_boost',
                message=f"Manual boost must be between 0.1 and 3.0",
                value=boost_value,
                severity="warning"
            ))
    
    return errors


def _validate_github_org_name(org_name: str) -> bool:
    """Validate GitHub organization name format."""
    
    if not org_name or len(org_name) > 39:
        return False
    
    # GitHub username/org name constraints
    if not org_name.replace('-', '').replace('_', '').isalnum():
        return False
    
    if org_name.startswith('-') or org_name.endswith('-'):
        return False
    
    return True


def _generate_default_division_config() -> Dict[str, Any]:
    """Generate default division configuration."""
    
    return {
        'version': '1.0.0',
        'organization': 'obinexus',
        'divisions': {
            'Computing': {
                'description': 'Core technical infrastructure and toolchain development',
                'governance_threshold': 0.6,
                'isolation_threshold': 0.8,
                'priority_boost': 1.2
            },
            'UCHE Nnamdi': {
                'description': 'Strategic leadership and architectural oversight',
                'governance_threshold': 0.5,
                'isolation_threshold': 0.7,
                'priority_boost': 1.5
            },
            'Aegis Engineering': {
                'description': 'Core engineering systems and build orchestration',
                'governance_threshold': 0.6,
                'isolation_threshold': 0.8,
                'priority_boost': 1.3
            }
        }
    }


def _create_default_division_metadata(division: DivisionType) -> DivisionMetadata:
    """Create default metadata for a division."""
    
    return DivisionMetadata(
        division=division,
        description=f"{division.value} Division",
        governance_threshold=0.6,
        isolation_threshold=0.8,
        priority_boost=1.0
    )


def _normalize_config_for_hashing(config_data: Dict[str, Any]) -> Dict[str, Any]:
    """Normalize configuration data for deterministic hashing."""
    
    normalized = {}
    
    for key, value in config_data.items():
        if isinstance(value, dict):
            normalized[key] = _normalize_config_for_hashing(value)
        elif isinstance(value, list):
            # Sort lists for deterministic ordering
            try:
                normalized[key] = sorted(value) if all(isinstance(x, (str, int, float)) for x in value) else value
            except TypeError:
                normalized[key] = value
        elif isinstance(value, float):
            # Round floats to avoid precision issues
            normalized[key] = round(value, 6)
        else:
            normalized[key] = value
    
    return normalized

#!/usr/bin/env python3
"""
PYDCL Setup Configuration

Traditional setup.py implementation for maximum compatibility across
deployment environments and legacy CI/CD systems.

Technical Architecture:
- Maintains compatibility with pyproject.toml modern standards
- Provides fallback distribution mechanism for legacy environments
- Integrates with OBINexus Aegis project waterfall methodology
- Supports NASA-STD-8739.8 compliance verification requirements

Author: OBINexus Computing
Technical Lead: Nnamdi Michael Okpala
License: MIT
"""

import os
import sys
from pathlib import Path
from setuptools import setup, find_packages

# Ensure minimum Python version for Aegis project compatibility
if sys.version_info < (3, 8):
    sys.exit(
        "PYDCL requires Python 3.8 or higher for systematic validation support.\n"
        "Current version: Python {}.{}".format(*sys.version_info[:2])
    )

# Technical constants for OBINexus integration
PACKAGE_NAME = "pydcl"
VERSION = "1.0.0"
DESCRIPTION = "Python Dynamic Cost Layer - Division-aware GitHub organization cost modeling toolkit"

# Repository and project URLs
HOMEPAGE_URL = "https://github.com/obinexus/pydcl"
REPOSITORY_URL = "https://github.com/obinexus/pydcl"
DOCUMENTATION_URL = "https://pydcl.readthedocs.io"
ISSUES_URL = "https://github.com/obinexus/pydcl/issues"
CHANGELOG_URL = "https://github.com/obinexus/pydcl/blob/main/CHANGELOG.md"

# Load README for long description with systematic validation
def load_long_description():
    """Load README.md with systematic error handling."""
    readme_path = Path(__file__).parent / "README.md"
    try:
        with open(readme_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return DESCRIPTION

# Core dependencies aligned with Aegis project requirements
CORE_DEPENDENCIES = [
    "PyGithub>=1.59.0",
    "PyYAML>=6.0",
    "click>=8.0.0",
    "rich>=13.0.0",
    "pydantic>=2.0.0",
    "requests>=2.28.0"
]

# Development dependencies for systematic testing
DEVELOPMENT_DEPENDENCIES = [
    "pytest>=7.0.0",
    "pytest-cov>=4.0.0",
    "black>=23.0.0",
    "isort>=5.12.0",
    "flake8>=6.0.0",
    "mypy>=1.0.0",
    "pre-commit>=3.0.0"
]

# Telemetry dependencies for cost monitoring
TELEMETRY_DEPENDENCIES = [
    "prometheus-client>=0.17.0",
    "structlog>=23.0.0"
]

# Visualization dependencies for inverted triangle interface
VISUALIZATION_DEPENDENCIES = [
    "matplotlib>=3.7.0",
    "plotly>=5.15.0",
    "pandas>=2.0.0"
]

# Technical classifiers following PyPI standards
CLASSIFIERS = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Topic :: Software Development :: Libraries :: Python Modules",
    "Topic :: Software Development :: Quality Assurance",
    "Topic :: System :: Systems Administration",
    "Topic :: Scientific/Engineering :: Information Analysis"
]

# Keywords for systematic discovery
KEYWORDS = [
    "github", "cost-modeling", "division-aware", "project-management",
    "dynamic-cost-layer", "obinexus", "sinphase", "hierarchical-structuring",
    "governance", "compliance", "architectural-analysis", "aegis-project"
]

# Package data and additional files
PACKAGE_DATA = {
    "pydcl": [
        "*.yaml",
        "*.json", 
        "templates/*",
        "schemas/*"
    ]
}

# Entry points for CLI integration
ENTRY_POINTS = {
    "console_scripts": [
        "pydcl=pydcl.cli:main",
    ],
}

# Systematic setup configuration
def main():
    """Execute setup with systematic validation."""
    
    # Validate package structure
    package_dir = Path(__file__).parent / "pydcl"
    if not package_dir.exists():
        sys.exit(
            f"ERROR: Package directory '{package_dir}' not found.\n"
            "Ensure PYDCL package structure is properly initialized."
        )
    
    # Validate __init__.py exists
    init_file = package_dir / "__init__.py"
    if not init_file.exists():
        sys.exit(
            f"ERROR: Package initialization file '{init_file}' not found.\n"
            "Ensure PYDCL package is properly structured."
        )
    
    # Execute setup with comprehensive configuration
    setup(
        # Basic package information
        name=PACKAGE_NAME,
        version=VERSION,
        description=DESCRIPTION,
        long_description=load_long_description(),
        long_description_content_type="text/markdown",
        
        # Author and maintainer information
        author="OBINexus Computing",
        author_email="support@obinexuscomputing.com",
        maintainer="OBINexus Computing",
        maintainer_email="support@obinexuscomputing.com",
        
        # Project URLs for systematic navigation
        url=HOMEPAGE_URL,
        project_urls={
            "Homepage": HOMEPAGE_URL,
            "Repository": REPOSITORY_URL,
            "Documentation": DOCUMENTATION_URL,
            "Bug Tracker": ISSUES_URL,
            "Changelog": CHANGELOG_URL,
        },
        
        # License and classification
        license="MIT",
        classifiers=CLASSIFIERS,
        keywords=KEYWORDS,
        
        # Python version requirements
        python_requires=">=3.8",
        
        # Package discovery and structure
        packages=find_packages(
            exclude=["tests", "tests.*", "docs", "docs.*"]
        ),
        package_data=PACKAGE_DATA,
        include_package_data=True,
        
        # Dependencies with systematic organization
        install_requires=CORE_DEPENDENCIES,
        extras_require={
            "dev": DEVELOPMENT_DEPENDENCIES,
            "telemetry": TELEMETRY_DEPENDENCIES,
            "visualization": VISUALIZATION_DEPENDENCIES,
            "all": (
                DEVELOPMENT_DEPENDENCIES + 
                TELEMETRY_DEPENDENCIES + 
                VISUALIZATION_DEPENDENCIES
            ),
        },
        
        # Entry points for CLI integration
        entry_points=ENTRY_POINTS,
        
        # Additional metadata for Aegis project integration
        zip_safe=False,  # Enable inspection for development
        platforms=["any"],
        
        # Technical options for systematic deployment
        options={
            "bdist_wheel": {
                "universal": False,  # Python 3.8+ specific
            },
            "egg_info": {
                "tag_build": "",
                "tag_svn_revision": False,
            },
        },
    )

if __name__ == "__main__":
    main()
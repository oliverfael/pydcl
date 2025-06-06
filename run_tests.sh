#!/bin/bash
# PYDCL Systematic Test Execution Script
# Technical Lead: Nnamdi Michael Okpala
# Aegis Project Integration Testing

echo "PYDCL Test Execution - Waterfall Methodology Validation"
echo "======================================================="

# Phase 1: Unit Test Validation
echo "Phase 1: Core Component Unit Testing"
pytest tests/unit/ -v -m "unit and not slow" --tb=short

# Phase 2: Integration Gate Validation  
echo "Phase 2: Integration Gateway Testing"
pytest tests/integration/ -v -m "integration" --tb=short

# Phase 3: Echo Integrity Validation
echo "Phase 3: Pipeline Determinism Validation"
pytest tests/ -v -m "echo" --tb=short

# Phase 4: Complete System Validation
echo "Phase 4: Complete System Integration"
pytest tests/ -v --tb=short --cov=pydcl --cov-report=html

echo "Test execution completed. Review reports for validation status."

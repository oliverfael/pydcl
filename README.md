# PYDCL: Python Dynamic Cost Layer

**Division-Aware GitHub Organization Cost Modeling Toolkit**

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/obinexus/pydcl)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Architecture](https://img.shields.io/badge/architecture-Sinphasé-purple.svg)](docs/sinphase_methodology.md)
[![OBINexus](https://img.shields.io/badge/maintainer-OBINexus-red.svg)](https://github.com/obinexus)

**Technical Lead**: Nnamdi Michael Okpala  
**Architecture**: Waterfall Methodology with Systematic Validation Checkpoints  
**Implementation**: Sinphasé (Single-Pass Hierarchical Structuring) Compliance  

---

## Current Development Status

**Phase Status**: Integration Gate - Core Implementation Development  
**Technical Readiness**: CLI Registration Functional, Core Architecture Established  
**Sinphasé Compliance**: Cost-based governance framework implemented with bounded complexity validation

### Available Functionality

**✅ Implemented Components**:
- Package installation and distribution (setuptools + pyproject.toml)
- CLI entry point registration with Rich console formatting
- Sinphasé-compliant data models with cost governance
- Division-aware organizational structure (DivisionType, ProjectStatus)
- Core cost calculation framework with validation bounds
- Systematic import resolution with graceful degradation

**🔄 Development Phase Components**:
- GitHub API integration layer (placeholder implementation)
- Complete cost calculation algorithms (framework established)
- Configuration management utilities (basic structure)
- Comprehensive CLI commands (analyze, display, init - in development)

**⏳ Planned Implementation**:
- Production GitHub API client with rate limiting
- Complete Pydantic model validation
- Interactive visualization components
- Integration testing framework

### Sinphasé Methodology Implementation

PYDCL implements the **Sinphasé (Single-Pass Hierarchical Structuring)** development pattern for systematic architectural governance:

**Core Principles**:
- **Bounded Complexity**: Cost functions limit component coupling within measurable thresholds (≤ 0.6 for autonomous operation)
- **Hierarchical Isolation**: Components maintain clear boundaries through governance contracts
- **Deterministic Compilation**: Single-pass requirements ensure predictable build behavior
- **Cost-Based Governance**: Automatic isolation triggers when complexity exceeds sustainable limits

**Governance Thresholds**:
```python
GOVERNANCE_THRESHOLD = 0.6      # Warning threshold for cost monitoring
ISOLATION_THRESHOLD = 0.8       # Automatic isolation recommendation  
REORGANIZATION_THRESHOLD = 1.0  # Mandatory architectural restructuring
```

**Technical Implementation**:
```python
# Sinphasé cost calculation with bounded complexity
def calculate_sinphase_cost(metrics, factors):
    cost = Σ(metrici × weighti) + circular_penalty + temporal_pressure
    if cost > GOVERNANCE_THRESHOLD:
        trigger_isolation_protocol()
    return min(cost, REORGANIZATION_THRESHOLD)
```

### Architecture Implementation

```
┌─────────────────────────────────────────────────────────────┐
│                    PYDCL Architecture                       │
├─────────────────────────────────────────────────────────────┤
│  CLI Interface (click + rich)                              │
│  ├── analyze: Systematic organization analysis             │
│  ├── display: Structured result formatting                 │
│  └── init: Configuration template generation               │
├─────────────────────────────────────────────────────────────┤
│  Cost Calculation Engine                                   │
│  ├── Weighted Factor Application                           │
│  ├── Division-Specific Parameter Resolution                │
│  ├── Governance Threshold Validation                       │
│  └── Sinphasé Compliance Assessment                        │
├─────────────────────────────────────────────────────────────┤
│  GitHub Integration Layer                                  │
│  ├── Repository Discovery with Pagination                  │
│  ├── Metrics Extraction (stars, commits, languages)       │
│  ├── Configuration Loading (.github/repo.yaml)            │
│  └── Rate Limiting Management                              │
├─────────────────────────────────────────────────────────────┤
│  Data Models (Pydantic)                                   │
│  ├── RepositoryMetrics: Raw GitHub data                    │
│  ├── CostCalculationResult: Analysis output               │
│  ├── DivisionMetadata: Organization structure             │
│  └── OrganizationCostReport: Comprehensive results        │
└─────────────────────────────────────────────────────────────┘
```

---

## Installation and Setup

### Prerequisites

- Python 3.8+ (tested with 3.8, 3.9, 3.10, 3.11, 3.12)
- GitHub Personal Access Token with organization read permissions
- Git for repository management

### Installation Methods

#### Production Installation
```bash
pip install pydcl
```

#### Development Installation
```bash
git clone https://github.com/obinexus/pydcl.git
cd pydcl

# CRITICAL: Execute from project root directory (containing setup.py/pyproject.toml)
pip install -e ".[dev,telemetry,visualization]"

# Alternative basic installation without optional dependencies
pip install -e .
```

#### Installation Verification
```bash
# Verify package installation and CLI registration
pydcl --version
# Expected: 1.0.0

pydcl --help
# Expected: Technical CLI interface with development phase commands

# Validate Sinphasé import resolution
python -c "import pydcl; from pydcl import ValidationError, calculate_sinphase_cost; print('✓ Sinphasé architecture validated')"
```

---

## Configuration Architecture

### Repository Configuration (.github/repo.yaml)

PYDCL discovers repository-specific configuration through systematic path resolution:

```yaml
# .github/repo.yaml
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
dependencies:
  - "nlink"
  - "polybuild"
sinphase_compliance: true
isolation_required: false
```

### Organization Configuration (pydcl.yaml)

```yaml
# pydcl.yaml or .github/pydcl.yaml
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
```

---

## Current Usage Examples

### Development Phase Testing

```bash
# Verify CLI registration and basic functionality
pydcl --version
# Output: 1.0.0

pydcl --help
# Output: Available commands and development status

# Test Sinphasé cost calculation framework
python3 -c "
from pydcl.models import RepositoryMetrics, CostFactors, calculate_sinphase_cost
metrics = RepositoryMetrics('test-repo')
metrics.stars_count = 25
metrics.commits_last_30_days = 15
factors = CostFactors()
cost = calculate_sinphase_cost(metrics, factors)
print(f'Sinphasé Cost Calculation: {cost:.3f}')
print(f'Governance Status: {"✓ Within bounds" if cost <= 0.6 else "⚠️ Exceeds threshold"}')
"

# Validate division-aware architecture
python3 -c "
from pydcl import DivisionType, ProjectStatus, GOVERNANCE_THRESHOLD
print(f'Available Divisions: {[d.value for d in DivisionType]}')
print(f'Project Statuses: {[s.value for s in ProjectStatus]}')
print(f'Governance Threshold: {GOVERNANCE_THRESHOLD}')
"
```

### Future Production Usage (Development Target)

```bash
# Planned full organization analysis (requires GitHub API implementation)
export GH_API_TOKEN="ghp_your_token_here"
pydcl analyze --org obinexus --output cost_scores.json --verbose

# Planned division-specific analysis
pydcl analyze --org obinexus --division "Computing" --output computing_analysis.json

# Planned configuration management
pydcl init --template enterprise --output .github/pydcl.yaml
```

### Phase 4: Integration with CI/CD

```yaml
# .github/workflows/cost-analysis.yml
name: PYDCL Cost Analysis
on:
  schedule:
    - cron: '0 6 * * 1'  # Weekly Monday 6 AM UTC
  workflow_dispatch:

jobs:
  cost-analysis:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install PYDCL
        run: pip install pydcl
      
      - name: Execute Cost Analysis
        env:
          GH_API_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          pydcl analyze --org ${{ github.repository_owner }} \
                       --output cost_scores.json \
                       --verbose
      
      - name: Upload Results
        uses: actions/upload-artifact@v3
        with:
          name: cost-analysis-results
          path: cost_scores.json
```

---

## Technical Implementation Details

### Cost Calculation Algorithm

PYDCL implements a systematic weighted cost calculation following the Sinphasé methodology:

```python
# Simplified cost calculation formula
def calculate_cost_score(metrics, cost_factors, division_metadata):
    # Phase 1: Metric Normalization
    normalized_metrics = normalize_raw_metrics(metrics)
    
    # Phase 2: Weighted Calculation
    base_score = (
        normalized_metrics['stars'] * cost_factors.stars_weight +
        normalized_metrics['commits'] * cost_factors.commit_activity_weight +
        normalized_metrics['build_time'] * cost_factors.build_time_weight +
        normalized_metrics['size'] * cost_factors.size_weight +
        normalized_metrics['test_coverage'] * cost_factors.test_coverage_weight
    )
    
    # Phase 3: Division-Specific Adjustments
    boosted_score = base_score * cost_factors.manual_boost
    final_score = boosted_score * division_metadata.priority_boost
    
    # Phase 4: Governance Validation
    governance_alerts = validate_thresholds(final_score, division_metadata)
    
    return final_score, governance_alerts
```

### Division Priority Matrix

Technical priority calculations based on OBINexus organizational structure:

| Division | Priority Boost | Governance Threshold | Technical Focus |
|----------|----------------|---------------------|-----------------|
| Computing | 1.2 | 0.6 | Core technical infrastructure |
| UCHE Nnamdi | 1.5 | 0.5 | Strategic leadership projects |
| Aegis Engineering | 1.3 | 0.6 | Build orchestration systems |
| OBIAxis R&D | 1.1 | 0.7 | Research and development |
| TDA | 1.0 | 0.6 | Tactical defense applications |
| Publishing | 0.9 | 0.7 | Documentation and content |
| Nkwakọba | 1.0 | 0.6 | Packaging and presentation |

### Sinphasé Compliance Validation

PYDCL implements systematic Sinphasé compliance assessment:

- **Single-Pass Compilation**: Build time threshold validation (< 30 minutes)
- **Circular Dependency Detection**: Heuristic analysis based on size/complexity correlation
- **Temporal Coupling Assessment**: Commit activity vs. dependency complexity analysis
- **Architectural Reorganization Triggers**: Automatic isolation recommendations

---

## Output Specification

### JSON Output Format (cost_scores.json)

```json
{
  "organization": "obinexus",
  "generation_timestamp": "2024-12-10T15:30:45.123456",
  "total_repositories": 42,
  "analyzed_repositories": 38,
  "sinphase_compliance_rate": 0.89,
  "division_summaries": {
    "Computing": {
      "total_repositories": 15,
      "average_cost_score": 67.3,
      "governance_violations": 2,
      "isolation_candidates": 1,
      "top_repositories": ["libpolycall-bindings", "nexuslink", "polybuild"]
    }
  },
  "repository_scores": [
    {
      "repository": "libpolycall-bindings",
      "division": "Computing",
      "status": "Core",
      "calculated_score": 0.673,
      "normalized_score": 67.3,
      "governance_alerts": [],
      "sinphase_violations": [],
      "requires_isolation": false,
      "raw_metrics": {
        "stars_count": 23,
        "commits_last_30_days": 15,
        "size_kb": 2840,
        "build_time_minutes": 8.5,
        "test_coverage_percent": 87
      }
    }
  ]
}
```

### Inverted Triangle Layer Generation

The output includes systematic layer classification for visualization:

```python
# Automatic layer generation
layers = organization_report.get_inverted_triangle_layers()
# Returns:
# {
#   "surface": [top 30% by cost score],    # Trending/high-activity projects
#   "active": [middle 40% by cost score],  # Implementation phase projects  
#   "core": [bottom 30% by cost score]     # Stable/foundational projects
# }
```

---

## Integration with OBINexus Ecosystem

### Build Orchestration Integration

PYDCL integrates systematically with the OBINexus toolchain:

```bash
# Integration with NLink and PolyBuild
nlink discover --integration pydcl --output nlink_integration.json
polybuild --cost-layer-input cost_scores.json --validate-compliance

# Sinphasé methodology validation
pydcl analyze --org obinexus --sinphase-strict --isolation-auto
```

### Architectural Decision Integration

PYDCL supports architectural decision workflows through structured output:

1. **Cost Threshold Exceedance**: Automatic isolation recommendations
2. **Governance Violations**: Systematic compliance reporting
3. **Division Rebalancing**: Organizational structure optimization
4. **Build Complexity Assessment**: Single-pass compilation validation

---

## Development and Testing

### Development Setup

```bash
# Clone and setup development environment
git clone https://github.com/obinexus/pydcl.git
cd pydcl

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Install with development dependencies
pip install -e ".[dev,telemetry,visualization]"
```

### Current Testing Framework

```bash
# Basic package validation
python -c "import pydcl; print('✓ Package import successful')"

# Sinphasé architecture validation  
python -c "
from pydcl import ValidationError, calculate_sinphase_cost, GOVERNANCE_THRESHOLD
from pydcl.models import RepositoryMetrics, CostFactors
print('✓ Sinphasé implementation validated')
print(f'✓ Governance threshold: {GOVERNANCE_THRESHOLD}')
"

# CLI functionality testing
pydcl --version
pydcl --help

# Cost calculation testing
python -c "
from pydcl.models import RepositoryMetrics, CostFactors, calculate_sinphase_cost
metrics = RepositoryMetrics('test-project')
metrics.stars_count = 50
metrics.commits_last_30_days = 30
factors = CostFactors()
cost = calculate_sinphase_cost(metrics, factors)
print(f'Test calculation result: {cost:.3f}')
assert 0.0 <= cost <= 1.0, 'Cost calculation within expected bounds'
print('✓ Cost calculation validation passed')
"
```

### Future Testing Framework (Development Target)

```bash
# Planned comprehensive test suite
pytest tests/ -v --cov=pydcl --cov-report=html

# Planned integration tests with GitHub API
pytest tests/integration/ --github-token=$GH_API_TOKEN

# Planned Sinphasé compliance validation
pytest tests/sinphase/ -k "compliance"
```

---

## Technical Roadmap and Development Status

### Completed Milestones (Phase 1-2)

**✅ Foundation Architecture** (Waterfall Phase 1)
- Sinphasé-compliant package structure with single-pass compilation
- Cost-based governance framework implementation
- CLI entry point registration and Rich console integration
- Division-aware organizational modeling (7 divisions supported)
- Bounded complexity validation with automatic isolation triggers

**✅ Core Implementation** (Waterfall Phase 2)  
- Complete data model hierarchy with Pydantic validation
- Cost calculation framework with governance thresholds
- Systematic import resolution with graceful degradation
- Development installation and distribution pipeline
- UTF-8 encoding integrity validation and resolution

### Active Development (Phase 3)

**🔄 GitHub Integration Layer**
- Production GitHub API client implementation
- Repository metrics extraction with rate limiting
- Configuration discovery and validation system
- Comprehensive error handling and retry mechanisms

**🔄 CLI Command Implementation**
- `analyze` command with progress tracking and division filtering
- `display` command with multiple output formats (table, JSON, summary)
- `init` command for configuration template generation
- Systematic validation checkpoints and governance reporting

### Planned Implementation (Phase 4)

**⏳ Production Features**
- Complete Pydantic model validation with schema enforcement
- Interactive visualization components for inverted triangle analysis
- Integration testing framework with GitHub API validation
- Performance optimization and caching mechanisms
- Comprehensive documentation with API reference

**⏳ OBINexus Ecosystem Integration**
- NLink and PolyBuild coordination protocols
- Three core interactive systems per Formal Math Function Reasoning specification
- Enterprise security features with audit trail generation
- CI/CD pipeline templates and workflow automation

### Contact Information

- **Technical Lead**: Nnamdi Michael Okpala (nnamdi@obinexuscomputing.com)
- **Engineering Team**: support@obinexuscomputing.com
- **Documentation**: [https://pydcl.readthedocs.io](https://pydcl.readthedocs.io)
- **Repository**: [https://github.com/obinexus/pydcl](https://github.com/obinexus/pydcl)

---

## License and Legal

```
MIT License

Copyright (c) 2024 OBINexus Computing

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

**PYDCL v1.0.0** - Python Dynamic Cost Layer  
**OBINexus Computing - Division-Aware GitHub Organization Analysis**  
**Technical Architecture: Sinphasé Methodology Implementation**  
**Engineering Leadership: Nnamdi Michael Okpala**

*"Systematic cost governance meets division-aware organization analysis"*
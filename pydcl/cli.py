"""
PYDCL Command Line Interface

Technical CLI implementation following waterfall methodology for
systematic cost analysis generation. Provides structured command
interface for OBINexus division-aware GitHub organization analysis.

Technical Architecture:
- Systematic error handling and validation
- Structured output formatting with Rich console integration
- Methodical progress tracking for large organization analysis
- Strategic configuration validation and governance compliance
"""

import os
import sys
import json
import time
from pathlib import Path
from typing import Optional, Dict, Any

import click
from rich.console import Console
from rich.progress import Progress, TaskID
from rich.table import Table
from rich.panel import Panel
from rich.text import Text

from .cost_scores import CostScoreCalculator
from .github_client import GitHubMetricsClient
from .models import OrganizationCostReport, DivisionType, ProjectStatus
from .utils import validate_config, load_division_config, setup_logging


# Rich console for structured output
console = Console()
error_console = Console(stderr=True, style="red")

# Technical constants following Sinphas‚ methodology
DEFAULT_CONFIG_PATH = ".github/pydcl.yaml"
DEFAULT_OUTPUT_PATH = "cost_scores.json"
VALIDATION_CHECKPOINT_INTERVAL = 10


@click.group()
@click.version_option(version="1.0.0", prog_name="PYDCL")
@click.option(
    "--verbose", "-v", 
    is_flag=True, 
    help="Enable verbose technical output for debugging"
)
@click.option(
    "--config", "-c",
    type=click.Path(exists=True),
    help="Path to PYDCL configuration file"
)
@click.pass_context
def cli(ctx: click.Context, verbose: bool, config: Optional[str]) -> None:
    """
    PYDCL: Python Dynamic Cost Layer
    
    Division-aware GitHub organization cost modeling toolkit implementing
    the OBINexus Sinphas‚ methodology for hierarchical project structuring.
    
    Technical Lead: Nnamdi Michael Okpala
    Architecture: Waterfall methodology with systematic validation checkpoints
    """
    ctx.ensure_object(dict)
    ctx.obj['verbose'] = verbose
    ctx.obj['config_path'] = config
    
    # Initialize structured logging
    setup_logging(verbose=verbose)
    
    if verbose:
        console.print("[cyan]PYDCL Technical CLI Initialized[/cyan]")
        console.print(f"[dim]Configuration: {config or 'default'}[/dim]")


@cli.command()
@click.option(
    "--org", "-o", 
    required=True,
    help="GitHub organization name (e.g., 'obinexus')"
)
@click.option(
    "--token", "-t",
    envvar="GH_API_TOKEN",
    help="GitHub API token (or set GH_API_TOKEN env var)"
)
@click.option(
    "--output", "-f",
    type=click.Path(),
    default=DEFAULT_OUTPUT_PATH,
    help=f"Output JSON file path (default: {DEFAULT_OUTPUT_PATH})"
)
@click.option(
    "--division", "-d",
    type=click.Choice([d.value for d in DivisionType]),
    help="Analyze specific division only"
)
@click.option(
    "--validate-only", 
    is_flag=True,
    help="Perform validation checkpoint without full analysis"
)
@click.option(
    "--include-archived",
    is_flag=True,
    help="Include archived repositories in analysis"
)
@click.pass_context
def analyze(
    ctx: click.Context,
    org: str,
    token: Optional[str],
    output: str,
    division: Optional[str],
    validate_only: bool,
    include_archived: bool
) -> None:
    """
    Execute systematic cost analysis on GitHub organization.
    
    Technical Implementation:
    - Phase 1: Configuration validation and GitHub API authentication
    - Phase 2: Repository discovery and metadata extraction
    - Phase 3: Cost calculation with Sinphas‚ compliance validation
    - Phase 4: Division-aware aggregation and report generation
    """
    verbose = ctx.obj.get('verbose', False)
    
    try:
        # Phase 1: Technical Validation Checkpoint
        if verbose:
            console.print("[yellow]Phase 1: Configuration Validation[/yellow]")
        
        if not token:
            error_console.print("ERROR: GitHub API token required")
            error_console.print("Set GH_API_TOKEN environment variable or use --token")
            sys.exit(1)
        
        # Initialize technical components
        github_client = GitHubMetricsClient(token=token)
        calculator = CostScoreCalculator()
        
        # Validate GitHub connectivity
        if not github_client.validate_connection():
            error_console.print("ERROR: GitHub API authentication failed")
            sys.exit(1)
            
        if verbose:
            console.print("[green]V GitHub API authentication validated[/green]")
        
        # Phase 2: Repository Discovery
        if verbose:
            console.print("[yellow]Phase 2: Repository Discovery[/yellow]")
            
        with Progress() as progress:
            discovery_task = progress.add_task(
                "[cyan]Discovering repositories...", 
                total=None
            )
            
            repositories = github_client.get_organization_repositories(
                org_name=org,
                include_archived=include_archived
            )
            
            progress.update(discovery_task, completed=len(repositories))
            
        if verbose:
            console.print(f"[green]V Discovered {len(repositories)} repositories[/green]")
        
        if validate_only:
            console.print("[cyan]Validation checkpoint completed successfully[/cyan]")
            return
        
        # Phase 3: Cost Analysis with Progress Tracking
        if verbose:
            console.print("[yellow]Phase 3: Cost Analysis Execution[/yellow]")
            
        analysis_results = []
        
        with Progress() as progress:
            analysis_task = progress.add_task(
                "[cyan]Analyzing repositories...", 
                total=len(repositories)
            )
            
            for i, repo_metrics in enumerate(repositories):
                try:
                    # Load repository-specific configuration
                    repo_config = github_client.get_repository_config(
                        org_name=org,
                        repo_name=repo_metrics.name
                    )
                    
                    # Apply division filter if specified
                    if division and repo_config and repo_config.division.value != division:
                        progress.advance(analysis_task)
                        continue
                    
                    # Calculate cost score with Sinphas‚ compliance
                    cost_result = calculator.calculate_repository_cost(
                        metrics=repo_metrics,
                        config=repo_config
                    )
                    
                    analysis_results.append(cost_result)
                    
                    # Validation checkpoint every N repositories
                    if (i + 1) % VALIDATION_CHECKPOINT_INTERVAL == 0 and verbose:
                        console.print(f"[dim]Checkpoint: {i + 1}/{len(repositories)} processed[/dim]")
                    
                except Exception as e:
                    if verbose:
                        error_console.print(f"Warning: Failed to analyze {repo_metrics.name}: {e}")
                    
                finally:
                    progress.advance(analysis_task)
        
        # Phase 4: Report Generation and Validation
        if verbose:
            console.print("[yellow]Phase 4: Report Generation[/yellow]")
        
        # Generate comprehensive organization report
        organization_report = OrganizationCostReport(
            organization=org,
            total_repositories=len(repositories),
            analyzed_repositories=len(analysis_results),
            repository_scores=analysis_results
        )
        
        # Calculate division summaries
        calculator.generate_division_summaries(organization_report)
        
        # Technical validation of final report
        governance_violations = sum(
            len(result.governance_alerts) for result in analysis_results
        )
        
        sinphase_violations = sum(
            len(result.sinphase_violations) for result in analysis_results
        )
        
        # Output structured results
        output_path = Path(output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(
                organization_report.dict(),
                f,
                indent=2,
                ensure_ascii=False
            )
        
        # Technical Summary Report
        _display_technical_summary(
            organization_report=organization_report,
            governance_violations=governance_violations,
            sinphase_violations=sinphase_violations,
            output_path=output_path,
            verbose=verbose
        )
        
    except Exception as e:
        error_console.print(f"CRITICAL ERROR: {e}")
        if verbose:
            import traceback
            error_console.print(traceback.format_exc())
        sys.exit(1)


@cli.command()
@click.option(
    "--input", "-i",
    type=click.Path(exists=True),
    required=True,
    help="Input cost_scores.json file"
)
@click.option(
    "--division", "-d",
    type=click.Choice([d.value for d in DivisionType]),
    help="Display specific division only"
)
@click.option(
    "--format", "-f",
    type=click.Choice(["table", "json", "summary"]),
    default="table",
    help="Output format for display"
)
@click.pass_context
def display(
    ctx: click.Context,
    input: str,
    division: Optional[str],
    format: str
) -> None:
    """
    Display systematic analysis results with structured formatting.
    
    Technical Implementation:
    - Structured data validation and parsing
    - Division-aware filtering and aggregation  
    - Rich console formatting for technical readability
    """
    verbose = ctx.obj.get('verbose', False)
    
    try:
        # Load and validate report data
        with open(input, 'r', encoding='utf-8') as f:
            report_data = json.load(f)
        
        organization_report = OrganizationCostReport(**report_data)
        
        if division:
            # Filter by specific division
            filtered_scores = [
                score for score in organization_report.repository_scores
                if score.division.value == division
            ]
            organization_report.repository_scores = filtered_scores
        
        if format == "json":
            console.print_json(data=organization_report.dict())
        elif format == "summary":
            _display_division_summary(organization_report)
        else:
            _display_repository_table(organization_report, verbose)
            
    except Exception as e:
        error_console.print(f"ERROR: Failed to display results: {e}")
        sys.exit(1)


@cli.command()
@click.option(
    "--template", "-t",
    type=click.Choice(["basic", "advanced", "enterprise"]),
    default="basic",
    help="Configuration template type"
)
@click.option(
    "--output", "-o",
    type=click.Path(),
    default=DEFAULT_CONFIG_PATH,
    help=f"Output configuration file (default: {DEFAULT_CONFIG_PATH})"
)
def init(template: str, output: str) -> None:
    """
    Initialize PYDCL configuration following technical specifications.
    
    Technical Implementation:
    - Template-based configuration generation
    - Sinphas‚ methodology compliance validation
    - Division-aware parameter initialization
    """
    try:
        config_data = _generate_config_template(template)
        
        output_path = Path(output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(config_data, f, indent=2)
        
        console.print(f"[green]V Configuration initialized: {output_path}[/green]")
        console.print("[cyan]Technical Note: Review and customize division parameters[/cyan]")
        
    except Exception as e:
        error_console.print(f"ERROR: Configuration initialization failed: {e}")
        sys.exit(1)


def _display_technical_summary(
    organization_report: OrganizationCostReport,
    governance_violations: int,
    sinphase_violations: int,
    output_path: Path,
    verbose: bool
) -> None:
    """Display structured technical summary with Rich formatting."""
    
    # Main summary panel
    summary_text = Text()
    summary_text.append(f"Organization: {organization_report.organization}\n", style="bold")
    summary_text.append(f"Total Repositories: {organization_report.total_repositories}\n")
    summary_text.append(f"Analyzed: {organization_report.analyzed_repositories}\n")
    summary_text.append(f"Governance Violations: {governance_violations}\n", 
                       style="red" if governance_violations > 0 else "green")
    summary_text.append(f"Sinphas‚ Violations: {sinphase_violations}\n",
                       style="red" if sinphase_violations > 0 else "green")
    summary_text.append(f"Output: {output_path}")
    
    console.print(Panel(summary_text, title="Technical Analysis Summary", border_style="cyan"))
    
    # Division breakdown if verbose
    if verbose and organization_report.division_summaries:
        console.print("\n[yellow]Division Technical Breakdown:[/yellow]")
        
        division_table = Table(show_header=True, header_style="bold cyan")
        division_table.add_column("Division")
        division_table.add_column("Repositories", justify="right")
        division_table.add_column("Avg Score", justify="right")
        division_table.add_column("Violations", justify="right")
        
        for division, summary in organization_report.division_summaries.items():
            division_table.add_row(
                division.value,
                str(summary.total_repositories),
                f"{summary.average_cost_score:.1f}",
                str(summary.governance_violations),
                style="red" if summary.governance_violations > 0 else None
            )
        
        console.print(division_table)


def _display_repository_table(report: OrganizationCostReport, verbose: bool) -> None:
    """Display repository analysis in structured table format."""
    
    table = Table(show_header=True, header_style="bold cyan")
    table.add_column("Repository")
    table.add_column("Division")
    table.add_column("Status")
    table.add_column("Score", justify="right")
    
    if verbose:
        table.add_column("Stars", justify="right")
        table.add_column("Commits", justify="right")
        table.add_column("Alerts", justify="right")
    
    # Sort by cost score (descending)
    sorted_repos = sorted(
        report.repository_scores,
        key=lambda x: x.normalized_score,
        reverse=True
    )
    
    for repo in sorted_repos:
        row_style = None
        if repo.requires_isolation:
            row_style = "red"
        elif repo.governance_alerts:
            row_style = "yellow"
        
        row_data = [
            repo.repository,
            repo.division.value,
            repo.status.value,
            f"{repo.normalized_score:.1f}"
        ]
        
        if verbose:
            row_data.extend([
                str(repo.raw_metrics.stars_count),
                str(repo.raw_metrics.commits_last_30_days),
                str(len(repo.governance_alerts) + len(repo.sinphase_violations))
            ])
        
        table.add_row(*row_data, style=row_style)
    
    console.print(table)


def _display_division_summary(report: OrganizationCostReport) -> None:
    """Display division-focused summary analysis."""
    
    for division, summary in report.division_summaries.items():
        panel_text = Text()
        panel_text.append(f"Repositories: {summary.total_repositories}\n")
        panel_text.append(f"Average Score: {summary.average_cost_score:.1f}\n")
        panel_text.append(f"Governance Issues: {summary.governance_violations}\n")
        
        if summary.top_repositories:
            panel_text.append("\nTop Projects:\n", style="bold")
            for repo in summary.top_repositories[:5]:
                panel_text.append(f"   {repo}\n")
        
        console.print(Panel(
            panel_text, 
            title=f"{division.value} Division", 
            border_style="cyan"
        ))


def _generate_config_template(template_type: str) -> Dict[str, Any]:
    """Generate configuration template based on specified type."""
    
    base_config = {
        "version": "1.0.0",
        "organization": "obinexus",
        "divisions": {
            "Computing": {
                "governance_threshold": 0.6,
                "isolation_threshold": 0.8,
                "priority_boost": 1.2
            },
            "UCHE Nnamdi": {
                "governance_threshold": 0.5,
                "isolation_threshold": 0.7,
                "priority_boost": 1.5
            }
        },
        "cost_factors": {
            "stars_weight": 0.2,
            "commit_activity_weight": 0.3,
            "build_time_weight": 0.2,
            "size_weight": 0.2,
            "test_coverage_weight": 0.1
        }
    }
    
    if template_type == "enterprise":
        base_config["telemetry"] = {
            "enabled": True,
            "prometheus_endpoint": "http://localhost:9090",
            "structured_logging": True
        }
        base_config["governance"] = {
            "strict_validation": True,
            "automated_isolation": True,
            "compliance_reporting": True
        }
    
    return base_config


def main() -> None:
    """Main CLI entry point with systematic error handling."""
    try:
        cli()
    except KeyboardInterrupt:
        error_console.print("\n[red]Operation interrupted by user[/red]")
        sys.exit(130)
    except Exception as e:
        error_console.print(f"[red]FATAL ERROR: {e}[/red]")
        sys.exit(1)


if __name__ == "__main__":
    main()

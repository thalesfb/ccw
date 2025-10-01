"""
Command-line interface for systematic review pipeline.
"""
import click
import logging
from pathlib import Path

from research.improved_pipeline import run_pipeline
from research.database import DatabaseManager
from research.exports import ExportManager
from research.config import DEFAULT_YEAR_MIN, DEFAULT_MAX_RESULTS_PER_QUERY


@click.group()
def cli():
    """Systematic Review Pipeline CLI."""
    pass


@cli.command()
@click.option(
    '--max-results',
    default=DEFAULT_MAX_RESULTS_PER_QUERY,
    help='Maximum results per query per API'
)
@click.option(
    '--year-min',
    default=DEFAULT_YEAR_MIN,
    help='Minimum publication year'
)
@click.option(
    '--no-db',
    is_flag=True,
    help='Skip saving to database'
)
@click.option(
    '--no-excel',
    is_flag=True,
    help='Skip Excel export'
)
@click.option(
    '--no-csv',
    is_flag=True,
    help='Skip CSV export'
)
@click.option(
    '--no-report',
    is_flag=True,
    help='Skip summary report generation'
)
@click.option(
    '--verbose',
    is_flag=True,
    help='Enable verbose logging'
)
def run(max_results, year_min, no_db, no_excel, no_csv, no_report, verbose):
    """Run the complete systematic review pipeline."""
    if verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    click.echo("🚀 Starting systematic review pipeline...")
    
    df = run_pipeline(
        max_results_per_query=max_results,
        year_min=year_min,
        save_to_db=not no_db,
        export_excel=not no_excel,
        export_csv=not no_csv,
        generate_report=not no_report
    )
    
    click.echo(f"\n✨ Pipeline completed. Total papers: {len(df)}")


@cli.command()
@click.option(
    '--database',
    help='Filter by database name'
)
@click.option(
    '--year-min',
    type=int,
    help='Filter by minimum year'
)
@click.option(
    '--format',
    type=click.Choice(['excel', 'csv', 'both']),
    default='excel',
    help='Export format'
)
def export(database, year_min, format):
    """Export papers from database."""
    click.echo("📤 Exporting papers from database...")
    
    db_manager = DatabaseManager()
    df = db_manager.load_papers(database=database, year_min=year_min)
    
    if df.empty:
        click.echo("⚠️ No papers found with the specified filters.")
        return
    
    export_manager = ExportManager()
    
    if format in ['excel', 'both']:
        filepath = export_manager.export_to_excel(df)
        click.echo(f"✅ Excel exported: {filepath}")
    
    if format in ['csv', 'both']:
        filepath = export_manager.export_to_csv(df)
        click.echo(f"✅ CSV exported: {filepath}")
    
    click.echo(f"\n✨ Exported {len(df)} papers")


@cli.command()
@click.option(
    '--database',
    help='Filter by database name'
)
@click.option(
    '--year-min',
    type=int,
    help='Filter by minimum year'
)
def stats(database, year_min):
    """Show statistics about papers in database."""
    click.echo("📊 Loading statistics from database...")
    
    db_manager = DatabaseManager()
    df = db_manager.load_papers(database=database, year_min=year_min)
    
    if df.empty:
        click.echo("⚠️ No papers found in database.")
        return
    
    click.echo(f"\nTotal Papers: {len(df)}")
    
    if 'database' in df.columns:
        click.echo("\nPapers by Database:")
        for db, count in df['database'].value_counts().items():
            click.echo(f"  - {db}: {count}")
    
    if 'year' in df.columns and not df['year'].isnull().all():
        click.echo(f"\nYear Range: {df['year'].min():.0f} - {df['year'].max():.0f}")
    
    if 'is_open_access' in df.columns:
        oa_count = df['is_open_access'].sum()
        click.echo(f"\nOpen Access Papers: {oa_count} ({oa_count/len(df)*100:.1f}%)")


@cli.command()
@click.confirmation_option(
    prompt='Are you sure you want to clear all papers from the database?'
)
def clear():
    """Clear all papers from database."""
    click.echo("🗑️ Clearing database...")
    
    db_manager = DatabaseManager()
    db_manager.clear_papers()
    
    click.echo("✅ Database cleared successfully")


@cli.command()
def info():
    """Show information about the pipeline configuration."""
    from research.config import (
        FIRST_TERMS,
        SECOND_TERMS,
        DEFAULT_YEAR_MIN,
        DEFAULT_MAX_RESULTS_PER_QUERY,
        DEDUP_RATIO_THRESHOLD,
        DEDUP_COSINE_THRESHOLD
    )
    
    click.echo("=" * 80)
    click.echo("SYSTEMATIC REVIEW PIPELINE CONFIGURATION")
    click.echo("=" * 80)
    
    click.echo(f"\nSearch Configuration:")
    click.echo(f"  - Primary Terms: {len(FIRST_TERMS)}")
    click.echo(f"  - Secondary Terms: {len(SECOND_TERMS)}")
    click.echo(f"  - Total Queries: {len(FIRST_TERMS) * len(SECOND_TERMS)}")
    click.echo(f"  - Default Year Min: {DEFAULT_YEAR_MIN}")
    click.echo(f"  - Default Max Results/Query: {DEFAULT_MAX_RESULTS_PER_QUERY}")
    
    click.echo(f"\nDeduplication Configuration:")
    click.echo(f"  - Fuzzy Ratio Threshold: {DEDUP_RATIO_THRESHOLD}")
    click.echo(f"  - Cosine Distance Threshold: {DEDUP_COSINE_THRESHOLD}")
    
    click.echo(f"\nDirectories:")
    click.echo(f"  - Cache: research/cache/")
    click.echo(f"  - Exports: research/exports/")
    click.echo(f"  - Logs: research/logs/")
    click.echo(f"  - Database: research/systematic_review.db")
    
    click.echo("\n" + "=" * 80)


if __name__ == '__main__':
    cli()

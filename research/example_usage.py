"""
Example usage of the systematic review pipeline.

This script demonstrates how to use the pipeline programmatically.
"""
import os
os.environ['USER_EMAIL'] = 'test@example.com'
os.environ['CORE_API_KEY'] = 'test_key'

from research.config import FIRST_TERMS, SECOND_TERMS
from research.utils import queries_generator
from research.models import Paper
from research.database import DatabaseManager
from research.exports import ExportManager
from research.deduplication import deduplicate_articles
import pandas as pd

# Example: Generate queries
print("=" * 80)
print("SYSTEMATIC REVIEW PIPELINE - EXAMPLE USAGE")
print("=" * 80)

queries = queries_generator(FIRST_TERMS[:2], SECOND_TERMS[:2])
print(f"\n📝 Generated {len(queries)} sample queries:")
for i, q in enumerate(queries, 1):
    print(f"  {i}. {q}")

# Example: Create sample papers
print("\n📚 Creating sample papers...")
sample_papers = [
    Paper(
        title="Machine Learning in Mathematics Education",
        authors="John Doe, Jane Smith",
        year=2020,
        database="example",
        abstract="This paper explores machine learning applications in math education.",
        doi_url="https://doi.org/10.1234/example1",
        is_open_access=True,
        search_terms=queries[0]
    ),
    Paper(
        title="Adaptive Learning Systems for Mathematics",
        authors="Alice Johnson",
        year=2021,
        database="example",
        abstract="An exploration of adaptive learning in mathematics education.",
        doi_url="https://doi.org/10.1234/example2",
        is_open_access=False,
        search_terms=queries[1]
    ),
    Paper(
        title="Machine Learning in Mathematics Education",  # Duplicate
        authors="John Doe",
        year=2020,
        database="example",
        abstract="This paper explores machine learning applications.",
        doi_url="https://doi.org/10.1234/example1",  # Same DOI
        is_open_access=True,
        search_terms=queries[0]
    ),
]

print(f"  Created {len(sample_papers)} sample papers (including 1 duplicate)")

# Example: Create DataFrame and deduplicate
print("\n🔄 Converting to DataFrame and deduplicating...")
df = pd.DataFrame([p.to_dict() for p in sample_papers])
print(f"  Before deduplication: {len(df)} papers")

df_dedup = deduplicate_articles(df)
print(f"  After deduplication: {len(df_dedup)} papers")

# Example: Database operations
print("\n💾 Database operations...")
import tempfile
db_path = os.path.join(tempfile.gettempdir(), "test_systematic_review.db")
db_manager = DatabaseManager(db_path)

# Clear any existing data
db_manager.clear_papers()

# Save papers
papers = [Paper(**row) for _, row in df_dedup.iterrows()]
saved_count = db_manager.save_papers(papers)
print(f"  Saved {saved_count} papers to database")

# Load papers
loaded_df = db_manager.load_papers()
print(f"  Loaded {len(loaded_df)} papers from database")

# Filter by year
recent_df = db_manager.load_papers(year_min=2021)
print(f"  Papers from 2021+: {len(recent_df)}")

# Example: Export operations
print("\n📤 Export operations...")
export_dir = tempfile.mkdtemp()
export_manager = ExportManager(export_dir)

excel_path = export_manager.export_to_excel(df_dedup, "example_review.xlsx")
print(f"  Excel exported to: {excel_path}")

csv_path = export_manager.export_to_csv(df_dedup, "example_review.csv")
print(f"  CSV exported to: {csv_path}")

report_path = export_manager.generate_summary_report(df_dedup)
print(f"  Summary report: {report_path}")

# Show summary
print("\n" + "=" * 80)
print("SUMMARY")
print("=" * 80)
print(f"  Total unique papers: {len(df_dedup)}")
print(f"  Duplicates removed: {len(df) - len(df_dedup)}")
print(f"  Years covered: {df_dedup['year'].min()}-{df_dedup['year'].max()}")
print(f"  Open access: {df_dedup['is_open_access'].sum()}")
print("\n✅ Example completed successfully!")

# Cleanup
os.remove(db_path)
print(f"\n🧹 Cleaned up test database: {db_path}")

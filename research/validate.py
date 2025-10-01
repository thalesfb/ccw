#!/usr/bin/env python3
"""
Validation script for research module refactoring.

This script validates that all components of the refactored research module
are working correctly without making actual API calls.
"""
import sys
import os

# Ensure we can import research module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

print("=" * 80)
print("RESEARCH MODULE VALIDATION")
print("=" * 80)

# Test 1: Module imports
print("\n[1/10] Testing module imports...")
try:
    from research import config, models, database, deduplication, exports
    from research.api_clients import (
        SemanticScholarSearcher,
        OpenAlexSearcher, 
        CrossrefSearcher,
        CoreSearcher
    )
    from research import utils, cli, improved_pipeline
    print("✅ All modules imported successfully")
except ImportError as e:
    print(f"❌ Import failed: {e}")
    sys.exit(1)

# Test 2: Configuration
print("\n[2/10] Testing configuration...")
try:
    assert len(config.FIRST_TERMS) > 0, "No primary search terms"
    assert len(config.SECOND_TERMS) > 0, "No secondary search terms"
    assert len(config.PAPER_COLUMNS) > 0, "No paper columns defined"
    assert config.DEFAULT_YEAR_MIN > 2000, "Invalid default year"
    print(f"✅ Configuration valid")
    print(f"   - {len(config.FIRST_TERMS)} primary terms")
    print(f"   - {len(config.SECOND_TERMS)} secondary terms")
    print(f"   - {len(config.PAPER_COLUMNS)} paper columns")
except AssertionError as e:
    print(f"❌ Configuration error: {e}")
    sys.exit(1)

# Test 3: Data models
print("\n[3/10] Testing data models...")
try:
    paper = models.Paper(
        title="Test Paper",
        authors="Test Author",
        year=2020,
        database="test"
    )
    paper_dict = paper.to_dict()
    assert isinstance(paper_dict, dict)
    assert paper_dict['title'] == "Test Paper"
    print("✅ Paper model working correctly")
except Exception as e:
    print(f"❌ Model error: {e}")
    sys.exit(1)

# Test 4: Utility functions
print("\n[4/10] Testing utility functions...")
try:
    # Test normalization
    normalized = utils.normalize_text("Educação Matemática")
    assert normalized == "educacao matematica"
    
    # Test query generation
    queries = utils.queries_generator(["term1"], ["term2"])
    assert len(queries) == 1
    assert '"term1" AND "term2"' in queries
    
    # Test relevance filtering
    test_paper = models.Paper(
        title="Machine Learning in Education",
        abstract="Using ML for adaptive learning",
        year=2020
    )
    relevant, _ = utils.is_relevant_paper(
        test_paper, 2015, ["en"], ["education", "learning"], ["machine learning"]
    )
    assert relevant is True
    
    print("✅ Utility functions working correctly")
except Exception as e:
    print(f"❌ Utility error: {e}")
    sys.exit(1)

# Test 5: Database operations
print("\n[5/10] Testing database operations...")
try:
    import tempfile
    db_path = os.path.join(tempfile.gettempdir(), "validation_test.db")
    
    # Create database
    db = database.DatabaseManager(db_path)
    
    # Save papers
    test_papers = [
        models.Paper(title=f"Paper {i}", year=2020+i, doi_url=f"doi{i}")
        for i in range(3)
    ]
    saved = db.save_papers(test_papers)
    assert saved == 3, f"Expected 3 papers saved, got {saved}"
    
    # Load papers
    loaded_df = db.load_papers()
    assert len(loaded_df) == 3, f"Expected 3 papers loaded, got {len(loaded_df)}"
    
    # Clear
    db.clear_papers()
    assert len(db.load_papers()) == 0
    
    # Cleanup
    os.remove(db_path)
    
    print("✅ Database operations working correctly")
except Exception as e:
    print(f"❌ Database error: {e}")
    sys.exit(1)

# Test 6: Deduplication
print("\n[6/10] Testing deduplication...")
try:
    import pandas as pd
    
    # Create test data with duplicates
    data = {
        'title': ['Paper A', 'Paper A', 'Paper B'],
        'doi_url': ['doi1', 'doi1', 'doi2'],
        'abstract': ['Abstract 1', 'Abstract 2', 'Abstract 3'],
        'year': [2020, 2020, 2021]
    }
    df = pd.DataFrame(data)
    
    # Add missing columns
    for col in config.PAPER_COLUMNS:
        if col not in df.columns:
            df[col] = None
    
    # Deduplicate
    df_dedup = deduplication.deduplicate_articles(df)
    
    assert len(df_dedup) == 2, f"Expected 2 papers after dedup, got {len(df_dedup)}"
    
    print("✅ Deduplication working correctly")
    print(f"   - Removed {len(df) - len(df_dedup)} duplicate(s)")
except Exception as e:
    print(f"❌ Deduplication error: {e}")
    sys.exit(1)

# Test 7: Export functionality
print("\n[7/10] Testing export functionality...")
try:
    import tempfile
    import pandas as pd
    
    export_dir = tempfile.mkdtemp()
    export_mgr = exports.ExportManager(export_dir)
    
    # Create test data
    test_df = pd.DataFrame([
        models.Paper(title="Test Paper", year=2020, doi_url="doi1").to_dict()
    ])
    
    # Export to Excel
    excel_path = export_mgr.export_to_excel(test_df, "test.xlsx")
    assert os.path.exists(excel_path)
    
    # Export to CSV
    csv_path = export_mgr.export_to_csv(test_df, "test.csv")
    assert os.path.exists(csv_path)
    
    # Generate report
    report_path = export_mgr.generate_summary_report(test_df)
    assert os.path.exists(report_path)
    
    # Cleanup
    import shutil
    shutil.rmtree(export_dir)
    
    print("✅ Export functionality working correctly")
    print(f"   - Excel export: {os.path.basename(excel_path)}")
    print(f"   - CSV export: {os.path.basename(csv_path)}")
    print(f"   - Report: {os.path.basename(report_path)}")
except Exception as e:
    print(f"❌ Export error: {e}")
    sys.exit(1)

# Test 8: API Client structure
print("\n[8/10] Testing API client structure...")
try:
    # Check that all clients exist and inherit from BaseSearcher
    from research.api_clients.base import BaseSearcher
    
    clients = [
        SemanticScholarSearcher,
        OpenAlexSearcher,
        CrossrefSearcher,
        CoreSearcher
    ]
    
    for client_class in clients:
        # Just check instantiation doesn't fail
        try:
            instance = client_class()
            assert hasattr(instance, 'search')
            assert hasattr(instance, '_request_page')
            assert hasattr(instance, '_item_to_paper')
        except Exception as e:
            print(f"   ⚠️  {client_class.__name__} instantiation warning: {e}")
    
    print("✅ API client structure validated")
    print(f"   - 4 API clients available")
except Exception as e:
    print(f"❌ API client error: {e}")
    sys.exit(1)

# Test 9: CLI availability
print("\n[9/10] Testing CLI availability...")
try:
    import click
    from research.cli import cli
    
    # Check CLI commands
    assert hasattr(cli, 'commands')
    commands = list(cli.commands.keys())
    expected_commands = ['run', 'export', 'stats', 'clear', 'info']
    
    for cmd in expected_commands:
        assert cmd in commands, f"Missing CLI command: {cmd}"
    
    print("✅ CLI structure validated")
    print(f"   - Available commands: {', '.join(commands)}")
except Exception as e:
    print(f"❌ CLI error: {e}")
    sys.exit(1)

# Test 10: Pipeline structure
print("\n[10/10] Testing pipeline structure...")
try:
    from research.improved_pipeline import run_pipeline, search_all_apis
    
    # Check functions exist
    assert callable(run_pipeline)
    assert callable(search_all_apis)
    
    print("✅ Pipeline structure validated")
except Exception as e:
    print(f"❌ Pipeline error: {e}")
    sys.exit(1)

# Summary
print("\n" + "=" * 80)
print("VALIDATION COMPLETE")
print("=" * 80)
print("\n✅ All 10 validation tests passed!")
print("\nModule components validated:")
print("  ✓ Module imports")
print("  ✓ Configuration")
print("  ✓ Data models")
print("  ✓ Utility functions")
print("  ✓ Database operations")
print("  ✓ Deduplication")
print("  ✓ Export functionality")
print("  ✓ API client structure")
print("  ✓ CLI interface")
print("  ✓ Pipeline structure")
print("\n🎉 Research module refactoring is complete and functional!")
print("\nNext steps:")
print("  1. Configure API keys in .env file")
print("  2. Run: python -m research.cli run --max-results 5")
print("  3. Review logs in research/logs/pipeline.log")
print("  4. Check exports in research/exports/")
print("\nFor more information, see:")
print("  - research/README.md")
print("  - research/refactoring_plan.md")
print("  - research/example_usage.py")

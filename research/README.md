# Research Module - Systematic Review Pipeline

Automated pipeline for conducting systematic literature reviews following PRISMA guidelines.

## Features

- **Multi-API Search**: Automated searches across Semantic Scholar, OpenAlex, Crossref, and CORE
- **Smart Deduplication**: Two-stage deduplication using DOI matching and TF-IDF similarity
- **Response Caching**: Reduces API calls and speeds up repeated searches
- **SQLite Database**: Persistent storage with indexing for fast queries
- **Multiple Export Formats**: Excel (with summary), CSV, and text reports
- **CLI Interface**: Easy-to-use command-line interface
- **Comprehensive Logging**: Audit trail for reproducibility
- **Test Suite**: 16 unit tests ensuring reliability

## Quick Start

### 1. Configuration

Create a `.env` file from the sample:

```bash
cp .env.sample .env
```

Edit `.env` with your API credentials:

```bash
# Required for CORE API
CORE_API_KEY=your_core_api_key_here

# Required for OpenAlex and Crossref
USER_EMAIL=your_email@example.com

# Optional: For higher Semantic Scholar rate limits
SEMANTIC_SCHOLAR_API_KEY=your_ss_api_key_here
```

### 2. Run the Pipeline

**Option A: Using CLI (Recommended)**

```bash
# Full pipeline with default settings
python -m research.cli run

# Custom parameters
python -m research.cli run --max-results 20 --year-min 2018

# Skip certain outputs
python -m research.cli run --no-excel --no-report

# Verbose logging
python -m research.cli run --verbose
```

**Option B: Programmatically**

```python
from research.improved_pipeline import run_pipeline

df = run_pipeline(
    max_results_per_query=15,
    year_min=2018,
    save_to_db=True,
    export_excel=True
)
```

**Option C: Direct Script**

```bash
python research/improved_pipeline.py
```

## CLI Commands

### `run` - Execute Pipeline

Execute the complete systematic review pipeline.

```bash
python -m research.cli run [OPTIONS]
```

Options:
- `--max-results INTEGER`: Maximum results per query per API (default: 10)
- `--year-min INTEGER`: Minimum publication year (default: 2015)
- `--no-db`: Skip saving to database
- `--no-excel`: Skip Excel export
- `--no-csv`: Skip CSV export
- `--no-report`: Skip summary report
- `--verbose`: Enable verbose logging

### `export` - Export from Database

Export papers from the database to files.

```bash
python -m research.cli export [OPTIONS]
```

Options:
- `--database TEXT`: Filter by database name
- `--year-min INTEGER`: Filter by minimum year
- `--format [excel|csv|both]`: Export format (default: excel)

### `stats` - Show Statistics

Display statistics about papers in the database.

```bash
python -m research.cli stats [OPTIONS]
```

Options:
- `--database TEXT`: Filter by database name
- `--year-min INTEGER`: Filter by minimum year

### `clear` - Clear Database

Remove all papers from the database (requires confirmation).

```bash
python -m research.cli clear
```

### `info` - Show Configuration

Display current pipeline configuration.

```bash
python -m research.cli info
```

## Architecture

### Module Structure

```
research/
├── __init__.py              # Package initialization
├── config.py                # Configuration and constants
├── models.py                # Data models (Paper)
├── improved_pipeline.py     # Main pipeline orchestration
├── cli.py                   # Command-line interface
├── database.py              # SQLite database manager
├── deduplication.py         # Deduplication logic
├── exports.py               # Export management
├── api_clients/             # API client implementations
│   ├── base.py             # Abstract base searcher
│   ├── semantic_scholar.py
│   ├── openalex.py
│   ├── crossref.py
│   └── core.py
└── utils/                   # Utility functions
```

### Data Flow

```
Search Terms → API Clients → Cache → Filtering → Deduplication → Database → Exports
                    ↓
                  Logging (audit trail)
```

## API Clients

### Semantic Scholar
- Full-text search with field-specific filters
- Optional API key for higher rate limits
- Automatically extracts: title, authors, year, venue, abstract, DOI, fields of study

### OpenAlex
- Open metadata with comprehensive coverage
- Reconstructs abstracts from inverted index
- Extracts: title, authors, year, venue, concepts, open access status

### Crossref
- Bibliographic metadata with DOI resolution
- Uses `crossref.restful` Python library
- Best for published journal articles

### CORE
- Focus on open access research
- Full-text availability when possible
- Requires API key

## Deduplication

Two-stage approach for maximum accuracy:

1. **Exact Matching**: Removes papers with identical DOIs/URLs
2. **Similarity Detection**:
   - Text normalization (lowercase, accent removal)
   - Blocking by title prefix (performance optimization)
   - TF-IDF vectorization
   - Nearest neighbor search with cosine similarity
   - RapidFuzz confirmation for fuzzy matching
   - Keeps paper with DOI or longer abstract

## Configuration

Edit `research/config.py` to customize:

- Search terms (primary and secondary)
- API rate limits and delays
- Deduplication thresholds
- DataFrame columns
- File paths

## Testing

```bash
# Run all tests
pytest research/tests/

# Quick tests only (fast)
pytest research/tests/quick/

# With coverage
pytest --cov=research research/tests/

# Specific test file
pytest research/tests/quick/test_basic.py -v
```

## Logging

Logs are written to:
- Console (INFO level and above)
- `research/logs/pipeline.log` (all levels)

Log format: `TIMESTAMP [LEVEL] MODULE: MESSAGE`

## Output Files

### Database
- `research/systematic_review.db` - SQLite database with all papers

### Cache
- `research/cache/[api_name]/[query_hash].json` - Cached API responses

### Exports
- Excel files with data and summary sheets
- CSV files for data analysis
- Text-based summary reports

## Troubleshooting

### ModuleNotFoundError: No module named 'research'

Run scripts using the `-m` flag:
```bash
python -m research.cli run
```

Or add the repository root to PYTHONPATH:
```bash
export PYTHONPATH=/path/to/ccw:$PYTHONPATH
```

### API Rate Limiting

If you encounter 429 errors:
1. Increase rate delays in `config.py`
2. Use API keys for higher limits
3. Enable response caching (on by default)

### Empty Results

Check:
1. API credentials in `.env` are correct
2. Search terms are not too restrictive
3. Year range is appropriate
4. Review logs for API errors

## Best Practices

1. **Start Small**: Test with `--max-results 5` first
2. **Use Caching**: Don't clear cache unless necessary
3. **Monitor Logs**: Check for API errors or rate limits
4. **Regular Exports**: Export data after successful runs
5. **Backup Database**: Copy `systematic_review.db` regularly

## Performance

- **Cache Hit**: ~instant (no API call)
- **API Response**: 3-10 seconds per query (depends on API)
- **Deduplication**: <1 second for 1000 papers
- **Database Save**: <1 second for 1000 papers

## Extending

### Add New API Client

1. Create `research/api_clients/new_api.py`
2. Subclass `BaseSearcher`
3. Implement `_request_page` and `_item_to_paper`
4. Add to `improved_pipeline.py`

Example:
```python
from .base import BaseSearcher
from ..models import Paper

class NewAPISearcher(BaseSearcher):
    def __init__(self):
        super().__init__("new_api")
    
    def _request_page(self, query, max_results):
        # Yield raw items from API
        pass
    
    def _item_to_paper(self, item, query):
        # Convert API item to Paper
        return Paper(...)
```

## Related Documents

- [Refactoring Plan](refactoring_plan.md) - Detailed architecture and design decisions
- [Example Usage](example_usage.py) - Programmatic usage examples
- [Original Notebook](systematic_review.ipynb) - Reference implementation

## Support

For issues or questions:
1. Check logs in `research/logs/`
2. Review test failures: `pytest research/tests/ -v`
3. Consult [refactoring_plan.md](refactoring_plan.md) for design details

## License

See repository LICENSE file.

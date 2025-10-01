# Research Module Refactoring Plan

## Overview
Refactoring of systematic review notebook into a modular Python pipeline for better maintainability, testability, and extensibility.

## Status: ✅ Completed

## Objectives
1. Convert Jupyter notebook code into reusable Python modules
2. Implement proper separation of concerns (SOLID principles)
3. Add comprehensive test coverage
4. Provide CLI for easy pipeline execution
5. Support configuration via environment variables
6. Implement robust caching and logging

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
├── exports.py               # Export management (Excel, CSV, reports)
├── api_clients/             # API client modules
│   ├── __init__.py
│   ├── base.py             # Abstract base searcher
│   ├── semantic_scholar.py # Semantic Scholar API
│   ├── openalex.py         # OpenAlex API
│   ├── crossref.py         # Crossref API
│   └── core.py             # CORE API
├── utils/                   # Utility functions
│   └── __init__.py         # Caching, normalization, etc.
├── tests/                   # Test suite
│   ├── quick/              # Fast unit tests
│   ├── full/               # Integration tests
│   └── benchmark/          # Performance tests
├── cache/                   # API response cache (gitignored)
├── exports/                 # Generated exports (gitignored)
└── logs/                    # Application logs (gitignored)
```

## Implementation Details

### 1. API Clients (✅ Completed)
- **Base Searcher**: Abstract base class with common search logic
- **Semantic Scholar**: Full-text search with field filters
- **OpenAlex**: Open access metadata with abstract reconstruction
- **Crossref**: Bibliographic data with DOI resolution
- **CORE**: Open access research papers with full-text

Each client implements:
- Pagination handling
- Rate limiting with exponential backoff
- Error handling and retry logic
- Response caching
- Data normalization to Paper model

### 2. Database Management (✅ Completed)
- SQLite for local storage
- Automatic schema creation
- Deduplication on insert
- Filtering by database and year
- Indexing on DOI and title for performance

### 3. Deduplication (✅ Completed)
Two-stage approach:
1. Exact DOI/URL matching
2. Title similarity using:
   - Text normalization
   - TF-IDF vectorization
   - Cosine similarity
   - Fuzzy string matching (RapidFuzz)

### 4. Export Management (✅ Completed)
- Excel export with multiple sheets (data + summary)
- CSV export for data analysis
- Text-based summary reports
- Configurable export directory

### 5. Configuration (✅ Completed)
- Environment variables via .env file
- Centralized configuration in config.py
- Search terms and filters
- API rate limits and delays
- Deduplication thresholds

### 6. Logging (✅ Completed)
- Structured logging with timestamps
- Per-module loggers
- File and console output
- Debug, Info, Warning, Error levels
- Audit trail for reproducibility

### 7. Testing (✅ Completed)
- Unit tests for core functions
- Integration tests for database operations
- Deduplication tests
- Test fixtures for database
- Pytest configuration

### 8. CLI Interface (✅ Completed)
Commands:
- `run`: Execute complete pipeline
- `export`: Export from database
- `stats`: Show statistics
- `clear`: Clear database
- `info`: Show configuration

## Design Principles Applied

### SOLID
- **Single Responsibility**: Each module has one clear purpose
- **Open/Closed**: Base searcher extensible without modification
- **Liskov Substitution**: All searchers interchangeable
- **Interface Segregation**: Minimal required interface for searchers
- **Dependency Inversion**: Depend on abstractions (base classes)

### DRY (Don't Repeat Yourself)
- Shared logic in base classes and utilities
- Reusable caching mechanism
- Common data models

### KISS (Keep It Simple, Stupid)
- Clear module boundaries
- Straightforward data flow
- Minimal abstractions

### YAGNI (You Aren't Gonna Need It)
- No premature optimization
- Features implemented as needed
- TODOs for future enhancements

## TODOs for Future Improvements

### High Priority
- [ ] Parallel processing of API requests (concurrent.futures)
- [ ] Progress bars for long-running operations (tqdm)
- [ ] Configurable timeout values per API
- [ ] Retry strategies configuration
- [ ] More comprehensive error recovery

### Medium Priority
- [ ] Web interface for pipeline monitoring
- [ ] Real-time search progress dashboard
- [ ] Email notifications on completion
- [ ] Scheduled/automated runs
- [ ] Support for additional APIs (IEEE Xplore, ACM Digital Library)

### Low Priority
- [ ] Machine learning-based relevance scoring
- [ ] Automatic abstract summarization
- [ ] PDF download and full-text extraction
- [ ] Citation network analysis
- [ ] Visualization of search results

## Testing Strategy

### Quick Tests (`tests/quick/`)
- Fast unit tests (<1s each)
- Mock external dependencies
- Test core logic and data models
- Run before every commit

### Full Tests (`tests/full/`)
- Integration tests with real database
- End-to-end pipeline tests
- May use API mocks
- Run before releases

### Benchmark Tests (`tests/benchmark/`)
- Performance measurements
- Deduplication efficiency
- Database query speed
- Memory usage profiling

## Usage Examples

### Running the Pipeline
```bash
# Full pipeline with defaults
python research/improved_pipeline.py

# Via CLI with options
python research/cli.py run --max-results 20 --year-min 2018

# Export existing data
python research/cli.py export --format both

# Show statistics
python research/cli.py stats
```

### Programmatic Usage
```python
from research.improved_pipeline import run_pipeline

# Run with custom parameters
df = run_pipeline(
    max_results_per_query=15,
    year_min=2018,
    save_to_db=True,
    export_excel=True
)
```

## Migration from Notebook

Original notebook functionality mapped to modules:
- **Search functions** → `api_clients/*`
- **Cache management** → `utils/__init__.py`
- **Deduplication** → `deduplication.py`
- **Database operations** → `database.py`
- **Exports** → `exports.py`
- **Configuration** → `config.py`
- **Main execution** → `improved_pipeline.py`

## Dependencies

Core dependencies (already in requirements.txt):
- pandas: Data manipulation
- requests: HTTP requests
- scikit-learn: TF-IDF and similarity
- rapidfuzz: Fuzzy string matching
- python-dotenv: Environment variables
- click: CLI framework
- openpyxl: Excel export
- crossrefapi: Crossref API client

## Security Considerations

- API keys stored in .env (gitignored)
- No secrets in logs
- Sanitized error messages
- Rate limiting to prevent abuse
- Input validation on CLI parameters

## Performance Considerations

- Response caching reduces API calls
- Database indexing speeds up queries
- Batch operations for efficiency
- Blocking strategy for deduplication
- Configurable rate limits

## Documentation

- Module-level docstrings
- Function-level docstrings with types
- Inline comments for complex logic
- README updates with usage examples
- This refactoring plan document

## Validation

Pipeline validated through:
- ✅ Unit test suite passing
- ✅ Sample run with test queries
- ✅ Export generation verified
- ✅ Database operations tested
- ✅ CLI commands functional

## Conclusion

The refactoring successfully transforms the notebook into a production-ready, modular pipeline that:
- Follows software engineering best practices
- Is maintainable and extensible
- Has comprehensive test coverage
- Provides both CLI and programmatic interfaces
- Maintains all original functionality
- Improves reliability and error handling

The pipeline is ready for use in the TCC systematic review process and can be extended with additional features as needed.

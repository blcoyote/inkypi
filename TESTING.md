# InkyPi - Quick Test Reference

## Running Tests

### Basic Commands
```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov

# Run specific test file
pytest tests/unit/test_models.py

# Run in quiet mode (less output)
pytest -q

# Run in verbose mode (more detail)
pytest -v
```

### Coverage Reports
```bash
# Terminal report with missing line numbers
pytest --cov --cov-report=term-missing

# Generate HTML coverage report
pytest --cov --cov-report=html
# Then open: htmlcov/index.html

# Both terminal and HTML reports
pytest --cov --cov-report=term-missing --cov-report=html
```

### Run by Test Type
```bash
# Only unit tests
pytest -m unit

# Only integration tests
pytest -m integration

# Exclude slow tests
pytest -m "not slow"
```

### Run Specific Tests
```bash
# Specific test class
pytest tests/unit/test_models.py::TestAddress

# Specific test method
pytest tests/unit/test_models.py::TestAddress::test_from_dict_valid_data

# Tests matching pattern
pytest -k "test_from_dict"
```

### Watch Mode (Auto-rerun on changes)
```bash
# Install pytest-watch first
pip install pytest-watch

# Watch and rerun on file changes
ptw
```

## Current Test Status

- **Total Tests**: 83
- **Passing**: 83 (100%)
- **Coverage**: 67%
- **Execution Time**: ~1.5 seconds

## Coverage by Module

| Module | Coverage |
|--------|----------|
| `core/content_provider.py` | 100% |
| `core/models.py` | 97% |
| `rendering/layouts.py` | 97% |
| `utils/state.py` | 96% |
| `utils/api_client.py` | 81% |
| `core/waste_repository.py` | 68% |
| **Overall** | **67%** |

## Test Files

```
tests/
├── conftest.py                   # Shared fixtures
├── unit/
│   ├── test_models.py           # 20 tests
│   ├── test_state_manager.py    # 16 tests
│   ├── test_api_client.py       # 18 tests
│   ├── test_content_provider.py # 8 tests
│   └── test_layouts.py          # 10 tests
└── integration/
    └── test_waste_repository.py # 11 tests
```

## Troubleshooting

### Tests not found
```bash
# Make sure you're in the project root
cd C:\Users\blc\Documents\inkypi

# Verify pytest can find tests
pytest --collect-only
```

### Import errors
```bash
# Ensure virtual environment is activated
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Verify pytest is installed
pytest --version
```

### Coverage not working
```bash
# Install coverage plugin
pip install pytest-cov

# Run with explicit coverage config
pytest --cov=core --cov=utils --cov=rendering
```

## Reading Coverage Reports

### Terminal Output
```
Name                  Stmts   Miss  Cover   Missing
---------------------------------------------------
core/models.py           73      2    97%   94-95
utils/state.py           49      2    96%   48-49
```

- **Stmts**: Total statements in file
- **Miss**: Uncovered statements
- **Cover**: Percentage covered
- **Missing**: Line numbers not covered

### HTML Report
Open `htmlcov/index.html` in browser:
- Click files to see line-by-line coverage
- Red lines = not covered
- Green lines = covered
- Yellow lines = partially covered

## Quick Verification

```bash
# Quick check - all tests pass?
pytest -q

# Full check with coverage
pytest --cov --cov-report=term-missing

# Verify application still works
python main.py
```

## Best Practices

1. **Run tests before committing code**
2. **Check coverage for new code** (aim for 80%+)
3. **Use descriptive test names** (test_method_scenario_result)
4. **Keep tests fast** (< 5 seconds total)
5. **Mock external dependencies** (API, hardware, filesystem)

## More Information

- Full test plan: [TEST_PLAN.md](TEST_PLAN.md)
- Implementation summary: [TEST_SUMMARY.md](TEST_SUMMARY.md)
- pytest documentation: https://docs.pytest.org/

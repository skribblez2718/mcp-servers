# Test Suite for Open WebUI MCP Server

Comprehensive test suite with >80% code coverage.

## Test Structure

```
tests/
├── conftest.py              # Shared fixtures
├── fixtures/
│   ├── openapi_responses.py # Mock API responses from OpenAPI spec
│   └── test_data.py         # Common test data
├── unit/
│   ├── test_config.py       # Configuration validation tests
│   ├── test_exceptions.py   # Exception hierarchy tests
│   ├── utils/               # Utility function tests
│   │   ├── test_validation.py
│   │   ├── test_rate_limiter.py
│   │   ├── test_error_handler.py
│   │   └── test_url_builder.py
│   ├── services/
│   │   └── test_client.py   # OpenWebUIClient tests
│   └── tools/
│       ├── test_chat_list_tool.py
│       └── test_factory.py  # ToolFactory tests
└── integration/
    ├── conftest.py          # Integration fixtures
    └── test_local_api.py    # Tests against local Open WebUI
```

## Running Tests

### All tests with coverage
```bash
# Requires OPENWEBUI_API_KEY environment variable
OPENWEBUI_API_KEY=sk-your_api_key_here uv run pytest
```

### Unit tests only (no API key required)
```bash
uv run pytest tests/unit -m unit
```

### Integration tests (requires local Open WebUI and API key)
```bash
# Method 1: Pass API key via environment
OPENWEBUI_API_KEY=sk-your_api_key_here uv run pytest tests/integration -m integration

# Method 2: Set in .env first
uv run pytest tests/integration -m integration
```

### Specific test file
```bash
uv run pytest tests/unit/test_config.py -v
```

### With detailed output
```bash
uv run pytest -vv --tb=long
```

### Generate HTML coverage report
```bash
uv run pytest --cov=src --cov-report=html
open htmlcov/index.html
```

## Test Categories

### Unit Tests (Fast)
- **Config**: Validation, defaults, environment variables
- **Exceptions**: Custom exception hierarchy
- **Validation**: ID, pagination, string, enum, path sanitization
- **Rate Limiter**: Token bucket algorithm, concurrency
- **Error Handler**: Message sanitization, HTTP error transformation
- **URL Builder**: Parameter encoding, safety checks
- **Client**: GET requests, error handling, rate limiting
- **Tools**: Input validation, API calls, response transformation
- **Factory**: Lazy loading, dependency injection, caching

### Integration Tests (Requires Local Instance and API Key)
- **Local API**: Real API calls to verify generated code
- **Authentication**: Verify API key authentication with Bearer header
- **Rate Limiting**: Verify rate limiter works with real API
- **Pagination**: Test pagination against actual data
- **Error Handling**: Verify error responses from API (including 401 Unauthorized)
- **API Key Format**: Tests validate `sk-xxxxx...` format authentication

## Fixtures

### Common Fixtures (`conftest.py`)
- `mock_config`: Mock configuration
- `real_config`: Real configuration for integration tests
- `mock_rate_limiter`: Mock rate limiter (always allows)
- `mock_client`: Mock OpenWebUI client
- `real_client`: Real client for integration tests
- `tool_factory`: Tool factory with mocks
- `sample_*_data`: Realistic sample data from OpenAPI spec

### Integration Fixtures (`integration/conftest.py`)
- `local_webui_available`: Check if local instance running
- `skip_if_no_local_webui`: Skip test if no local instance
- `integration_config`: Config for integration tests

## Test Data

All mock responses in `fixtures/openapi_responses.py` are based on actual OpenAPI specification examples for realism.

## Coverage Requirements

- **Target**: >80% code coverage
- **Critical paths**: 100% (validation, error handling)
- **Enforced**: Tests fail if coverage <80%

Run coverage check:
```bash
uv run pytest --cov-fail-under=80
```

## Integration Test Setup

To run integration tests against local Open WebUI:

1. Start local Open WebUI instance:
```bash
docker run -d -p 8080:8080 ghcr.io/open-webui/open-webui:main
```

2. Get API key from Open WebUI:
   - Open http://localhost:8080 in browser
   - Go to Settings → Account → API Keys
   - Create/copy API key
   - Export in shell or add to `.env`:
   ```bash
   export OPENWEBUI_API_KEY=sk-your_api_key_here
   ```

3. Run integration tests:
```bash
# Method 1: With environment variable
OPENWEBUI_API_KEY=sk-your_api_key_here uv run pytest tests/integration -m integration

# Method 2: Set in .env
echo "OPENWEBUI_API_KEY=sk-your_api_key_here" >> .env
uv run pytest tests/integration -m integration
```

4. Skip integration tests if no local instance:
```bash
uv run pytest -m "not integration"
```

## Test Markers

- `@pytest.mark.unit`: Fast unit test
- `@pytest.mark.integration`: Requires local Open WebUI
- `@pytest.mark.slow`: Test takes >1s
- `@pytest.mark.asyncio`: Async test

## Writing New Tests

1. **Unit tests**: Mock all external dependencies
2. **Integration tests**: Use real API, mark with `@pytest.mark.integration`
3. **Follow patterns**: See existing tests for structure
4. **Use fixtures**: Reuse common fixtures from conftest.py
5. **Test edge cases**: Boundary conditions, errors, empty inputs

## Continuous Integration

Tests are designed to run in CI environments:
- Unit tests run always (fast, no dependencies)
- Integration tests run only if `CI_INTEGRATION=true` env var set
- Coverage report uploaded as artifact

## Troubleshooting

### Import Errors
```bash
# Ensure dependencies installed
uv sync

# Run tests with uv
uv run pytest
```

### Integration Tests Failing
```bash
# Check if local Open WebUI running
curl http://localhost:8080/api/health

# Skip integration tests
uv run pytest -m "not integration"
```

### Coverage Too Low
```bash
# See missing coverage
uv run pytest --cov=src --cov-report=term-missing

# Generate HTML report for detailed view
uv run pytest --cov=src --cov-report=html
```

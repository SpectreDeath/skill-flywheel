---
name: comprehensive-testing-harness
description: "Use when: writing tests, running test suites, debugging test failures, analyzing coverage, generating tests with AI, or implementing testing best practices. Covers pytest, vitest, jest, playwright. Triggers: 'test', 'pytest', 'unit test', 'integration test', 'e2e', 'coverage', 'expect', 'assert', 'mock', 'fixture', 'playwright', 'vitest', 'jest', 'debug test', 'test failure'. NOT for: production monitoring (use observability skills), or manual QA."
---

# Comprehensive Testing Harness

Complete testing framework with unit tests, integration tests, e2e tests, coverage analysis, and AI-assisted test generation.

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    Testing Harness                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │    Unit     │  │ Integration│  │     E2E     │             │
│  │   Tests     │  │   Tests    │  │   Tests     │             │
│  └─────────────┘  └─────────────┘  └─────────────┘             │
│         │               │               │                       │
│         v               v               v                       │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │              Test Runner & Collector                     │    │
│  │         (pytest, vitest, jest, playwright)              │    │
│  └─────────────────────────────────────────────────────────┘    │
│         │                                                       │
│         v                                                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │  Coverage    │  │   Report    │  │  AI Test     │          │
│  │  Analyzer    │  │  Generator  │  │  Generator   │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Unit Testing

```python
import pytest
from unittest.mock import Mock, patch, MagicMock

class TestUnitPatterns:
    """Unit testing patterns and best practices."""
    
    def test_with_mock(self):
        """Basic mock usage."""
        mock = Mock()
        mock.return_value = "result"
        
        result = mock("arg")
        assert result == "result"
        mock.assert_called_once_with("arg")
        
    def test_with_patch(self):
        """Patch external dependencies."""
        with patch("module.ExternalClass") as mock_cls:
            mock_instance = Mock()
            mock_instance.method.return_value = "mocked"
            mock_cls.return_value = mock_instance
            
            # Test code that uses ExternalClass
            result = your_function()
            assert result == "expected"
            
    def test_with_property_mock(self):
        """Mock properties and methods."""
        mock = MagicMock()
        mock.method.return_value = "value"
        mock.property = "prop_value"
        
        assert mock.method() == "value"
        assert mock.property == "prop_value"
        
    def test_exception_handling(self):
        """Test exception raising."""
        with pytest.raises(ValueError) as exc_info:
            function_that_raises()
        assert "expected message" in str(exc_info.value)
        
    def test_parametrized(self):
        """Parametrized tests for multiple inputs."""
        @pytest.mark.parametrize("input,expected", [
            (1, 2),
            (2, 4),
            (3, 6),
        ])
        def test_multiply(input, expected):
            assert input * 2 == expected
```

## Integration Testing

```python
import pytest
from httpx import AsyncClient

@pytest.fixture
async def test_client():
    """Create test client for API testing."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client

class TestIntegration:
    """Integration test patterns."""
    
    @pytest.mark.asyncio
    async def test_api_endpoint(self, test_client):
        """Test API endpoint."""
        response = await test_client.get("/api/users")
        assert response.status_code == 200
        assert "users" in response.json()
        
    @pytest.mark.asyncio  
    async def test_database_integration(self, test_db):
        """Test database integration."""
        # Create record
        user = await create_user(test_db, name="test")
        
        # Query and verify
        result = await get_user(test_db, user.id)
        assert result.name == "test"
        
    @pytest.mark.integration
    async def test_external_service(self):
        """Test external service integration."""
        with mock_external_service() as mock:
            result = await call_service()
            mock.assert_called_once()
```

## End-to-End Testing (Playwright)

```python
import pytest
from playwright.sync_api import Page, expect

class TestE2E:
    """End-to-end test patterns."""
    
    @pytest.fixture
    def page(self, browser):
        """Create page fixture."""
        context = browser.new_context()
        page = context.new_page()
        yield page
        context.close()
        
    def test_login_flow(self, page: Page):
        """Test complete login flow."""
        page.goto("/login")
        page.fill("[name=email]", "test@example.com")
        page.fill("[name=password]", "password123")
        page.click("[type=submit]")
        
        expect(page).to_have_url("/dashboard")
        expect(page.locator(".welcome")).to_contain_text("Welcome")
        
    def test_form_submission(self, page: Page):
        """Test form with validation."""
        page.goto("/form")
        
        # Empty submission
        page.click("[type=submit]")
        expect(page.locator(".error")).to_be_visible()
        
        # Valid submission
        page.fill("[name=email]", "valid@example.com")
        page.click("[type=submit]")
        expect(page.locator(".success")).to_be_visible()
        
    def test_api_interaction(self, page: Page):
        """Test API interaction."""
        page.goto("/data")
        
        # Wait for API response
        page.wait_for_response(
            lambda r: r.url.endswith("/api/data") and r.status == 200
        )
        
        expect(page.locator(".data-row")).to_have_count(10)
        
    def test_authenticated_request(self, page: Page):
        """Test authenticated API calls."""
        # Set auth token
        page.evaluate("""
            localStorage.setItem('token', 'test-token')
        """)
        
        page.goto("/protected")
        expect(page.locator(".content")).to_be_visible()
```

## Coverage Analysis

```python
import pytest
import coverage

class CoverageAnalyzer:
    """Analyze and report test coverage."""
    
    def __init__(self):
        self.cov = coverage.Coverage(
            source=["src"],
            omit=["*/tests/*", "*/migrations/*"]
        )
        
    def run_with_coverage(self, test_args):
        """Run tests with coverage."""
        self.cov.start()
        pytest.main(test_args)
        self.cov.stop()
        
        return self.cov.report()
        
    def get_uncovered_lines(self):
        """Get uncovered line numbers."""
        return self.cov.get_data().uncovered_lines()
        
    def generate_html_report(self, output_dir):
        """Generate HTML coverage report."""
        self.cov.html_report(directory=output_dir)
        
    def enforce_threshold(self, min_coverage=80):
        """Fail if coverage below threshold."""
        coverage_percent = self.cov.report()
        if coverage_percent < min_coverage:
            raise CoverageError(
                f"Coverage {coverage_percent}% < {min_coverage}%"
            )
```

## AI Test Generation

```python
import openai

class AITestGenerator:
    """Generate tests using AI."""
    
    def __init__(self, api_key: str):
        self.client = openai.Client(api_key=api_key)
        
    def generate_unit_tests(self, code: str) -> list[str]:
        """Generate unit tests for code."""
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[{
                "role": "system",
                "content": "Generate pytest unit tests for this code."
            }, {
                "role": "user", 
                "content": code
            }]
        )
        return response.choices[0].message.content
        
    def generate_test_cases(self, spec: str) -> list[str]:
        """Generate test cases from spec."""
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[{
                "role": "system",
                "content": """Generate comprehensive test cases.
                Include: happy path, edge cases, error cases, 
                boundary conditions."""
            }, {
                "role": "user",
                "content": spec
            }]
        )
        return parse_test_cases(response)
        
    def suggest_missing_tests(self, code: str, existing_tests: list) -> list[str]:
        """Suggest missing test coverage."""
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[{
                "role": "system",
                "content": "Suggest missing test cases."
            }, {
                "role": "user",
                "content": f"Code:\n{code}\n\nExisting tests:\n{existing_tests}"
            }]
        )
        return response.choices[0].message.content
```

## Test Fixtures and Factories

```python
import pytest
from factory import Factory, LazyAttribute

class UserFactory(Factory):
    class Meta:
        model = User
        
    id = LazyAttribute(lambda _: uuid4())
    name = "Test User"
    email = LazyAttribute(lambda self: f"{self.name.lower()}@test.com")
    created_at = LazyAttribute(lambda: datetime.now())

class TestFixtures:
    """Fixture patterns."""
    
    @pytest.fixture
    def sample_user(self):
        """Create sample user."""
        return UserFactory()
        
    @pytest.fixture
    def multiple_users(self):
        """Create multiple users."""
        return [UserFactory() for _ in range(5)]
        
    @pytest.fixture
    def authenticated_client(self, client):
        """Authenticated API client."""
        client.headers["Authorization"] = "Bearer test-token"
        return client
        
    @pytest.fixture(scope="session")
    def db_session():
        """Session-scoped database."""
        session = create_test_db()
        yield session
        cleanup_test_db(session)
```

## Test Organization

```python
# conftest.py - shared fixtures
pytest_plugins = ["pytest_asyncio", "pytest_cov"]

def pytest_configure(config):
    config.addinivalue_line("markers", "slow: slow running tests")
    config.addinivalue_line("markers", "integration: integration tests")
    config.addinivalue_line("markers", "e2e: end-to-end tests")

# pytest.ini
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = "test_*.py"
python_classes = "Test*"
python_functions = "test_*"
addopts = "-v --strict-markers"
markers = [
    "slow: marks tests as slow",
    "integration: marks tests as integration tests"
]
```

## CI Integration

```yaml
# .github/workflows/test.yml
name: Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - run: pytest --cov=src --cov-report=xml
      - uses: codecov/codecov-action@v4
        with:
          file: coverage.xml
```

## Constraints

- MUST use descriptive test names
- SHOULD follow AAA pattern (Arrange, Act, Assert)
- MUST isolate tests from each other
- SHOULD use fixtures for shared setup
- MUST clean up resources in teardown
- SHOULD test edge cases and error paths
- SHOULD aim for >80% coverage on critical paths
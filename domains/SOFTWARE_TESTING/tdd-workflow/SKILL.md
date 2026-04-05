---
name: tdd-workflow
description: "Use when: writing new features, fixing bugs, or refactoring code with test-driven development methodology. Enforces 80%+ test coverage including unit, integration, and E2E tests. Triggers: 'TDD', 'test driven', 'write tests first', 'red green refactor', 'test coverage', 'unit test', 'integration test'. NOT for: prototype code, experiments, or one-off scripts that won't be maintained."
---

# TDD Workflow

Test-driven development workflow enforcing 80%+ test coverage including unit, integration, and E2E tests.

## When to Use This Skill

Use this skill when:
- Writing new features for production code
- Fixing bugs that need regression prevention
- Refactoring existing code
- Building reusable libraries or components
- Any code that will be maintained long-term

Do NOT use when:
- Prototype code or experiments
- One-off scripts that won't be reused
- Quick proofs of concept
- Code where test overhead exceeds value

## TDD Cycle: Red-Green-Refactor

### 1. Red: Write a Failing Test
```
1. Understand the requirement
2. Write test that describes desired behavior
3. Run test - it should FAIL
4. Verify failure is for right reason (not missing import, etc.)
```

### 2. Green: Make the Test Pass
```
1. Write minimal code to pass test
2. No optimization yet - just get green
3. Run tests - should all pass
4. Only move on when tests pass
```

### 3. Refactor: Improve Code
```
1. Clean up code while tests pass
2. Remove duplication
3. Improve naming
4. Add new tests for edge cases
5. Run tests after each change
```

## Test Coverage Requirements

### Minimum Coverage Thresholds
- **Unit Tests**: 80% line coverage
- **Integration Tests**: Critical path coverage
- **E2E Tests**: Key user workflows

### Coverage Enforcement
```python
# pytest.ini
[tool.pytest.coverage]
fail_under = 80
exclude_lines = [
    "pragma: no cover",
    "if __name__ == .__main__.:",
    "raise NotImplementedError",
]
```

### Test Organization
```
tests/
├── unit/
│   ├── test_module_a.py
│   └── test_module_b.py
├── integration/
│   ├── test_api_endpoints.py
│   └── test_database.py
└── e2e/
    ├── test_user_flows.py
    └── test_checkout.py
```

## Test Types and When to Use

### Unit Tests
```python
def test_calculate_discount_applies_percentage():
    """Test single function in isolation"""
    result = calculate_discount(100, 0.10)
    assert result == 10
```

**Use for**: Individual functions, classes, small units of logic

### Integration Tests
```python
def test_api_returns_user_with_orders():
    """Test multiple units working together"""
    response = client.get('/api/users/1')
    assert response.status_code == 200
    assert 'orders' in response.json()
```

**Use for**: Database operations, API endpoints, service interactions

### E2E Tests
```python
def test_user_can_checkout():
    """Test full user workflow"""
    page.goto('/cart')
    page.click('#checkout')
    page.fill('#email', 'user@test.com')
    page.click('#submit')
    expect(page.locator('.confirmation')).to_be_visible()
```

**Use for**: Critical user journeys, payment flows, authentication

## Writing Effective Tests

### Test Naming Convention
```python
def test_function_name_given_condition_expect_result():
    # Arrange - set up test data
    # Act - call function
    # Assert - verify result
```

### AAA Pattern
```python
def test_order_total_with_tax():
    # Arrange
    order = Order(items=[Item(price=100), Item(price=50)])
    
    # Act
    total = order.calculate_total()
    
    # Assert
    assert total == 165  # 150 + 15 tax
```

### Avoiding Test Fragility
```python
# Bad - fragile, breaks on any HTML change
assert 'Hello' in page.locator('div:nth-child(3) > span').text()

# Good - stable, uses semantic selectors
assert page.locator('.user-greeting').text() == 'Hello'
```

## Mocking and Test Databases

### Proper Mock Usage
```python
def test_send_email_calls_provider():
    mock_provider = Mock()
    service = EmailService(provider=mock_provider)
    
    service.send('test@example.com', 'Subject', 'Body')
    
    mock_provider.send.assert_called_once()
```

### Test Database Patterns
```python
@pytest.fixture
def test_db():
    """Create in-memory test database"""
    db = create_test_database()
    yield db
    db.cleanup()
```

## Running Tests

### CI/CD Test Commands
```bash
# Unit tests with coverage
npm run test:unit -- --coverage

# Integration tests
npm run test:integration

# E2E tests
npm run test:e2e

# All tests
npm run test:all
```

### Test Execution Order
```bash
# Run fast tests first
pytest -m "not slow"

# Run only unit tests
pytest tests/unit/

# Run with coverage
pytest --cov=src --cov-report=html
```

## Test-Driven Bug Fixing

### Before Fixing a Bug
1. Write test that reproduces bug
2. Verify test fails
3. Fix code
4. Verify test passes
5. Add regression test

```python
def test_login_with_wrong_password():
    """Bug reproduction test"""
    with patch('auth.verify_password', return_value=False):
        result = login('user@test.com', 'wrong')
        assert result.success is False
        assert 'Invalid' in result.error
```

## Constraints

- Never skip tests to meet deadlines
- Test should be deterministic (no flaky tests)
- Each test should test one thing
- Tests should not depend on each other
- Use descriptive test names
- Keep tests fast for rapid iteration
- 80% coverage is minimum, not target

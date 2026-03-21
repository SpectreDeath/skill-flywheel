# Contributing to Skill Flywheel

Welcome! This guide will help you get started with contributing to Skill Flywheel.

## Quick Start

```bash
# Clone the repository
git clone https://github.com/SpectreDeath/skill-flywheel.git
cd skill-flywheel

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Run tests
pytest tests/
```

## Development Setup

### Prerequisites
- Python 3.10+
- pip
- git

### Running the Server
```bash
cd src/flywheel
python -m server.config  # Or use server.py
```

## Code Standards

### Linting
We use Ruff for linting:
```bash
ruff check src/ tests/
```

### Type Checking
We use mypy for type checking:
```bash
mypy src/
```

### Testing
```bash
# Run all tests
pytest tests/

# Run with coverage
pytest tests/ --cov=src --cov-report=term
```

## Pull Request Process

1. **Create a feature branch:**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes:**
   - Follow the existing code style
   - Add tests for new functionality
   - Update documentation as needed

3. **Run checks locally:**
   ```bash
   ruff check src/ tests/
   pytest tests/
   ```

4. **Commit your changes:**
   ```bash
   git add .
   git commit -m "feat: Add your feature"
   ```

5. **Push and create PR:**
   ```bash
   git push origin feature/your-feature-name
   ```

## Commit Message Format

We follow Conventional Commits:
- `feat:` New feature
- `fix:` Bug fix
- `refactor:` Code refactoring
- `docs:` Documentation changes
- `test:` Test changes
- `chore:` Maintenance

## Project Structure

```
skill-flywheel/
├── src/flywheel/          # Main source code
│   ├── core/             # Core modules
│   ├── server/           # Server components
│   ├── skills/           # Skill implementations
│   └── monitoring/       # Monitoring tools
├── tests/                # Test files
├── docs/                 # Documentation
└── domains/             # Skill domain specifications
```

## Getting Help

- Open an issue for bugs or feature requests
- Check existing issues before creating new ones

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

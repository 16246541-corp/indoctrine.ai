# Contributing to Agent Indoctrination

Thank you for your interest in contributing to the Agent Indoctrination framework! We welcome contributions from the community.

## How to Contribute

### Reporting Bugs

If you find a bug, please open an issue on GitHub with:
- A clear description of the problem
- Steps to reproduce the issue
- Expected vs actual behavior
- Your environment (OS, Python version, package version)

### Suggesting Enhancements

We welcome feature requests! Please open an issue with:
- A clear description of the enhancement
- Use cases and benefits
- Any implementation ideas you might have

### Pull Requests

1. **Fork the repository** and create your branch from `main`
2. **Make your changes** with clear, descriptive commits
3. **Add tests** for any new functionality
4. **Update documentation** as needed
5. **Ensure tests pass**: `pytest tests/`
6. **Format your code**: `black . && ruff check .`
7. **Submit a pull request** with a clear description of changes

## Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/agent-indoctrination.git
cd agent-indoctrination

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode with all extras
pip install -e ".[all,dev]"

# Install pre-commit hooks
pre-commit install
```

## Code Style

- Follow PEP 8 guidelines
- Use type hints for all functions
- Write docstrings for all public APIs (Google style)
- Keep line length to 100 characters
- Use `black` for formatting and `ruff` for linting

## Testing

- Write unit tests for all new code
- Maintain >80% code coverage
- Run tests before submitting PR: `pytest tests/ -v`
- Test with multiple Python versions if possible (3.10, 3.11, 3.12)

## Adding New Features

### New Attack Strategies
Place in `agent_indoctrination/engines/attack/` and inherit from base attack class.

### New Compliance Frameworks
Add to `agent_indoctrination/engines/governance/` following existing patterns.

### New Metrics
Add to `agent_indoctrination/reporting/benchmark.py` and update report templates.

## Documentation

- Update relevant documentation in `docs/`
- Add examples to `examples/` for new features
- Keep README.md up to date
- Document breaking changes clearly

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Questions?

Feel free to open an issue for any questions or reach out to the maintainers.

Thank you for contributing! 🎉

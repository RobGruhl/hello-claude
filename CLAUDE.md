# CLAUDE.md - Python Project Configuration and Guidelines

## Build & Test Commands
- Install: `pip install -e .`
- Lint: `ruff check .`
- Type Check: `mypy .`
- Format: `black .`
- Test (all): `pytest`
- Test (single): `pytest tests/test_file.py::test_function`
- Run: `python -m project_name`

## Code Style Guidelines
- **Formatting**: Use Black with default settings
- **Imports**: Use isort, group by stdlib, third-party, first-party
- **Types**: Use type hints with mypy
- **Naming**: 
  - Functions/variables/modules: snake_case
  - Classes: PascalCase
  - Constants: UPPER_SNAKE_CASE
- **Error handling**: Use specific exceptions, context managers
- **Docstrings**: Google-style docstrings for public functions and classes

## Project Structure
This is a new Python project. The structure will evolve as development progresses.
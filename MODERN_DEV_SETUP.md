# Modern Development Setup with UV

This guide shows how to set up a clean, modern Python development environment using `uv` (the fast Python package manager) instead of traditional `venv` + `pip`.

## Why UV?

- **10-100x faster** than pip for dependency resolution and installation
- **Built-in virtual environment** management (no separate `venv` commands)
- **Better dependency resolution** (avoids conflicts we had with OpenTelemetry)
- **Modern Python packaging** standard (actively maintained by Astral)
- **Cross-platform** and **deterministic** builds

## Clean Setup Process

### 1. Remove Old Environment

```bash
# Navigate to project
cd /path/to/tcgplayer_client

# Remove old virtual environments
rm -rf venv/
rm -rf test_env/
rm -rf .venv/
rm -rf tcgplayer_client.egg-info/

# Clear any cached build artifacts
rm -rf build/
rm -rf dist/
rm -rf .pytest_cache/
rm -rf .mypy_cache/
```

### 2. Install UV

```bash
# Install uv via Homebrew (recommended on macOS)
brew install uv

# Verify installation
uv --version
```

### 3. Initialize Project with UV

```bash
# Navigate to project root
cd /path/to/tcgplayer_client

# Initialize UV project (creates .python-version and uv.lock)
uv init --app --python 3.11

# Or if you want to use existing pyproject.toml
uv sync
```

### 4. Install Dependencies

```bash
# Install all dependencies (automatically creates virtual environment)
uv sync

# Or install specific dependency groups
uv sync --group dev

# Add new dependencies (automatically updates uv.lock)
uv add requests aiohttp
uv add --dev pytest black mypy
```

### 5. Development Commands

```bash
# Run commands in UV environment (replaces 'source venv/bin/activate')
uv run python script.py
uv run pytest
uv run black .
uv run mypy .

# Or activate shell (if you prefer traditional activation)
source .venv/bin/activate

# Install project in editable mode
uv pip install -e .
```

## Project-Specific Setup

### For TCGplayer Client:

```bash
# 1. Clean old setup
rm -rf venv/ test_env/ .venv/ tcgplayer_client.egg-info/
rm -rf build/ dist/ .pytest_cache/ .mypy_cache/

# 2. Install UV
brew install uv

# 3. Set up project
uv sync --all-extras

# 4. Run tests
uv run pytest tests/test_endpoints_inventory.py -v

# 5. Run full test suite
uv run pytest --cov=tcgplayer_client --cov-report=html

# 6. Code quality checks
uv run black .
uv run flake8
uv run mypy tcgplayer_client/
```

## UV Configuration

### Create `.python-version` (UV will auto-detect):
```
3.11
```

### Update `pyproject.toml` for UV compatibility:
```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "tcgplayer_client"
dynamic = ["version"]
dependencies = [
    "aiohttp>=3.8.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "pytest-asyncio>=0.21.0",
    "pytest-cov>=4.0.0",
    "black>=23.0.0",
    "flake8>=6.0.0",
    "mypy>=1.0.0",
]

[tool.uv]
dev-dependencies = [
    "pytest>=7.0.0",
    "pytest-asyncio>=0.21.0",
    "pytest-mock>=3.10.0",
    "black>=23.0.0",
    "flake8>=6.0.0",
    "mypy>=1.0.0",
]
```

## Daily Workflow

```bash
# Start development
cd tcgplayer_client

# Quality checks using Makefile (recommended)
make format           # Format code with Black
make lint             # Run Flake8 linting  
make type-check       # Run MyPy type checking
make test             # Run full test suite
make test-fast        # Run tests without coverage

# Or run individual UV commands
uv run pytest tests/
uv run pytest tests/test_endpoints_catalog.py -v
uv run black .
uv run flake8 tcgplayer_client/ tests/
uv run mypy tcgplayer_client/

# Package management
uv add new-package
uv sync --all-extras
uv lock --upgrade

# Install project for development
uv pip install -e .
```

## Environment Variables

Create `.env` file (UV will auto-load it):
```bash
TCGPLAYER_CLIENT_ID="your_client_id"
TCGPLAYER_CLIENT_SECRET="your_client_secret"
TCGPLAYER_LOG_LEVEL="DEBUG"
```

## Makefile Integration

Update existing `Makefile` to use UV:

```makefile
# Use UV instead of pip/python
PYTHON := uv run python
PYTEST := uv run pytest
BLACK := uv run black
FLAKE8 := uv run flake8
MYPY := uv run mypy

.PHONY: install
install:
	uv sync --all-extras

.PHONY: test
test:
	$(PYTEST) tests/ -v

.PHONY: test-cov
test-cov:
	$(PYTEST) --cov=tcgplayer_client --cov-report=html --cov-report=term-missing

.PHONY: format
format:
	$(BLACK) .

.PHONY: lint
lint:
	$(FLAKE8) tcgplayer_client tests

.PHONY: type-check
type-check:
	$(MYPY) tcgplayer_client/

.PHONY: ci
ci: format lint type-check test
```

## VS Code Integration

Update `.vscode/settings.json`:
```json
{
    "python.pythonPath": ".venv/bin/python",
    "python.terminal.activateEnvironment": false,
    "python.defaultInterpreterPath": ".venv/bin/python"
}
```

## Benefits Over Traditional Setup

1. **No more `source venv/bin/activate`** - UV handles environments automatically
2. **Faster installs** - Parallel downloads and better caching
3. **Lock files** - Deterministic, reproducible builds
4. **Better error messages** - Clear dependency conflict resolution
5. **Modern tooling** - Integrates well with modern Python ecosystem

## Migration Checklist ✅ COMPLETED

- [x] Remove old virtual environments (`rm -rf venv/ test_env/`)
- [x] Install UV (`brew install uv`) - version 0.8.15
- [x] Run `uv sync --all-extras` to create new environment
- [x] Update scripts to use `uv run` commands
- [x] Update Makefile to use UV (all targets working)
- [x] Test that `uv run pytest` works (all 161 tests, 41 catalog tests passing)
- [x] Create `.flake8` config with line length 88
- [x] Update `pyproject.toml` with modern hatchling build system
- [x] Document team setup process

## Troubleshooting

### Common Issues:

**UV not found:**
```bash
# Ensure UV is in PATH
echo $PATH
which uv
```

**Python version issues:**
```bash
# Set specific Python version
uv python install 3.11
uv python pin 3.11
```

**Dependency conflicts:**
```bash
# UV shows better error messages - follow suggestions
uv sync --resolution=highest
```

**VS Code not detecting environment:**
```bash
# Point VS Code to .venv/bin/python manually
# Or restart VS Code after uv sync
```

This modern setup will make development much faster and more reliable for future projects!
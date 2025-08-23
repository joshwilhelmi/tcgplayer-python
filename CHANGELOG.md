# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.1] - 2024-12-19

### Fixed
- **Code Quality**: Resolved all flake8 linting issues
  - Fixed line length violations (E501) across all modules
  - Removed unused imports (F401) from core modules and test files
  - Fixed undefined variable references (F821)
  - Cleaned up trailing whitespace (W291, W293)
  - Fixed spacing issues (E302, E303)
- **Import Cleanup**: Streamlined imports in test files, removing unused mock objects and exception classes
- **Code Formatting**: Improved code readability with proper line breaks and consistent formatting
- **Documentation**: Fixed docstring line length issues for better readability

### Technical Details
- All modules now comply with 88-character line length limit
- Removed 20+ unused imports across the codebase
- Fixed exception handling in retry logic
- Added missing logger imports where needed
- Maintained 100% test coverage (90 tests passing)

## [1.0.0] - 2024-12-19

### Added
- Initial release of TCGplayer Client library
- Full API coverage for all 67 documented endpoints
- Async/await support throughout
- Comprehensive rate limiting and retry logic
- OAuth2 authentication with automatic token refresh
- Full type hint support
- Comprehensive error handling with custom exceptions
- Organized endpoint classes for different API categories
- Extensive test coverage

### Features
- **Catalog Endpoints**: Product categories, groups, and details
- **Pricing Endpoints**: Market prices and price guides  
- **Store Endpoints**: Store information and inventory
- **Order Endpoints**: Order management and tracking
- **Inventory Endpoints**: Inventory management
- **Buylist Endpoints**: Buylist operations

### Technical
- Built with Python 3.8+ support
- Uses aiohttp for async HTTP requests
- Configurable rate limiting (default: 10 req/s)
- Configurable retry logic with exponential backoff
- Comprehensive logging throughout
- Full test suite with pytest

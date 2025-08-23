# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial package configuration for pip installation
- Comprehensive documentation and README
- Development environment setup

## [1.0.0] - 2024-12-19

### Added
- Initial release of TCGPlayer Client library
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

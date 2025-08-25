#!/bin/bash

# TCGplayer Client - Local CI Pipeline
# This script mimics the GitHub Actions pipeline exactly
# Run this before committing to catch issues early

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to install missing tools
install_tool() {
    local tool=$1
    local install_cmd=$2
    
    if ! command_exists "$tool"; then
        print_warning "$tool not found. Installing..."
        eval "$install_cmd"
    else
        print_success "$tool is already installed"
    fi
}

# Check Python version
check_python_version() {
    print_status "Checking Python version..."
    python_version=$(python3 --version 2>&1 | awk '{print $2}')
    print_success "Python version: $python_version"
}

# Install development dependencies
install_dependencies() {
    print_status "Installing development dependencies..."
    
    # Check if virtual environment is activated
    if [[ "$VIRTUAL_ENV" == "" ]]; then
        print_warning "Virtual environment not detected. Please activate your venv first."
        print_status "You can activate it with: source venv/bin/activate"
        exit 1
    fi
    
    # Install requirements
    if [ -f "requirements-dev.txt" ]; then
        pip install -r requirements-dev.txt
        print_success "Development dependencies installed"
    else
        print_warning "requirements-dev.txt not found, installing common dev tools..."
        pip install black flake8 isort mypy pytest pytest-cov bandit safety semgrep pip-audit
        print_success "Common development tools installed"
    fi
}

# Code formatting checks
run_formatting_checks() {
    print_status "Running code formatting checks..."
    
    # Black formatting check
    print_status "Checking Black formatting..."
    if black --check --diff .; then
        print_success "Black formatting check passed"
    else
        print_error "Black formatting check failed. Run 'make format' to fix."
        exit 1
    fi
    
    # isort import sorting check
    print_status "Checking isort import sorting..."
    if isort --check-only --diff .; then
        print_success "isort import sorting check passed"
    else
        print_error "isort import sorting check failed. Run 'make import-sort' to fix."
        exit 1
    fi
}

# Linting checks
run_linting_checks() {
    print_status "Running linting checks..."
    
    # Flake8 linting
    print_status "Running Flake8 linting..."
    if flake8 tcgplayer_client/ tests/ --max-line-length=88 --extend-ignore=E203,W503; then
        print_success "Flake8 linting passed"
    else
        print_error "Flake8 linting failed. Please fix the issues above."
        exit 1
    fi
}

# Type checking
run_type_checks() {
    print_status "Running type checks..."
    
    # MyPy type checking
    print_status "Running MyPy type checking..."
    if mypy tcgplayer_client/ --ignore-missing-imports --no-strict-optional; then
        print_success "MyPy type checking passed"
    else
        print_error "MyPy type checking failed. Please fix the type issues above."
        exit 1
    fi
}

# Security scanning
run_security_checks() {
    print_status "Running security checks..."
    
    # Bandit security scanning
    print_status "Running Bandit security scanning..."
    if [ -f ".bandit" ]; then
        if bandit -c .bandit -r tcgplayer_client/ -f txt; then
            print_success "Bandit security scanning passed"
        else
            print_error "Bandit security scanning failed. Please fix the security issues above."
            exit 1
        fi
    else
        print_warning ".bandit configuration not found, skipping Bandit check"
    fi
    
    # Safety dependency vulnerability checker
    print_status "Running Safety dependency vulnerability checker..."
    if command_exists safety; then
        if safety check; then
            print_success "Safety dependency vulnerability checker passed"
        else
            print_warning "Safety found some dependency vulnerabilities. Consider updating packages."
        fi
    else
        print_warning "Safety not installed, skipping dependency vulnerability check"
    fi
    
    # Semgrep static analysis
    print_status "Running Semgrep static analysis..."
    if command_exists semgrep; then
        if python -m semgrep --config=auto tcgplayer_client/; then
            print_success "Semgrep static analysis passed"
        else
            print_warning "Semgrep found some issues. Please review the output above."
        fi
    else
        print_warning "Semgrep not installed, skipping static analysis"
    fi
    
    # pip-audit dependency security
    print_status "Running pip-audit for dependency security..."
    if command_exists pip-audit; then
        if pip-audit; then
            print_success "pip-audit dependency security check passed"
        else
            print_warning "pip-audit found some dependency security issues. Consider updating packages."
        fi
    else
        print_warning "pip-audit not installed, skipping dependency security check"
    fi
}

# Testing
run_tests() {
    print_status "Running tests..."
    
    # Run pytest
    print_status "Running pytest test suite..."
    if python -m pytest tests/ -v --tb=short; then
        print_success "All tests passed"
    else
        print_error "Some tests failed. Please fix the test issues above."
        exit 1
    fi
}

# Build check
run_build_check() {
    print_status "Running build check..."
    
    # Check if package can be built
    print_status "Checking if package can be built..."
    if python -m build --dry-run; then
        print_success "Package build check passed"
    else
        print_error "Package build check failed. Please fix the build issues above."
        exit 1
    fi
}

# Main execution
main() {
    echo "🚀 TCGplayer Client - Local CI Pipeline"
    echo "========================================"
    echo ""
    
    # Check Python version
    check_python_version
    
    # Install dependencies
    install_dependencies
    
    echo ""
    echo "🔍 Running all CI checks..."
    echo ""
    
    # Run all checks
    run_formatting_checks
    run_linting_checks
    run_type_checks
    run_security_checks
    run_tests
    run_build_check
    
    echo ""
    echo "🎉 All CI checks passed! 🎉"
    echo "Your code is ready to commit and push to GitHub."
    echo ""
    echo "Next steps:"
    echo "  git add ."
    echo "  git commit -m 'Your commit message'"
    echo "  git push origin main"
}

# Run main function
main "$@"

"""
Unit tests for the custom exception classes.
"""

import pytest

from tcgplayer_client.exceptions import (
    APIError,
    AuthenticationError,
    ConfigurationError,
    NetworkError,
    RateLimitError,
    TCGPlayerError,
    ValidationError,
)


class TestTCGPlayerError:
    """Test cases for the base TCGPlayerError class."""

    def test_base_exception_inheritance(self):
        """Test that TCGPlayerError inherits from Exception."""
        error = TCGPlayerError("Test error")
        assert isinstance(error, Exception)

    def test_error_message(self):
        """Test that error message is set correctly."""
        message = "Test error message"
        error = TCGPlayerError(message)
        assert str(error) == message

    def test_error_repr(self):
        """Test error string representation."""
        message = "Test error"
        error = TCGPlayerError(message)
        repr_str = repr(error)

        assert "TCGPlayerError" in repr_str
        assert message in repr_str


class TestAuthenticationError:
    """Test cases for AuthenticationError class."""

    def test_inheritance(self):
        """Test that AuthenticationError inherits from TCGPlayerError."""
        error = AuthenticationError("Auth failed")
        assert isinstance(error, TCGPlayerError)

    def test_error_message(self):
        """Test that authentication error message is set correctly."""
        message = "Invalid credentials"
        error = AuthenticationError(message)
        assert str(error) == message

    def test_error_type(self):
        """Test that AuthenticationError is the correct type."""
        error = AuthenticationError("Auth error")
        assert isinstance(error, AuthenticationError)


class TestRateLimitError:
    """Test cases for RateLimitError class."""

    def test_inheritance(self):
        """Test that RateLimitError inherits from TCGPlayerError."""
        error = RateLimitError("Rate limit exceeded")
        assert isinstance(error, TCGPlayerError)

    def test_error_message(self):
        """Test that rate limit error message is set correctly."""
        message = "Too many requests"
        error = RateLimitError(message)
        assert str(error) == message

    def test_error_type(self):
        """Test that RateLimitError is the correct type."""
        error = RateLimitError("Rate limit error")
        assert isinstance(error, RateLimitError)


class TestAPIError:
    """Test cases for APIError class."""

    def test_inheritance(self):
        """Test that APIError inherits from TCGPlayerError."""
        error = APIError("API request failed")
        assert isinstance(error, TCGPlayerError)

    def test_error_message(self):
        """Test that API error message is set correctly."""
        message = "Bad request"
        error = APIError(message)
        assert str(error) == message

    def test_error_type(self):
        """Test that APIError is the correct type."""
        error = APIError("API error")
        assert isinstance(error, APIError)

    def test_api_error_with_status_code(self):
        """Test API error with status code context."""
        message = "Not found"
        status_code = 404
        error = APIError(f"{message} with status {status_code}")

        assert str(error) == f"{message} with status {status_code}"


class TestNetworkError:
    """Test cases for NetworkError class."""

    def test_inheritance(self):
        """Test that NetworkError inherits from TCGPlayerError."""
        error = NetworkError("Network connection failed")
        assert isinstance(error, TCGPlayerError)

    def test_error_message(self):
        """Test that network error message is set correctly."""
        message = "Connection timeout"
        error = NetworkError(message)
        assert str(error) == message

    def test_error_type(self):
        """Test that NetworkError is the correct type."""
        error = NetworkError("Network error")
        assert isinstance(error, NetworkError)


class TestValidationError:
    """Test cases for ValidationError class."""

    def test_inheritance(self):
        """Test that ValidationError inherits from TCGPlayerError."""
        error = ValidationError("Invalid input")
        assert isinstance(error, TCGPlayerError)

    def test_error_message(self):
        """Test that validation error message is set correctly."""
        message = "Invalid category ID"
        error = ValidationError(message)
        assert str(error) == message

    def test_error_type(self):
        """Test that ValidationError is the correct type."""
        error = ValidationError("Validation error")
        assert isinstance(error, ValidationError)


class TestConfigurationError:
    """Test cases for ConfigurationError class."""

    def test_inheritance(self):
        """Test that ConfigurationError inherits from TCGPlayerError."""
        error = ConfigurationError("Missing configuration")
        assert isinstance(error, TCGPlayerError)

    def test_error_message(self):
        """Test that configuration error message is set correctly."""
        message = "Missing API key"
        error = ConfigurationError(message)
        assert str(error) == message

    def test_error_type(self):
        """Test that ConfigurationError is the correct type."""
        error = ConfigurationError("Configuration error")
        assert isinstance(error, ConfigurationError)


class TestExceptionHierarchy:
    """Test cases for exception hierarchy and relationships."""

    def test_exception_hierarchy(self):
        """Test that all exceptions inherit from the base class."""
        exceptions = [
            AuthenticationError("test"),
            RateLimitError("test"),
            APIError("test"),
            NetworkError("test"),
            ValidationError("test"),
            ConfigurationError("test"),
        ]

        for exc in exceptions:
            assert isinstance(exc, TCGPlayerError)

    def test_exception_uniqueness(self):
        """Test that different exception types are not equal."""
        auth_error = AuthenticationError("auth failed")
        api_error = APIError("api failed")

        assert auth_error != api_error
        assert not isinstance(auth_error, APIError)
        assert not isinstance(api_error, AuthenticationError)


class TestExceptionContext:
    """Test cases for exception context and usage."""

    def test_exception_in_try_except(self):
        """Test that exceptions can be caught in try-except blocks."""
        try:
            raise AuthenticationError("Test auth error")
        except AuthenticationError as e:
            assert str(e) == "Test auth error"
        except Exception:
            pytest.fail("Should have caught AuthenticationError")

    def test_exception_chaining(self):
        """Test that exceptions can be chained."""
        try:
            try:
                raise ValueError("Original error")
            except ValueError as e:
                raise AuthenticationError("Auth failed") from e
        except AuthenticationError as e:
            assert e.__cause__ is not None
            assert isinstance(e.__cause__, ValueError)

    def test_exception_with_custom_attributes(self):
        """Test that exceptions can have custom attributes."""
        error = APIError("API failed")
        error.status_code = 500
        error.endpoint = "/test"

        assert error.status_code == 500
        assert error.endpoint == "/test"

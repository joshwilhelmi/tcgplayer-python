"""
Custom exceptions for the TCGPlayer client library.
"""

from typing import Any, Optional


class TCGPlayerError(Exception):
    """Base exception for all TCGPlayer client errors."""

    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        response_data: Optional[Any] = None,
    ):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.response_data = response_data


class AuthenticationError(TCGPlayerError):
    """Raised when authentication fails."""

    pass


class RateLimitError(TCGPlayerError):
    """Raised when rate limit is exceeded."""

    def __init__(self, message: str, retry_after: Optional[int] = None):
        super().__init__(message)
        self.retry_after = retry_after


class APIError(TCGPlayerError):
    """Raised when the TCGPlayer API returns an error."""

    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        response_data: Optional[Any] = None,
    ):
        super().__init__(message, status_code, response_data)
        self.error_type = self._determine_error_type(status_code)

    def _determine_error_type(self, status_code: Optional[int]) -> str:
        """Determine the type of error based on status code."""
        if status_code is None:
            return "unknown"

        if 400 <= status_code < 500:
            return "client_error"
        elif 500 <= status_code < 600:
            return "server_error"
        else:
            return "other"

    @property
    def is_client_error(self) -> bool:
        """Check if this is a client-side error (4xx)."""
        return self.status_code is not None and 400 <= self.status_code < 500

    @property
    def is_server_error(self) -> bool:
        """Check if this is a server-side error (5xx)."""
        return self.status_code is not None and 500 <= self.status_code < 600


class NetworkError(TCGPlayerError):
    """Raised when network-related errors occur."""

    pass


class ValidationError(TCGPlayerError):
    """Raised when input validation fails."""

    pass


class ConfigurationError(TCGPlayerError):
    """Raised when there's a configuration issue."""

    pass


class TimeoutError(TCGPlayerError):
    """Raised when a request times out."""

    def __init__(self, message: str, timeout_seconds: Optional[float] = None):
        super().__init__(message)
        self.timeout_seconds = timeout_seconds


class RetryExhaustedError(TCGPlayerError):
    """Raised when all retry attempts are exhausted."""

    def __init__(
        self, message: str, attempts_made: int, last_error: Optional[Exception] = None
    ):
        super().__init__(message)
        self.attempts_made = attempts_made
        self.last_error = last_error


class InvalidResponseError(TCGPlayerError):
    """Raised when the API response is invalid or malformed."""

    def __init__(self, message: str, response_data: Optional[Any] = None):
        super().__init__(message, response_data=response_data)

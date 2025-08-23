"""
Configuration management for TCGPlayer Client.

This module provides flexible configuration management with support for
environment variables, configuration files, and runtime configuration.
"""

import json
import logging
import os
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Dict, Optional, Union

from .exceptions import ConfigurationError

logger = logging.getLogger(__name__)


@dataclass
class ClientConfig:
    """Configuration for TCGPlayer Client."""

    # API Configuration
    base_url: str = "https://api.tcgplayer.com"
    api_version: str = "v1.39.0"

    # Authentication
    client_id: Optional[str] = None
    client_secret: Optional[str] = None

    # Rate Limiting
    max_requests_per_second: int = 10
    rate_limit_window: float = 1.0

    # Request Configuration
    max_retries: int = 3
    base_delay: float = 1.0
    timeout_total: float = 30.0
    timeout_connect: float = 10.0
    timeout_read: float = 30.0

    # Session Configuration
    max_connections: int = 100
    max_connections_per_host: int = 10
    keepalive_timeout: int = 30

    # Logging Configuration
    log_level: str = "INFO"
    log_file: Optional[str] = None
    log_json_format: bool = False

    # Caching Configuration
    enable_caching: bool = True
    cache_ttl: int = 300  # 5 minutes
    cache_max_size: int = 1000

    # Development/Testing
    debug_mode: bool = False
    mock_responses: bool = False

    def __post_init__(self):
        """Validate configuration after initialization."""
        self._validate_config()

    def _validate_config(self):
        """Validate configuration values."""
        if self.max_requests_per_second <= 0:
            raise ConfigurationError("max_requests_per_second must be positive")

        # Enforce TCGPlayer's absolute maximum rate limit
        if self.max_requests_per_second > 10:
            logger.warning(
                f"Configuration rate limit "
                f"{self.max_requests_per_second} req/s exceeds "
                f"TCGPlayer's maximum of 10 req/s. "
                f"Rate limit has been capped to 10 req/s to prevent API "
                f"violations."
            )
            self.max_requests_per_second = 10

        if self.rate_limit_window <= 0:
            raise ConfigurationError("rate_limit_window must be positive")

        if self.max_retries < 0:
            raise ConfigurationError("max_retries must be non-negative")

        if self.base_delay <= 0:
            raise ConfigurationError("base_delay must be positive")

        if self.timeout_total <= 0:
            raise ConfigurationError("timeout_total must be positive")

        if self.max_connections <= 0:
            raise ConfigurationError("max_connections must be positive")

        if self.cache_ttl <= 0:
            raise ConfigurationError("cache_ttl must be positive")

    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary."""
        return asdict(self)

    def update(self, **kwargs):
        """Update configuration with new values."""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                raise ConfigurationError(f"Unknown configuration key: {key}")

        # Re-validate after update
        self._validate_config()


class ConfigurationManager:
    """Manages configuration loading and validation."""

    DEFAULT_CONFIG_FILE = "tcgplayer_config.json"
    ENV_PREFIX = "TCGPLAYER_"

    def __init__(self, config_file: Optional[Union[str, Path]] = None):
        """
        Initialize configuration manager.

        Args:
            config_file: Path to configuration file
        """
        self.config_file = (
            Path(config_file) if config_file else Path(self.DEFAULT_CONFIG_FILE)
        )
        self.config = ClientConfig()

    def load_from_env(self) -> ClientConfig:
        """Load configuration from environment variables."""
        env_config: Dict[str, Any] = {}

        # Map environment variables to configuration keys
        env_mapping = {
            "TCGPLAYER_BASE_URL": "base_url",
            "TCGPLAYER_API_VERSION": "api_version",
            "TCGPLAYER_CLIENT_ID": "client_id",
            "TCGPLAYER_CLIENT_SECRET": "client_secret",
            "TCGPLAYER_MAX_REQUESTS_PER_SECOND": "max_requests_per_second",
            "TCGPLAYER_RATE_LIMIT_WINDOW": "rate_limit_window",
            "TCGPLAYER_MAX_RETRIES": "max_retries",
            "TCGPLAYER_BASE_DELAY": "base_delay",
            "TCGPLAYER_TIMEOUT_TOTAL": "timeout_total",
            "TCGPLAYER_TIMEOUT_CONNECT": "timeout_connect",
            "TCGPLAYER_TIMEOUT_READ": "timeout_read",
            "TCGPLAYER_MAX_CONNECTIONS": "max_connections",
            "TCGPLAYER_MAX_CONNECTIONS_PER_HOST": "max_connections_per_host",
            "TCGPLAYER_KEEPALIVE_TIMEOUT": "keepalive_timeout",
            "TCGPLAYER_LOG_LEVEL": "log_level",
            "TCGPLAYER_LOG_FILE": "log_file",
            "TCGPLAYER_LOG_JSON_FORMAT": "log_json_format",
            "TCGPLAYER_ENABLE_CACHING": "enable_caching",
            "TCGPLAYER_CACHE_TTL": "cache_ttl",
            "TCGPLAYER_CACHE_MAX_SIZE": "cache_max_size",
            "TCGPLAYER_DEBUG_MODE": "debug_mode",
            "TCGPLAYER_MOCK_RESPONSES": "mock_responses",
        }

        for env_var, config_key in env_mapping.items():
            value = os.getenv(env_var)
            if value is not None:
                # Convert string values to appropriate types
                if config_key in [
                    "max_requests_per_second",
                    "max_retries",
                    "max_connections",
                    "max_connections_per_host",
                    "keepalive_timeout",
                    "cache_ttl",
                    "cache_max_size",
                ]:
                    env_config[config_key] = int(value)
                elif config_key in [
                    "rate_limit_window",
                    "base_delay",
                    "timeout_total",
                    "timeout_connect",
                    "timeout_read",
                ]:
                    env_config[config_key] = float(value)
                elif config_key in [
                    "log_json_format",
                    "enable_caching",
                    "debug_mode",
                    "mock_responses",
                ]:
                    env_config[config_key] = value.lower() in ("true", "1", "yes", "on")
                elif config_key in [
                    "log_level",
                    "base_url",
                    "api_version",
                    "client_id",
                    "client_secret",
                    "log_file",
                ]:
                    env_config[config_key] = str(value)
                else:
                    env_config[config_key] = value

        # Update configuration with environment values
        self.config.update(**env_config)
        return self.config

    def load_from_file(
        self, config_file: Optional[Union[str, Path]] = None
    ) -> ClientConfig:
        """Load configuration from JSON file."""
        file_path = Path(config_file) if config_file else self.config_file

        if not file_path.exists():
            return self.config

        try:
            with open(file_path, "r") as f:
                file_config = json.load(f)

            # Update configuration with file values
            self.config.update(**file_config)
            return self.config

        except (json.JSONDecodeError, IOError) as e:
            raise ConfigurationError(
                f"Failed to load configuration file {file_path}: {e}"
            )

    def save_to_file(self, config_file: Optional[Union[str, Path]] = None) -> None:
        """Save current configuration to JSON file."""
        file_path = Path(config_file) if config_file else self.config_file

        try:
            # Create directory if it doesn't exist
            file_path.parent.mkdir(parents=True, exist_ok=True)

            with open(file_path, "w") as f:
                json.dump(self.config.to_dict(), f, indent=2)

        except IOError as e:
            raise ConfigurationError(
                f"Failed to save configuration file {file_path}: {e}"
            )

    def create_default_config(
        self, config_file: Optional[Union[str, Path]] = None
    ) -> None:
        """Create a default configuration file."""
        default_config = ClientConfig()
        self.config = default_config
        self.save_to_file(config_file)

    def get_config(self) -> ClientConfig:
        """Get the current configuration."""
        return self.config

    def update_config(self, **kwargs) -> None:
        """Update configuration with new values."""
        self.config.update(**kwargs)

    def reset_to_defaults(self) -> None:
        """Reset configuration to default values."""
        self.config = ClientConfig()

    def validate_config(self) -> bool:
        """Validate the current configuration."""
        try:
            self.config._validate_config()
            return True
        except ConfigurationError:
            return False


def load_config(
    config_file: Optional[Union[str, Path]] = None, env_override: bool = True
) -> ClientConfig:
    """
    Load configuration from file and environment.

    Args:
        config_file: Path to configuration file
        env_override: Whether environment variables override file values

    Returns:
        Loaded configuration
    """
    config_manager = ConfigurationManager(config_file)

    # Load from file first
    config_manager.load_from_file()

    # Then load from environment (overriding file values)
    if env_override:
        config_manager.load_from_env()

    return config_manager.get_config()


def create_default_config(config_file: Optional[Union[str, Path]] = None) -> None:
    """Create a default configuration file."""
    config_manager = ConfigurationManager(config_file)
    config_manager.create_default_config()


# Environment variable helpers
def get_env_bool(key: str, default: bool = False) -> bool:
    """Get boolean value from environment variable."""
    value = os.getenv(key, "").lower()
    return value in ("true", "1", "yes", "on") if value else default


def get_env_int(key: str, default: int = 0) -> int:
    """Get integer value from environment variable."""
    try:
        return int(os.getenv(key, default))
    except (ValueError, TypeError):
        return default


def get_env_float(key: str, default: float = 0.0) -> float:
    """Get float value from environment variable."""
    try:
        return float(os.getenv(key, default))
    except (ValueError, TypeError):
        return default

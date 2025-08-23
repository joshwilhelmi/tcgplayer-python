"""
Enhanced logging configuration for TCGPlayer Client.

This module provides structured logging with configurable log levels,
formatters, and handlers for better debugging and monitoring.
"""

import json
import logging
import logging.handlers
import os
import sys
from pathlib import Path
from typing import Dict, Optional, Union

# Default logging configuration
DEFAULT_LOG_LEVEL = "INFO"
DEFAULT_LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
DEFAULT_JSON_FORMAT = {
    "timestamp": "%(asctime)s",
    "level": "%(levelname)s",
    "logger": "%(name)s",
    "message": "%(message)s",
    "module": "%(module)s",
    "function": "%(funcName)s",
    "line": "%(lineno)d",
}


class StructuredFormatter(logging.Formatter):
    """Custom formatter that supports both text and JSON output."""

    def __init__(
        self,
        fmt: Optional[str] = None,
        datefmt: Optional[str] = None,
        json_format: bool = False,
        json_fields: Optional[Dict[str, str]] = None,
    ):
        """
        Initialize the formatter.

        Args:
            fmt: Format string for text output
            datefmt: Date format string
            json_format: Whether to output JSON format
            json_fields: Custom JSON field mappings
        """
        super().__init__(fmt, datefmt)
        self.json_format = json_format
        self.json_fields = json_fields or DEFAULT_JSON_FORMAT

    def format(self, record: logging.LogRecord) -> str:
        """Format the log record."""
        if self.json_format:
            return self._format_json(record)
        return super().format(record)

    def _format_json(self, record: logging.LogRecord) -> str:
        """Format the log record as JSON."""
        log_data = {}

        for field, fmt in self.json_fields.items():
            try:
                if fmt.startswith("%(") and fmt.endswith(")s"):
                    # Extract field name from format string
                    field_name = fmt[2:-2]
                    if hasattr(record, field_name):
                        log_data[field] = getattr(record, field_name)
                    else:
                        log_data[field] = fmt
                else:
                    log_data[field] = fmt
            except Exception:
                log_data[field] = fmt

        # Add extra fields if present
        if hasattr(record, "extra_fields"):
            log_data.update(record.extra_fields)

        # Add exception info if present
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_data, default=str)


class TCGPlayerLogger:
    """Enhanced logger for TCGPlayer Client with structured logging support."""

    def __init__(
        self, name: str = "tcgplayer_client", level: Optional[Union[str, int]] = None
    ):
        """
        Initialize the logger.

        Args:
            name: Logger name
            level: Log level (string or int)
        """
        self.name = name
        self.logger = logging.getLogger(name)

        # Set log level
        if level is not None:
            if isinstance(level, str):
                level = getattr(logging, level.upper())
            self.logger.setLevel(level)

        # Configure handlers if none exist
        if not self.logger.handlers:
            self._setup_handlers()

    def _setup_handlers(self):
        """Set up default handlers."""
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)

        # File handler (rotating)
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        file_handler = logging.handlers.RotatingFileHandler(
            log_dir / "tcgplayer_client.log",
            maxBytes=10 * 1024 * 1024,  # 10MB
            backupCount=5,
        )
        file_handler.setLevel(logging.DEBUG)

        # Set formatters
        console_formatter = StructuredFormatter(DEFAULT_LOG_FORMAT)
        file_formatter = StructuredFormatter(
            json_format=True, json_fields=DEFAULT_JSON_FORMAT
        )

        console_handler.setFormatter(console_formatter)
        file_handler.setFormatter(file_formatter)

        # Add handlers
        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)

    def set_level(self, level: Union[str, int]):
        """Set the log level."""
        if isinstance(level, str):
            level = getattr(logging, level.upper())
        self.logger.setLevel(level)

    def add_file_handler(
        self,
        filepath: Union[str, Path],
        level: Union[str, int] = logging.DEBUG,
        json_format: bool = False,
    ):
        """Add a custom file handler."""
        if isinstance(level, str):
            level = getattr(logging, level.upper())

        handler = logging.FileHandler(filepath)
        handler.setLevel(level)

        if json_format:
            formatter = StructuredFormatter(json_format=True)
        else:
            formatter = StructuredFormatter(DEFAULT_LOG_FORMAT)

        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def add_rotating_file_handler(
        self,
        filepath: Union[str, Path],
        max_bytes: int = 10 * 1024 * 1024,
        backup_count: int = 5,
        level: Union[str, int] = logging.DEBUG,
        json_format: bool = False,
    ):
        """Add a rotating file handler."""
        if isinstance(level, str):
            level = getattr(logging, level.upper())

        handler = logging.handlers.RotatingFileHandler(
            filepath, maxBytes=max_bytes, backupCount=backup_count
        )
        handler.setLevel(level)

        if json_format:
            formatter = StructuredFormatter(json_format=True)
        else:
            formatter = StructuredFormatter(DEFAULT_LOG_FORMAT)

        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def log_with_context(self, level: int, message: str, **extra_fields):
        """Log a message with extra context fields."""
        record = self.logger.makeRecord(self.name, level, "", 0, message, (), None)
        record.extra_fields = extra_fields
        self.logger.handle(record)

    def debug(self, message: str, **extra_fields):
        """Log a debug message with optional extra fields."""
        if extra_fields:
            self.log_with_context(logging.DEBUG, message, **extra_fields)
        else:
            self.logger.debug(message)

    def info(self, message: str, **extra_fields):
        """Log an info message with optional extra fields."""
        if extra_fields:
            self.log_with_context(logging.INFO, message, **extra_fields)
        else:
            self.logger.info(message)

    def warning(self, message: str, **extra_fields):
        """Log a warning message with optional extra fields."""
        if extra_fields:
            self.log_with_context(logging.WARNING, message, **extra_fields)
        else:
            self.logger.warning(message)

    def error(self, message: str, **extra_fields):
        """Log an error message with optional extra fields."""
        if extra_fields:
            self.log_with_context(logging.ERROR, message, **extra_fields)
        else:
            self.logger.error(message)

    def critical(self, message: str, **extra_fields):
        """Log a critical message with optional extra fields."""
        if extra_fields:
            self.log_with_context(logging.CRITICAL, message, **extra_fields)
        else:
            self.logger.critical(message)

    def exception(self, message: str, **extra_fields):
        """Log an exception message with traceback."""
        if extra_fields:
            self.log_with_context(logging.ERROR, message, **extra_fields)
        else:
            self.logger.exception(message)


def setup_logging(
    name: str = "tcgplayer_client",
    level: Optional[Union[str, int]] = None,
    log_file: Optional[Union[str, Path]] = None,
    json_format: bool = False,
) -> TCGPlayerLogger:
    """
    Set up logging for TCGPlayer Client.

    Args:
        name: Logger name
        level: Log level (string or int)
        log_file: Optional log file path
        json_format: Whether to use JSON format for file logging

    Returns:
        Configured logger instance
    """
    # Get log level from environment if not specified
    if level is None:
        level = os.getenv("TCGPLAYER_LOG_LEVEL", DEFAULT_LOG_LEVEL)

    logger = TCGPlayerLogger(name, level)

    # Add file handler if specified
    if log_file:
        logger.add_file_handler(log_file, json_format=json_format)

    return logger


def get_logger(name: str = "tcgplayer_client") -> logging.Logger:
    """
    Get a standard Python logger for the given name.

    Args:
        name: Logger name

    Returns:
        Python logger instance
    """
    return logging.getLogger(name)

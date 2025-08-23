"""
Input validation for TCGPlayer API parameters.

This module provides validation functions for API parameters including
bounds checking, type validation, and format validation.
"""

import logging
import re
from typing import Any, Dict, List, Optional, Union

from .exceptions import ValidationError

logger = logging.getLogger(__name__)


class ParameterValidator:
    """Validates API parameters before making requests."""

    # Common validation patterns
    GTIN_PATTERN = re.compile(r"^\d{13}$")  # 13-digit GTIN
    EMAIL_PATTERN = re.compile(r"^[^@]+@[^@]+\.[^@]+$")

    @staticmethod
    def validate_integer_range(
        value: Any,
        param_name: str,
        min_value: Optional[int] = None,
        max_value: Optional[int] = None,
    ) -> int:
        """
        Validate and convert a value to an integer within a specified range.

        Args:
            value: Value to validate
            param_name: Name of the parameter for error messages
            min_value: Minimum allowed value (inclusive)
            max_value: Maximum allowed value (inclusive)

        Returns:
            Validated integer value

        Raises:
            ValidationError: If validation fails
        """
        try:
            int_value = int(value)
        except (ValueError, TypeError):
            raise ValidationError(
                f"{param_name} must be an integer, got {type(value).__name__}"
            )

        if min_value is not None and int_value < min_value:
            raise ValidationError(
                f"{param_name} must be >= {min_value}, got {int_value}"
            )

        if max_value is not None and int_value > max_value:
            raise ValidationError(
                f"{param_name} must be <= {max_value}, got {int_value}"
            )

        return int_value

    @staticmethod
    def validate_float_range(
        value: Any,
        param_name: str,
        min_value: Optional[float] = None,
        max_value: Optional[float] = None,
    ) -> float:
        """
        Validate and convert a value to a float within a specified range.

        Args:
            value: Value to validate
            param_name: Name of the parameter for error messages
            min_value: Minimum allowed value (inclusive)
            max_value: Maximum allowed value (inclusive)

        Returns:
            Validated float value

        Raises:
            ValidationError: If validation fails
        """
        try:
            float_value = float(value)
        except (ValueError, TypeError):
            raise ValidationError(
                f"{param_name} must be a number, got {type(value).__name__}"
            )

        if min_value is not None and float_value < min_value:
            raise ValidationError(
                f"{param_name} must be >= {min_value}, got {float_value}"
            )

        if max_value is not None and float_value > max_value:
            raise ValidationError(
                f"{param_name} must be <= {max_value}, got {float_value}"
            )

        return float_value

    @staticmethod
    def validate_string(
        value: Any,
        param_name: str,
        min_length: Optional[int] = None,
        max_length: Optional[int] = None,
        pattern: Optional[re.Pattern] = None,
    ) -> str:
        """
        Validate a string value.

        Args:
            value: Value to validate
            param_name: Name of the parameter for error messages
            min_length: Minimum string length
            max_length: Maximum string length
            pattern: Regex pattern to match against

        Returns:
            Validated string value

        Raises:
            ValidationError: If validation fails
        """
        if not isinstance(value, str):
            raise ValidationError(
                f"{param_name} must be a string, got {type(value).__name__}"
            )

        if min_length is not None and len(value) < min_length:
            raise ValidationError(
                f"{param_name} must be at least {min_length} characters long"
            )

        if max_length is not None and len(value) > max_length:
            raise ValidationError(
                f"{param_name} must be at most {max_length} characters long"
            )

        if pattern is not None and not pattern.match(value):
            raise ValidationError(f"{param_name} does not match required format")

        return value

    @staticmethod
    def validate_list(
        value: Any,
        param_name: str,
        min_items: Optional[int] = None,
        max_items: Optional[int] = None,
        item_type: Optional[type] = None,
    ) -> List[Any]:
        """
        Validate a list value.

        Args:
            value: Value to validate
            param_name: Name of the parameter for error messages
            min_items: Minimum number of items
            max_items: Maximum number of items
            item_type: Expected type for list items

        Returns:
            Validated list value

        Raises:
            ValidationError: If validation fails
        """
        if not isinstance(value, list):
            raise ValidationError(
                f"{param_name} must be a list, got {type(value).__name__}"
            )

        if min_items is not None and len(value) < min_items:
            raise ValidationError(f"{param_name} must have at least {min_items} items")

        if max_items is not None and len(value) > max_items:
            raise ValidationError(f"{param_name} must have at most {max_items} items")

        if item_type is not None:
            for i, item in enumerate(value):
                if not isinstance(item, item_type):
                    raise ValidationError(
                        f"{param_name}[{i}] must be {item_type.__name__}, "
                        f"got {type(item).__name__}"
                    )

        return value

    @staticmethod
    def validate_gtin(gtin: str) -> str:
        """
        Validate GTIN (Global Trade Item Number) format.

        Args:
            gtin: GTIN string to validate

        Returns:
            Validated GTIN string

        Raises:
            ValidationError: If GTIN format is invalid
        """
        return ParameterValidator.validate_string(
            gtin, "GTIN", pattern=ParameterValidator.GTIN_PATTERN
        )

    @staticmethod
    def validate_email(email: str) -> str:
        """
        Validate email format.

        Args:
            email: Email string to validate

        Returns:
            Validated email string

        Raises:
            ValidationError: If email format is invalid
        """
        return ParameterValidator.validate_string(
            email, "email", pattern=ParameterValidator.EMAIL_PATTERN
        )

    @staticmethod
    def validate_pagination_params(
        limit: Optional[int] = None, offset: Optional[int] = None
    ) -> Dict[str, int]:
        """
        Validate pagination parameters.

        Args:
            limit: Maximum number of items to return
            offset: Number of items to skip

        Returns:
            Dictionary with validated limit and offset

        Raises:
            ValidationError: If validation fails
        """
        validated = {}

        if limit is not None:
            validated["limit"] = ParameterValidator.validate_integer_range(
                limit, "limit", min_value=1, max_value=1000
            )

        if offset is not None:
            validated["offset"] = ParameterValidator.validate_integer_range(
                offset, "offset", min_value=0
            )

        return validated

    @staticmethod
    def validate_price(price: Union[int, float], param_name: str = "price") -> float:
        """
        Validate price values.

        Args:
            price: Price value to validate
            param_name: Name of the parameter for error messages

        Returns:
            Validated price value

        Raises:
            ValidationError: If validation fails
        """
        return ParameterValidator.validate_float_range(price, param_name, min_value=0.0)

    @staticmethod
    def validate_quantity(
        quantity: Union[int, float], param_name: str = "quantity"
    ) -> float:
        """
        Validate quantity values.

        Args:
            quantity: Quantity value to validate
            param_name: Name of the parameter for error messages

        Returns:
            Validated quantity value

        Raises:
            ValidationError: If validation fails
        """
        return ParameterValidator.validate_float_range(
            quantity, param_name, min_value=0.0
        )


# Convenience functions for common validations
def validate_id(id_value: Any, param_name: str = "ID") -> int:
    """Validate an ID parameter (positive integer)."""
    return ParameterValidator.validate_integer_range(id_value, param_name, min_value=1)


def validate_positive_integer(value: Any, param_name: str) -> int:
    """Validate a positive integer parameter."""
    return ParameterValidator.validate_integer_range(value, param_name, min_value=1)


def validate_non_negative_integer(value: Any, param_name: str) -> int:
    """Validate a non-negative integer parameter."""
    return ParameterValidator.validate_integer_range(value, param_name, min_value=0)


def validate_positive_float(value: Any, param_name: str) -> float:
    """Validate a positive float parameter."""
    return ParameterValidator.validate_float_range(value, param_name, min_value=0.0)

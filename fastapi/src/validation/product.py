"""Product validation functions."""

from typing import Any
from fastapi import HTTPException, status


def validate_product_id(product_id: Any) -> int | str:
    """Validate product ID with LLM-friendly error messages."""
    if product_id is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Product ID is required. Please provide a valid product ID as an integer (e.g., 1, 2, 3) or string (e.g., '1', '2', '3')."
        )

    if not isinstance(product_id, (int, str)):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Product ID must be an integer or string. Please provide a valid product ID like 1 or '1'."
        )

    return product_id
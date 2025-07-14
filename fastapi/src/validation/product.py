"""Product validation functions."""

from typing import Any
from fastapi import HTTPException, status


def validate_product_id(product_id: Any) -> int | str:
    """Validate product ID with detailed error messages."""
    if product_id is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="productId is required and cannot be null"
        )

    if not isinstance(product_id, (int, str)):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"productId must be an integer or string, got {type(product_id).__name__}"
        )

    return product_id
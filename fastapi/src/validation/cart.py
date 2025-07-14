"""Cart validation functions."""

from typing import Any, List, Dict
from fastapi import HTTPException, status


def validate_user_id(user_id: Any) -> int:
    """Validate user ID with detailed error messages."""
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="userId is required and cannot be null"
        )

    if not isinstance(user_id, (int, str)):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"userId must be an integer or string, got {type(user_id).__name__}"
        )

    try:
        return int(user_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"userId must be a valid integer, got '{user_id}'"
        )


def validate_cart_id(cart_id: Any) -> int | str:
    """Validate cart ID with detailed error messages."""
    if cart_id is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="cartId is required and cannot be null"
        )

    if not isinstance(cart_id, (int, str)):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"cartId must be an integer or string, got {type(cart_id).__name__}"
        )

    return cart_id


def validate_products(products: Any) -> List[Dict[str, Any]]:
    """Validate products list with detailed error messages."""
    if not isinstance(products, list):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"products must be a list, got {type(products).__name__}"
        )

    validated_products = []
    for i, product in enumerate(products):
        if not isinstance(product, dict):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Product at index {i} must be an object, got {type(product).__name__}"
            )

        if "id" not in product:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Product at index {i} must have an 'id' field"
            )

        product_id = product["id"]
        if not isinstance(product_id, (int, str)):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Product id at index {i} must be an integer or string, got {type(product_id).__name__}"
            )

        try:
            validated_id = int(product_id)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Product id at index {i} must be a valid integer, got '{product_id}'"
            )

        validated_product = {"id": validated_id}

        # Handle quantity if provided
        if "quantity" in product:
            quantity = product["quantity"]
            if not isinstance(quantity, (int, str)):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Product quantity at index {i} must be an integer or string, got {type(quantity).__name__}"
                )

            try:
                validated_quantity = int(quantity)
                if validated_quantity < 1:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Product quantity at index {i} must be at least 1, got {validated_quantity}"
                    )
                validated_product["quantity"] = validated_quantity
            except ValueError:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Product quantity at index {i} must be a valid integer, got '{quantity}'"
                )

        validated_products.append(validated_product)

    return validated_products
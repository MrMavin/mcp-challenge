"""Cart validation functions."""

from typing import Any, List, Dict
from fastapi import HTTPException, status


def validate_cart_id(cart_id: Any) -> int | str:
    """Validate cart ID with LLM-friendly error messages."""
    if cart_id is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cart ID is required. Please provide a valid cart ID as an integer (e.g., 1, 2, 3) or string (e.g., '1', '2', '3')."
        )

    if not isinstance(cart_id, (int, str)):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cart ID must be an integer or string. Please provide a valid cart ID like 1 or '1'."
        )

    return cart_id


def validate_products(products: Any) -> List[Dict[str, Any]]:
    """Validate products list with general, LLM-friendly error messages."""
    if not isinstance(products, list):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The 'products' field must be an array of product objects. Please provide products as: [{\"id\": 1, \"quantity\": 2}, {\"id\": 2, \"quantity\": 1}]"
        )

    validated_products = []
    has_format_errors = False
    has_id_errors = False
    has_quantity_errors = False

    for product in products:
        if not isinstance(product, dict):
            has_format_errors = True
            continue

        # Validate product ID
        if "id" not in product:
            has_id_errors = True
        else:
            product_id = product["id"]
            if not isinstance(product_id, (int, str)):
                has_id_errors = True
            else:
                try:
                    int(product_id)
                except ValueError:
                    has_id_errors = True

        # Validate quantity if provided
        if "quantity" in product:
            quantity = product["quantity"]
            if not isinstance(quantity, (int, str)):
                has_quantity_errors = True
            else:
                try:
                    validated_quantity = int(quantity)
                    if validated_quantity < 1:
                        has_quantity_errors = True
                except ValueError:
                    has_quantity_errors = True

        # If no errors for this product, add it to validated products
        if (isinstance(product, dict) and 
            "id" in product and 
            isinstance(product["id"], (int, str)) and
            str(product["id"]).isdigit() and
            ("quantity" not in product or 
             (isinstance(product["quantity"], (int, str)) and 
              str(product["quantity"]).isdigit() and 
              int(product["quantity"]) >= 1))):
            
            validated_product = {"id": int(product["id"])}
            if "quantity" in product:
                validated_product["quantity"] = int(product["quantity"])
            validated_products.append(validated_product)

    # Provide general guidance based on error types found
    error_messages = []
    
    if has_format_errors:
        error_messages.append("Some products are not properly formatted. Each product must be an object with an 'id' field.")
    
    if has_id_errors:
        error_messages.append("Some products have invalid IDs. Product IDs must be positive integers (e.g., 1, 2, 3).")
    
    if has_quantity_errors:
        error_messages.append("Some products have invalid quantities. Quantities must be positive integers (1 or greater).")

    if error_messages:
        guidance = " Please ensure all products follow this format: {\"id\": 1, \"quantity\": 2} where 'id' is a positive integer and 'quantity' is optional but must be 1 or greater if provided."
        error_detail = "There are issues with the products in your request. " + " ".join(error_messages) + guidance
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error_detail
        )

    return validated_products

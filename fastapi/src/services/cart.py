"""Service layer for cart operations.

Handles interaction with the fakestoreapi.com cart endpoints.
This service strictly follows the fakestoreapi.com API specification.
"""

import requests
from typing import Dict, Any, Union
from src.logger import get_logger

logger = get_logger(__name__)

# Base URL for the fake store API
BASE_URL = "https://fakestoreapi.com"


async def get_cart(cart_id: Union[int, str]) -> Dict[str, Any]:
    """Fetch a specific cart by ID.

    API Reference: GET /carts/{id}
    Path Parameter: id (integer) - Cart ID
    Returns: Cart object

    Cart Schema:
    {
        "id": integer,
        "userId": integer,
        "products": [Product...]
    }

    Args:
        cart_id: The ID of the cart to retrieve (must be integer)

    Returns:
        Dict[str, Any]: Cart object

    Raises:
        requests.HTTPError: If cart not found (404) or other HTTP errors
    """
    try:
        response = requests.get(f"{BASE_URL}/carts/{cart_id}")

        response.raise_for_status()

        return response.json()
    except requests.RequestException as e:
        logger.error(f"Error fetching cart {cart_id}: {e}")

        raise


async def create_cart(cart_data: Dict[str, Any]) -> Dict[str, Any]:
    """Create a new cart.

    API Reference: POST /carts
    Request Body: Cart object (JSON)
    Returns: Cart object with generated ID

    Expected Request Body Schema:
    {
        "userId": integer,
        "products": [Product...]
    }

    Note: The API spec shows products as Product objects, but the actual API
    expects simplified objects with just {id: number, quantity: number}.
    This function accepts the simplified format that the API actually uses.

    Args:
        cart_data: The cart data to create

    Returns:
        Dict[str, Any]: The created cart object

    Raises:
        requests.HTTPError: If cart creation fails
    """
    try:
        response = requests.post(
            f"{BASE_URL}/carts",
            json=cart_data,
            headers={"Content-Type": "application/json"}
        )

        response.raise_for_status()

        return response.json()
    except requests.RequestException as e:
        logger.error(f"Error creating cart: {e}")

        raise


async def update_cart(cart_id: Union[int, str], cart_data: Dict[str, Any]) -> Dict[str, Any]:
    """Update a specific cart.

    API Reference: PUT /carts/{id}
    Path Parameter: id (integer) - Cart ID
    Request Body: Cart object (JSON)
    Returns: Updated cart object

    Expected Request Body Schema:
    {
        "userId": integer,
        "products": [Product...]
    }

    Note: The API spec shows products as Product objects, but the actual API
    expects simplified objects with just {id: number, quantity: number}.
    This function accepts the simplified format that the API actually uses.

    Args:
        cart_id: The ID of the cart to update (must be integer)
        cart_data: The new cart data

    Returns:
        Dict[str, Any]: The updated cart object

    Raises:
        requests.HTTPError: If cart not found (404) or update fails
    """
    try:
        response = requests.put(
            f"{BASE_URL}/carts/{cart_id}",
            json=cart_data,
            headers={"Content-Type": "application/json"}
        )

        response.raise_for_status()

        return response.json()
    except requests.RequestException as e:
        logger.error(f"Error updating cart {cart_id}: {e}")

        raise

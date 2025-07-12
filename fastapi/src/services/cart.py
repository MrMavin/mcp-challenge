"""Service layer for cart operations.

Handles interaction with the fakestoreapi.com cart endpoints.
"""

import requests
from typing import Dict, List, Any, Optional
from src.logger import get_logger

logger = get_logger(__name__)

# Base URL for the fake store API
BASE_URL = "https://fakestoreapi.com"


async def get_all_carts() -> List[Dict[str, Any]]:
    """Fetch all carts from the API.

    Returns:
        List[Dict[str, Any]]: List of cart objects
    """
    try:
        response = requests.get(f"{BASE_URL}/carts")
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logger.error(f"Error fetching all carts: {e}")
        raise


async def get_cart(cart_id: int | str) -> Dict[str, Any]:
    """Fetch a specific cart by ID.

    Args:
        cart_id: The ID of the cart to retrieve

    Returns:
        Dict[str, Any]: Cart object
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

    Args:
        cart_data: The cart data to create

    Returns:
        Dict[str, Any]: The created cart object
    """
    try:
        response = requests.post(
            f"{BASE_URL}/carts",
            json=cart_data
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logger.error(f"Error creating cart: {e}")
        raise


async def update_cart(cart_id: int | str, cart_data: Dict[str, Any]) -> Dict[str, Any]:
    """Update a specific cart.

    Args:
        cart_id: The ID of the cart to update
        cart_data: The new cart data

    Returns:
        Dict[str, Any]: The updated cart object
    """
    try:
        response = requests.put(
            f"{BASE_URL}/carts/{cart_id}",
            json=cart_data
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logger.error(f"Error updating cart {cart_id}: {e}")
        raise


async def delete_cart(cart_id: int | str) -> Dict[str, Any]:
    """Delete a specific cart.

    Args:
        cart_id: The ID of the cart to delete

    Returns:
        Dict[str, Any]: Response data
    """
    try:
        response = requests.delete(f"{BASE_URL}/carts/{cart_id}")
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logger.error(f"Error deleting cart {cart_id}: {e}")
        raise

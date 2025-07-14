"""Service layer for cart operations.

Handles interaction with the fakestoreapi.com cart endpoints.
This service strictly follows the fakestoreapi.com API specification.
"""

import requests
from typing import Dict, List, Any, Optional, Union
from src.logger import get_logger

logger = get_logger(__name__)

# Base URL for the fake store API
BASE_URL = "https://fakestoreapi.com"


async def get_all_carts() -> List[Dict[str, Any]]:
    """Fetch all carts from the API.
    
    API Reference: GET /carts
    Returns: Array of Cart objects
    
    Cart Schema:
    {
        "id": integer,
        "userId": integer,
        "products": [Product...]
    }

    Returns:
        List[Dict[str, Any]]: List of cart objects
    """
    try:
        logger.info("Fetching all carts from fakestoreapi.com")
        response = requests.get(f"{BASE_URL}/carts")
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logger.error(f"Error fetching all carts: {e}")
        raise


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
        logger.info(f"Fetching cart {cart_id} from fakestoreapi.com")
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
        logger.info(f"Creating cart with data: {cart_data}")
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
        logger.info(f"Updating cart {cart_id} with data: {cart_data}")
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


async def delete_cart(cart_id: Union[int, str]) -> Dict[str, Any]:
    """Delete a specific cart.
    
    API Reference: DELETE /carts/{id}
    Path Parameter: id (integer) - Cart ID
    Returns: Success response
    
    Response: HTTP 200 with confirmation message

    Args:
        cart_id: The ID of the cart to delete (must be integer)

    Returns:
        Dict[str, Any]: Response data (typically confirms deletion)
        
    Raises:
        requests.HTTPError: If cart not found (404) or deletion fails
    """
    try:
        logger.info(f"Deleting cart {cart_id} from fakestoreapi.com")
        response = requests.delete(f"{BASE_URL}/carts/{cart_id}")
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logger.error(f"Error deleting cart {cart_id}: {e}")
        raise

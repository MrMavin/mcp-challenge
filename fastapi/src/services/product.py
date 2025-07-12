"""Service layer for product operations.

Handles interaction with the fakestoreapi.com product endpoints.
"""

import requests
from typing import Dict, List, Any, Optional, Union
from src.logger import get_logger

logger = get_logger(__name__)

# Base URL for the fake store API
BASE_URL = "https://fakestoreapi.com"


async def get_all_products() -> List[Dict[str, Any]]:
    """Fetch all products from the API.

    Returns:
        List[Dict[str, Any]]: List of product objects
    """
    try:
        logger.info("Fetching all products")
        response = requests.get(f"{BASE_URL}/products")
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logger.error(f"Error fetching all products: {e}")
        raise


async def get_product(product_id: Union[int, str]) -> Dict[str, Any]:
    """Fetch a specific product by ID.

    Args:
        product_id: The ID of the product to retrieve (can be integer or string)

    Returns:
        Dict[str, Any]: Product object
    """
    try:
        logger.info(f"Fetching product {product_id}")
        response = requests.get(f"{BASE_URL}/products/{product_id}")
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logger.error(f"Error fetching product {product_id}: {e}")
        raise

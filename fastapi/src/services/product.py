"""Service layer for product operations.

Handles interaction with the fakestoreapi.com product endpoints.
This service strictly follows the fakestoreapi.com API specification.
"""

import requests
from typing import Dict, List, Any, Optional, Union
from src.logger import get_logger

logger = get_logger(__name__)

# Base URL for the fake store API
BASE_URL = "https://fakestoreapi.com"


async def get_all_products() -> List[Dict[str, Any]]:
    """Fetch all products from the API.

    API Reference: GET /products
    Returns: Array of Product objects

    Product Schema:
    {
        "id": integer,
        "title": string,
        "price": number (float),
        "description": string,
        "category": string,
        "image": string (uri)
    }

    Returns:
        List[Dict[str, Any]]: List of product objects

    Raises:
        requests.HTTPError: If request fails
    """
    try:
        logger.info("Fetching all products from fakestoreapi.com")
        response = requests.get(f"{BASE_URL}/products")
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logger.error(f"Error fetching all products: {e}")
        raise


async def get_product(product_id: Union[int, str]) -> Dict[str, Any]:
    """Fetch a specific product by ID.

    API Reference: GET /products/{id}
    Path Parameter: id (integer) - Product ID
    Returns: Product object

    Product Schema:
    {
        "id": integer,
        "title": string,
        "price": number (float),
        "description": string,
        "category": string,
        "image": string (uri)
    }

    Args:
        product_id: The ID of the product to retrieve (must be integer)

    Returns:
        Dict[str, Any]: Product object

    Raises:
        requests.HTTPError: If product not found (404) or other HTTP errors
    """
    try:
        logger.info(f"Fetching product {product_id} from fakestoreapi.com")
        response = requests.get(f"{BASE_URL}/products/{product_id}")
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logger.error(f"Error fetching product {product_id}: {e}")
        raise

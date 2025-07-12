"""Product API endpoints.

This module contains all the API endpoints for product operations.
"""

from typing import List, Union
import requests
from fastapi import APIRouter, HTTPException, Path, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from src.services import product as product_service
from src.logger import get_logger

# Initialize logger
logger = get_logger(__name__)

# Define router
router = APIRouter(prefix="/products", tags=["Products"])


# Product Model - We're defining it in its own route file for better organization
class ProductModel(BaseModel):
    """Complete product model matching the API structure.

    This represents the full product data structure from fakestoreapi.com.
    """
    id: int = Field(..., description="Product ID")
    title: str = Field(..., description="Product title")
    price: float = Field(..., description="Product price")
    description: str = Field(..., description="Product description")
    category: str = Field(..., description="Product category")
    image: str = Field(..., description="Product image URL")


# API Endpoints
@router.get(
    "",
    operation_id="get_all_products",
    summary="Get all products",
    response_model=List[ProductModel],
    responses={
        200: {"description": "Success"},
        500: {"description": "Internal server error"}
        # Note: FastAPI will automatically handle validation errors
    }
)
async def get_all_products():
    """Retrieve a list of all available products.

    Returns:
        JSONResponse: List of all products
    """
    try:
        products = await product_service.get_all_products()
        return JSONResponse(content=products)
    except Exception as e:
        logger.error(f"Failed to get all products: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve products"
        )


@router.get(
    "/{product_id}",
    operation_id="get_product",
    summary="Get a single product",
    response_model=ProductModel,
    responses={
        200: {"description": "Success"},
        404: {"description": "Product not found"},
        500: {"description": "Internal server error"}
    }
)
async def get_product(
    product_id: Union[int, str] = Path(...,
                                       description="The ID of the product to retrieve (can be integer or string)")
):
    """Retrieve details of a specific product by ID.

    Args:
        product_id: The ID of the product to retrieve

    Returns:
        JSONResponse: Product details
    """
    try:
        product = await product_service.get_product(product_id)
        return JSONResponse(content=product)
    except requests.HTTPError as e:
        if e.response.status_code == 404:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product with ID {product_id} not found"
            )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve product"
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred"
        )

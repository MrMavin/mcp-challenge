from typing import List, Optional
import requests
from fastapi import APIRouter, HTTPException, Path, Query, Body, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, ConfigDict
from src.services import cart as cart_service
from src.logger import get_logger

# Initialize logger
logger = get_logger(__name__)

# Define router
router = APIRouter(prefix="/carts", tags=["Carts"])


# Models
class ProductModel(BaseModel):
    """Complete product model matching the API structure.

    This represents the full product data returned from the API.
    """
    id: int = Field(..., description="Product ID")
    title: str = Field(..., description="Product title")
    price: float = Field(..., description="Product price")
    description: str = Field(..., description="Product description")
    category: str = Field(..., description="Product category")
    image: str = Field(..., description="Product image URL")


class CartProductModel(BaseModel):
    """Simplified product model for cart operations, only requiring product ID."""
    id: int = Field(..., description="Product ID")


class SimpleCartModel(BaseModel):
    """Simplified model for cart creation and updates, only requiring product IDs."""
    userId: int = Field(..., description="User ID who owns this cart")
    products: List[CartProductModel] = Field(
        default_factory=list, description="List of product IDs in cart")


class CartModel(BaseModel):
    """Complete model for a shopping cart with full product details."""
    id: Optional[int] = Field(None, description="Cart ID")
    userId: int = Field(..., description="User ID who owns this cart")
    products: List[ProductModel] = Field(
        default_factory=list, description="List of products in cart")


# API Endpoints
@router.get(
    "",
    operation_id="get_all_carts",
    summary="Get all carts",
    description="Retrieves a list of all available shopping carts",
    response_model=List[CartModel],
    responses={
        200: {"description": "List of carts successfully retrieved"},
        500: {"description": "Internal server error"}
        # Note: 400 errors are automatically handled by FastAPI's validation
    }
)
async def get_all_carts():
    """Fetch all available shopping carts.

    Returns:
        List of cart objects
    """
    try:
        carts = await cart_service.get_all_carts()

        return JSONResponse(content=carts)
    except Exception as e:
        # We're not differentiating error types here for simplicity
        # In a production system, we would handle different error types differently
        logger.error(f"Failed to get all carts: {e}")

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve carts"
        )


@router.get(
    "/{cart_id}",
    operation_id="get_cart",
    summary="Get a single cart",
    description="Retrieve details of a specific cart by ID",
    response_model=CartModel,
    responses={
        200: {"description": "Cart successfully retrieved"},
        404: {"description": "Cart not found"},
        500: {"description": "Internal server error"}
        # Note: 400 errors are automatically handled by FastAPI's validation
    }
)
async def get_cart(
    cart_id: int | str = Path(...,
                              description="The ID of the cart to retrieve")
):
    """Get a specific cart by ID.

    Args:
        cart_id: The unique identifier of the cart

    Returns:
        Cart details
    """
    try:
        cart = await cart_service.get_cart(cart_id)
        return JSONResponse(content=cart)
    except requests.HTTPError as e:
        if e.response.status_code == 404:
            logger.error(f"Cart with ID {cart_id} not found")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Cart with ID {cart_id} not found"
            )
        logger.error(f"Failed to get cart {cart_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve cart"
        )
    except Exception as e:
        logger.error(f"Unexpected error getting cart {cart_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred"
        )


@router.post(
    "",
    operation_id="create_cart",
    summary="Add a new cart",
    description="Create a new shopping cart with just product IDs",
    response_model=CartModel,
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {"description": "Cart created successfully"},
        422: {"description": "Validation error"},
        500: {"description": "Internal server error"}
        # Note: 400 errors are automatically handled by FastAPI's validation
    }
)
async def create_cart(cart: SimpleCartModel = Body(...)):
    """Create a new shopping cart using simplified product model.

    Args:
        cart: The simplified cart data with only product IDs

    Returns:
        The newly created cart with ID assigned
    """
    try:
        # Convert SimpleCartModel to the format expected by the API
        cart_data = {
            "userId": cart.userId,
            "products": [
                {"id": product.id}
                for product in cart.products
            ]
        }

        # Create the cart with simplified product data
        logger.info(f"Creating cart with simplified product data: {cart_data}")
        new_cart = await cart_service.create_cart(cart_data)

        return JSONResponse(
            content=new_cart,
            status_code=status.HTTP_201_CREATED
        )
    except Exception as e:
        logger.error(f"Failed to create cart: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create cart"
        )


@router.put(
    "/{cart_id}",
    operation_id="update_cart",
    summary="Update a cart",
    description="Update an existing cart by ID using just product IDs",
    response_model=CartModel,
    responses={
        200: {"description": "Cart updated successfully"},
        404: {"description": "Cart not found"},
        422: {"description": "Validation error"},
        500: {"description": "Internal server error"}
        # Note: 400 errors are automatically handled by FastAPI's validation
    }
)
async def update_cart(
    cart_id: int | str = Path(..., description="The ID of the cart to update"),
    cart: SimpleCartModel = Body(...)
):
    """Update an existing cart with simplified product model.

    Args:
        cart_id: The ID of the cart to update
        cart: The simplified cart data with only product IDs

    Returns:
        The updated cart details
    """
    try:
        # Convert SimpleCartModel to the format expected by the API
        cart_data = {
            "userId": cart.userId,
            "products": [
                {"id": product.id}
                for product in cart.products
            ]
        }

        updated_cart = await cart_service.update_cart(cart_id, cart_data)
        return JSONResponse(content=updated_cart)
    except requests.HTTPError as e:
        if e.response.status_code == 404:
            logger.error(f"Cart with ID {cart_id} not found")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Cart with ID {cart_id} not found"
            )
        logger.error(f"Failed to update cart {cart_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update cart"
        )
    except Exception as e:
        logger.error(f"Unexpected error updating cart {cart_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred"
        )


@router.delete(
    "/{cart_id}",
    operation_id="delete_cart",
    summary="Delete a cart",
    description="Delete a specific cart by ID",
    responses={
        200: {"description": "Cart deleted successfully"},
        404: {"description": "Cart not found"},
        500: {"description": "Internal server error"}
        # Note: 400 errors are automatically handled by FastAPI's validation
    }
)
async def delete_cart(
    cart_id: int | str = Path(..., description="The ID of the cart to delete")
):
    """Delete a specific cart.

    Args:
        cart_id: The ID of the cart to delete

    Returns:
        Success message
    """
    try:
        result = await cart_service.delete_cart(cart_id)
        return JSONResponse(
            content={
                "message": f"Cart with ID {cart_id} successfully deleted",
                "data": result
            }
        )
    except requests.HTTPError as e:
        if e.response.status_code == 404:
            logger.error(f"Cart with ID {cart_id} not found")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Cart with ID {cart_id} not found"
            )
        logger.error(f"Failed to delete cart {cart_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete cart"
        )
    except Exception as e:
        logger.error(f"Unexpected error deleting cart {cart_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred"
        )

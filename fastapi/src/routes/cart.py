from typing import List
from fastapi import APIRouter, Request, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from src.services import cart as cart_service
from src.logger import get_logger
from src.utils.exceptions import handle_route_errors, validate_required_field
from src.validation.cart import validate_user_id, validate_cart_id, validate_products
from src.validation.common import parse_request_body

logger = get_logger(__name__)

router = APIRouter(prefix="/carts", tags=["Carts"])


class CartProduct(BaseModel):
    """Product item in a cart"""
    id: int
    quantity: int = 1


class GetCartRequest(BaseModel):
    """Request schema for getting a cart"""
    cartId: int | str


class ManageCartRequest(BaseModel):
    """Request schema for creating or updating a cart"""
    userId: int
    products: List[CartProduct]
    cartId: int | str | None = None


class DeleteCartRequest(BaseModel):
    """Request schema for deleting a cart"""
    cartId: int | str


@router.post(
    "/get-cart",
    operation_id="get_cart",
    summary="Get a single cart",
    description="Retrieve details of a specific cart by ID. Example: {\"cartId\": 1}"
)
@handle_route_errors("get cart")
async def get_cart(request: Request):
    # Parse and validate request body
    body = await parse_request_body(request)
    validate_required_field(body, "cartId", '{"cartId": 1}')

    # Validate with schema
    validated_request = GetCartRequest(**body)
    cart_id = validate_cart_id(validated_request.cartId)

    # Get cart from service
    cart = await cart_service.get_cart(cart_id)
    return JSONResponse(content=cart)


@router.post(
    "/manage-cart",
    operation_id="manage_cart",
    summary="Create or update a cart",
    description="Create a new cart or update an existing one. If cartId is provided, it updates the existing cart by REPLACING all products with the provided list (empty products array will clear the cart). If no cartId is provided, creates a new cart. Example: {\"userId\": 1, \"products\": [{\"id\": 1, \"quantity\": 2}], \"cartId\": 1}"
)
@handle_route_errors("manage cart")
async def manage_cart(request: Request):
    # Parse and validate request body
    body = await parse_request_body(request)
    validate_required_field(
        body, "userId", '{"userId": 1, "products": [{"id": 1, "quantity": 2}]}')

    # Validate with schema
    validated_request = ManageCartRequest(**body)
    user_id = validated_request.userId
    products = [product.model_dump() for product in validated_request.products]
    cart_id = validated_request.cartId

    cart_data = {
        "userId": user_id,
        "products": products
    }

    if cart_id:
        # Update existing cart
        validated_cart_id = validate_cart_id(cart_id)
        logger.info(
            f"Updating cart {validated_cart_id} with data: {cart_data}")
        updated_cart = await cart_service.update_cart(validated_cart_id, cart_data)
        return JSONResponse(content=updated_cart)
    else:
        # Create new cart
        logger.info(f"Creating new cart with data: {cart_data}")
        new_cart = await cart_service.create_cart(cart_data)

        # manually modify the cart id as the fakestoreapi.com returns id 11 by default
        # which contains an empty cart.
        new_cart['id'] = 1

        return JSONResponse(
            content=new_cart,
            status_code=status.HTTP_201_CREATED
        )


@router.post(
    "/delete-cart",
    operation_id="delete_cart",
    summary="Delete a cart",
    description="Delete a specific cart by ID. Example: {\"cartId\": 1}"
)
@handle_route_errors("delete cart")
async def delete_cart(request: Request):
    # Parse and validate request body
    body = await parse_request_body(request)
    validate_required_field(body, "cartId", '{"cartId": 1}')

    # Validate with schema
    validated_request = DeleteCartRequest(**body)
    cart_id = validate_cart_id(validated_request.cartId)

    # Delete cart
    logger.info(f"Deleting cart {cart_id}")
    result = await cart_service.delete_cart(cart_id)
    return JSONResponse(content=result)

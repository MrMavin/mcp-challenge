from typing import List
from fastapi import APIRouter, Request, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from src.services import cart as cart_service
from src.logger import get_logger
from src.utils.exceptions import handle_route_errors, validate_required_field
from src.validation.cart import validate_cart_id, validate_products
from src.validation.common import parse_request_body
from src.middleware.auth import extract_user_id_from_request

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
    # Ensure authentication
    extract_user_id_from_request(request)

    body = await parse_request_body(request)
    validate_required_field(body, "cartId", '{"cartId": 1}')

    validated_request = GetCartRequest(**body)
    cart_id = validate_cart_id(validated_request.cartId)

    cart = await cart_service.get_cart(cart_id)

    return JSONResponse(content=cart)


@router.post(
    "/manage-cart",
    operation_id="manage_cart",
    summary="Create or update a cart",
    description="Create a new cart or update an existing one. If cartId is provided, it updates the existing cart by REPLACING all products with the provided list (empty products array will clear the cart). If no cartId is provided, creates a new cart. Example: {\"products\": [{\"id\": 1, \"quantity\": 2}], \"cartId\": 1}"
)
@handle_route_errors("manage cart")
async def manage_cart(request: Request):
    # Ensure authentication
    user_id = extract_user_id_from_request(request)

    body = await parse_request_body(request)
    validate_required_field(
        body, "products", '{"products": [{"id": 1, "quantity": 2}]}')

    # Use manual validation for products to get detailed error messages
    products = validate_products(body.get("products", []))
    cart_id = body.get("cartId")

    cart_data = {
        "userId": user_id,
        "products": products
    }

    if cart_id:
        validated_cart_id = validate_cart_id(cart_id)

        updated_cart = await cart_service.update_cart(validated_cart_id, cart_data)

        return JSONResponse(content=updated_cart)
    else:
        new_cart = await cart_service.create_cart(cart_data)

        # manually modify the cart id as the fakestoreapi.com returns id 11 by default
        # which contains an empty cart.
        new_cart['id'] = 1

        return JSONResponse(
            content=new_cart,
            status_code=status.HTTP_201_CREATED
        )

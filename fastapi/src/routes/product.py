"""Product API endpoints.

This module contains all the API endpoints for product operations.
"""

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from src.services import product as product_service
from src.logger import get_logger
from src.utils.exceptions import handle_route_errors, validate_required_field
from src.validation.product import validate_product_id
from src.validation.common import parse_request_body

# Initialize logger
logger = get_logger(__name__)

# Define router
router = APIRouter(prefix="/products", tags=["Products"])


class GetProductRequest(BaseModel):
    """Request schema for getting a single product"""
    id: int | str



# API Endpoints


@router.get(
    "",
    operation_id="get_all_products",
    summary="Get all products",
    description="Retrieve all available products from the store",
)
@handle_route_errors("get all products")
async def get_all_products():
    products = await product_service.get_all_products()
    return JSONResponse(content=products)


@router.post(
    "/single-product",
    operation_id="get_product",
    summary="Get a single product",
    description="Retrieve details of a specific product by ID. Example: {\"id\": 1}"
)
@handle_route_errors("get product")
async def get_product(request: Request):
    # Parse and validate request body
    body = await parse_request_body(request)
    validate_required_field(body, "id", '{"id": 1}')
    
    # Validate with schema
    validated_request = GetProductRequest(**body)
    product_id = validate_product_id(validated_request.id)
    
    # Get product from service
    product = await product_service.get_product(product_id)
    return JSONResponse(content=product)

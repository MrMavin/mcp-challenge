"""Centralized exception handling utilities."""

from typing import Dict, Any, Callable
from functools import wraps
import requests
from fastapi import HTTPException, status
from pydantic import ValidationError
from src.logger import get_logger

logger = get_logger(__name__)


def handle_route_errors(operation: str):
    """Decorator to handle all route exceptions in a centralized way.
    
    Args:
        operation: Description of the operation for logging (e.g., "get cart", "create product")
    """
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except HTTPException:
                # Re-raise HTTP exceptions as-is (includes validation errors)
                raise
            except ValidationError as e:
                # Convert Pydantic validation errors to our custom format
                error_details = []
                for error in e.errors():
                    field = ".".join(str(loc) for loc in error['loc'])
                    error_details.append(f"{field}: {error['msg']}")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Validation error: {'; '.join(error_details)}"
                )
            except requests.HTTPError as e:
                # Handle requests errors (from service layer)
                if e.response.status_code == 404:
                    logger.error(f"Not found during {operation}: {e}")
                    # Extract resource info from the error or operation
                    resource = operation.split()[1] if len(operation.split()) > 1 else "Resource"
                    # Try to extract ID from the URL in the error
                    try:
                        # The URL typically ends with /carts/{id} or /products/{id}
                        url = str(e.response.url)
                        resource_id = url.split('/')[-1]
                        raise HTTPException(
                            status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"{resource.capitalize()} with ID {resource_id} not found"
                        )
                    except:
                        raise HTTPException(
                            status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"{resource.capitalize()} not found"
                        )
                logger.error(f"HTTP error during {operation}: {e}")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Failed to {operation}"
                )
            except Exception as e:
                logger.error(f"Unexpected error during {operation}: {e}")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="An unexpected error occurred"
                )
        return wrapper
    return decorator


def validate_required_field(body: Dict[str, Any], field: str, example: str):
    """Validate that a required field exists in the request body.
    
    Args:
        body: The request body dictionary
        field: The required field name
        example: Example JSON string to show in error message
        
    Raises:
        HTTPException: If the field is missing
    """
    if not body or field not in body:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Missing required field: {field}. Example: {example}"
        )
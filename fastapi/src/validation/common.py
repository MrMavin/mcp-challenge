"""Common validation functions."""

from typing import Dict, Any
from fastapi import HTTPException, status, Request


async def parse_request_body(request: Request) -> Dict[str, Any]:
    """Parse request body with detailed error messages."""
    try:
        body = await request.json()
    except Exception as e:
        # If no body or empty body, return empty dict
        raw_body = await request.body()
        if not raw_body:
            return {}
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid JSON in request body: {str(e)}"
        )

    if not isinstance(body, dict):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Request body must be a JSON object, got {type(body).__name__}"
        )

    return body
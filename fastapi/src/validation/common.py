"""Common validation functions."""

from typing import Dict, Any
from fastapi import HTTPException, status, Request


async def parse_request_body(request: Request) -> Dict[str, Any]:
    """Parse request body with LLM-friendly error messages."""
    try:
        body = await request.json()
    except Exception:
        # If no body or empty body, return empty dict
        raw_body = await request.body()
        if not raw_body:
            return {}
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The request body contains invalid JSON. Please ensure your request body is valid JSON format, for example: {\"key\": \"value\"}"
        )

    if not isinstance(body, dict):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The request body must be a JSON object with key-value pairs. Please provide data as: {\"key\": \"value\"} instead of arrays or other formats."
        )

    return body
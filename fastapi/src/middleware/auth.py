from typing import Optional
from fastapi import Request, HTTPException, status
from src.logger import get_logger

logger = get_logger(__name__)


def extract_user_id_from_request(request: Request) -> int:
    """
    Extract user ID from the Authorization header.

    Args:
        request: FastAPI request object

    Returns:
        int: User ID extracted from bearer token

    Raises:
        HTTPException: If no authorization header or invalid format
    """
    auth_header = request.headers.get("Authorization")

    if not auth_header:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required. Please provide Authorization header with Bearer token."
        )

    if not auth_header.startswith("Bearer "):
        logger.warning(f"Invalid authorization header format: {auth_header}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization header format. Expected: Bearer <user_id>"
        )

    # Extract the token part (which is actually the user ID)
    token = auth_header[7:]  # Remove "Bearer " prefix

    try:
        user_id = int(token)

        return user_id
    except ValueError:
        logger.warning(f"Invalid user ID format in token: {token}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user ID format. User ID must be a valid integer."
        )

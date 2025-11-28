"""
Authentication utilities for API protection.
Provides shared authentication dependencies for FastAPI routes.
"""

from fastapi import Header, HTTPException, Depends
from typing import Optional
from app.config import get_settings
from app.utils.logger import logger


async def verify_admin_key(x_admin_key: Optional[str] = Header(None, alias="X-Admin-Key")) -> bool:
    """
    Verify the admin API key from request headers.
    
    This is a FastAPI dependency that can be used to protect routes:
    
        @router.get("/protected")
        async def protected_route(_: bool = Depends(verify_admin_key)):
            return {"message": "You are authenticated"}
    
    Args:
        x_admin_key: The API key from X-Admin-Key header
        
    Returns:
        True if authentication is successful
        
    Raises:
        HTTPException: 401 if key is missing, 403 if key is invalid
    """
    settings = get_settings()
    
    # Check if admin key is configured
    if not settings.validate_admin_key():
        logger.error("ADMIN_API_KEY is not properly configured! Set it in your .env file.")
        raise HTTPException(
            status_code=500,
            detail="Server misconfiguration: Admin API key not set"
        )
    
    # Check if key was provided
    if not x_admin_key:
        logger.warning("Admin request without API key")
        raise HTTPException(
            status_code=401,
            detail="Admin API key required. Provide X-Admin-Key header."
        )
    
    # Validate the key
    if x_admin_key != settings.admin_api_key:
        logger.warning(f"Invalid admin API key attempt")
        raise HTTPException(
            status_code=403,
            detail="Invalid admin API key"
        )
    
    return True


async def optional_admin_key(x_admin_key: Optional[str] = Header(None, alias="X-Admin-Key")) -> Optional[bool]:
    """
    Optionally verify admin key - doesn't raise if missing.
    Useful for routes that have different behavior for admins.
    
    Returns:
        True if valid admin key provided, None otherwise
    """
    settings = get_settings()
    
    if not x_admin_key:
        return None
    
    if not settings.validate_admin_key():
        return None
        
    if x_admin_key == settings.admin_api_key:
        return True
    
    return None


# Dependency aliases for cleaner imports
AdminRequired = Depends(verify_admin_key)
AdminOptional = Depends(optional_admin_key)


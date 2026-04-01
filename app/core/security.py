# IMPORT LIBRARIES 

from fastapi import Security, HTTPException # Security → used for dependency injection (auth handling)
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
# HTTPBearer → extracts Bearer token from request header
from app.core.config import BEARER_TOKEN
# Import your secret token from config
# SECURITY SCHEME
security = HTTPBearer()
# AUTH FUNCTION

def get_auth(auth: HTTPAuthorizationCredentials = Security(security)):
    """
    Validates the Bearer token sent in request header.

    Args:
        auth: Extracted credentials from request

    Raises:
        HTTPException (401): If token is invalid

    Returns:
        str: Valid token
    """

    # Compare incoming token with expected token
    if auth.credentials != BEARER_TOKEN:
        # If token does not match → Unauthorized error
        raise HTTPException(
            status_code=401,
            detail="Unauthorized"
        )
    return auth.credentials
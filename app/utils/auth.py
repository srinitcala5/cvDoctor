import os

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

_bearer = HTTPBearer(auto_error=True)


def _jwt_secret() -> str:
    secret = os.getenv("SUPABASE_JWT_SECRET")
    if not secret:
        raise RuntimeError("SUPABASE_JWT_SECRET is not configured.")
    return secret


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(_bearer),
) -> dict:
    """
    Verify the Supabase-issued JWT and return the decoded claims.
    FastAPI dependency — inject via `Depends(get_current_user)`.

    Supabase signs JWTs with HS256 using SUPABASE_JWT_SECRET.
    The `sub` claim is the authenticated user's UUID.
    """
    token = credentials.credentials
    try:
        payload = jwt.decode(
            token,
            _jwt_secret(),
            algorithms=["HS256"],
            audience="authenticated",
        )
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_id: str | None = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token missing user identity.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return {"user_id": user_id, "email": payload.get("email", "")}

from fastapi import HTTPException, Header
from jose import jwt, JWTError
from .config import settings


async def verify_admin_token(authorization: str = Header(None)):
    """
    Dependency to verify JWT token in Authorization header.
    Only allows access if token is valid and email matches AUTHORIZED_EMAIL.
    """
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header missing")

    # Extract token from "Bearer <token>"
    try:
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            raise HTTPException(status_code=401, detail="Invalid authentication scheme")
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid authorization header format")

    # Verify token
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")

        if not email:
            raise HTTPException(status_code=401, detail="Invalid token payload")

        if email != settings.AUTHORIZED_EMAIL:
            raise HTTPException(status_code=403, detail="Unauthorized email")

        return {"email": email, "name": payload.get("name")}

    except JWTError as e:
        print(f"[AUTH] JWT Error: {e}")
        raise HTTPException(status_code=401, detail="Invalid or expired token")

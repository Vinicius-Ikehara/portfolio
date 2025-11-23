from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import RedirectResponse
from authlib.integrations.starlette_client import OAuth
from starlette.requests import Request
from jose import jwt, JWTError
from datetime import datetime, timedelta
from typing import Optional
from ..config import settings
import httpx

router = APIRouter(
    prefix="/api/auth",
    tags=["authentication"]
)

# Configure OAuth
oauth = OAuth()
oauth.register(
    name='google',
    client_id=settings.GOOGLE_CLIENT_ID,
    client_secret=settings.GOOGLE_CLIENT_SECRET,
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={
        'scope': 'openid email profile'
    }
)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


@router.get("/google/login")
async def google_login(request: Request):
    """Initiate Google OAuth login"""
    redirect_uri = settings.GOOGLE_REDIRECT_URI
    return await oauth.google.authorize_redirect(request, redirect_uri)


@router.get("/google/callback")
async def google_callback(request: Request):
    """Handle Google OAuth callback"""
    try:
        # Get token from Google
        token = await oauth.google.authorize_access_token(request)

        # Get user info
        user_info = token.get('userinfo')
        if not user_info:
            raise HTTPException(status_code=400, detail="Failed to get user info from Google")

        email = user_info.get('email')

        # Check if email is authorized
        if email != settings.AUTHORIZED_EMAIL:
            # Redirect to frontend with error
            frontend_url = "https://portfolio.ikehara.dev.br/admin?error=unauthorized"
            return RedirectResponse(url=frontend_url)

        # Create JWT token
        access_token = create_access_token(
            data={"sub": email, "name": user_info.get('name'), "picture": user_info.get('picture')}
        )

        # Redirect to frontend with token
        frontend_url = f"https://portfolio.ikehara.dev.br/admin?token={access_token}"
        return RedirectResponse(url=frontend_url)

    except Exception as e:
        print(f"[AUTH ERROR] {e}")
        frontend_url = "https://portfolio.ikehara.dev.br/admin?error=auth_failed"
        return RedirectResponse(url=frontend_url)


@router.post("/verify")
async def verify_token(token: str):
    """Verify JWT token"""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")

        if email != settings.AUTHORIZED_EMAIL:
            raise HTTPException(status_code=403, detail="Unauthorized email")

        return {
            "valid": True,
            "email": email,
            "name": payload.get("name"),
            "picture": payload.get("picture")
        }
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

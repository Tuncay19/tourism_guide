from fastapi import APIRouter, Request, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import create_access_token
from app.db.database import get_db
from app.db.models import AuthProviderEnum
from app.oauth.clients import oauth
from app.oauth.utils import find_or_create_oauth_user

router = APIRouter(prefix="/api/auth", tags=["oauth"])


# ---- Google ----

@router.get("/google")
async def google_login(request: Request):
    return await oauth.google.authorize_redirect(request, settings.google_redirect_uri)


@router.get("/google/callback")
async def google_callback(request: Request, db: Session = Depends(get_db)):
    token = await oauth.google.authorize_access_token(request)
    profile = token.get("userinfo") or await oauth.google.userinfo(token=token)

    user = find_or_create_oauth_user(
        db,
        provider=AuthProviderEnum.GOOGLE,
        provider_account_id=profile["sub"],
        email=profile.get("email"),
        full_name=profile.get("name"),
        avatar_url=profile.get("picture"),
    )

    jwt_token = create_access_token({"sub": user.id})
    return RedirectResponse(f"{settings.client_url}/oauth-success?token={jwt_token}")


# ---- Facebook ----

@router.get("/facebook")
async def facebook_login(request: Request):
    return await oauth.facebook.authorize_redirect(request, settings.facebook_redirect_uri)


@router.get("/facebook/callback")
async def facebook_callback(request: Request, db: Session = Depends(get_db)):
    token = await oauth.facebook.authorize_access_token(request)
    resp = await oauth.facebook.get("me?fields=id,name,email,picture", token=token)
    profile = resp.json()

    user = find_or_create_oauth_user(
        db,
        provider=AuthProviderEnum.FACEBOOK,
        provider_account_id=profile["id"],
        email=profile.get("email"),
        full_name=profile.get("name"),
        avatar_url=profile.get("picture", {}).get("data", {}).get("url"),
    )

    jwt_token = create_access_token({"sub": user.id})
    return RedirectResponse(f"{settings.client_url}/oauth-success?token={jwt_token}")

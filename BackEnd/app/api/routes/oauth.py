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

# Token yalnız bizim app-ın açıla biləcəyi ünvanlara göndərilir (təhlükəsizlik üçün).
# exp:// — Expo Go, azturizm:// — hazır (build olunmuş) app
ALLOWED_APP_REDIRECT_PREFIXES = ("exp://", "exps://", "azturizm://")


@router.get("/google")
async def google_login(request: Request, app_redirect: str | None = None):
    # Mobil app hansı ünvana qayıtmaq istədiyini bildirir; yoxlayıb session-da saxlayırıq
    if app_redirect and app_redirect.startswith(ALLOWED_APP_REDIRECT_PREFIXES):
        request.session["app_redirect"] = app_redirect
    else:
        request.session.pop("app_redirect", None)

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

    base = request.session.pop("app_redirect", None) or f"{settings.client_url}/oauth-success"
    separator = "&" if "?" in base else "?"
    return RedirectResponse(f"{base}{separator}token={jwt_token}")

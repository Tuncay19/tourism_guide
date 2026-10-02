from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from app.core.config import settings
from app.api.routes import auth, oauth

app = FastAPI(title="Qarabağ Tur Platforması API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.client_url],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Authlib-in OAuth axını (state saxlamaq) üçün session middleware lazımdır
app.add_middleware(SessionMiddleware, secret_key=settings.session_secret)

app.include_router(auth.router)
app.include_router(oauth.router)


@app.get("/")
def root():
    return {"message": "Qarabağ Tur Platforması API işləyir 🇦🇿"}

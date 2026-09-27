import random
from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.email import send_verification_email
from app.core.security import hash_password, verify_password, create_access_token
from app.db.database import get_db
from app.db.models import User
from app.schemas.auth import (
    SignupRequest,
    LoginRequest,
    TokenResponse,
    UserOut,
    VerifyEmailRequest,
    ResendCodeRequest,
    MessageResponse,
)

router = APIRouter(prefix="/api/auth", tags=["auth"])

CODE_VALID_MINUTES = 15


def _generate_code() -> str:
    return f"{random.randint(0, 999999):06d}"


@router.post("/signup", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
def signup(payload: SignupRequest, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=409, detail="Bu email artıq qeydiyyatdan keçib.")

    code = _generate_code()
    user = User(
        email=payload.email,
        password=hash_password(payload.password),
        full_name=payload.full_name,
        verification_code=code,
        verification_code_expires_at=datetime.now(timezone.utc) + timedelta(minutes=CODE_VALID_MINUTES),
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    send_verification_email(user.email, code)

    token = create_access_token({"sub": user.id})
    return TokenResponse(
        message="Qeydiyyat uğurla tamamlandı. Email-inizə göndərilən kodu təsdiqləyin.",
        token=token,
        user=UserOut.model_validate(user),
    )


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()

    if not user or not user.password or not verify_password(payload.password, user.password):
        raise HTTPException(status_code=401, detail="Email və ya şifrə yanlışdır.")

    token = create_access_token({"sub": user.id})
    return TokenResponse(message="Giriş uğurludur.", token=token, user=UserOut.model_validate(user))


@router.get("/me", response_model=UserOut)
def get_me(current_user: User = Depends(get_current_user)):
    return UserOut.model_validate(current_user)


@router.post("/verify-email", response_model=MessageResponse)
def verify_email(payload: VerifyEmailRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="İstifadəçi tapılmadı.")

    if user.is_verified:
        return MessageResponse(message="Email artıq təsdiqlənib.")

    if not user.verification_code or user.verification_code != payload.code:
        raise HTTPException(status_code=400, detail="Kod yanlışdır.")

    if user.verification_code_expires_at and user.verification_code_expires_at < datetime.now(timezone.utc):
        raise HTTPException(status_code=400, detail="Kodun vaxtı bitib. Yeni kod tələb edin.")

    user.is_verified = True
    user.verification_code = None
    user.verification_code_expires_at = None
    db.commit()

    return MessageResponse(message="Email uğurla təsdiqləndi.")


@router.post("/resend-code", response_model=MessageResponse)
def resend_code(payload: ResendCodeRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="İstifadəçi tapılmadı.")

    if user.is_verified:
        return MessageResponse(message="Email artıq təsdiqlənib.")

    code = _generate_code()
    user.verification_code = code
    user.verification_code_expires_at = datetime.now(timezone.utc) + timedelta(minutes=CODE_VALID_MINUTES)
    db.commit()

    send_verification_email(user.email, code)
    return MessageResponse(message="Yeni kod göndərildi.")

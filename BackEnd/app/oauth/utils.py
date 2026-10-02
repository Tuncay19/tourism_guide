from sqlalchemy.orm import Session

from app.db.models import User, Account, AuthProviderEnum


def find_or_create_oauth_user(
    db: Session,
    provider: AuthProviderEnum,
    provider_account_id: str,
    email: str | None,
    full_name: str | None,
    avatar_url: str | None,
) -> User:
    # 1) Bu provider ilə əvvəllər qeydiyyatdan keçib?
    existing_account = (
        db.query(Account)
        .filter(Account.provider == provider, Account.provider_account_id == provider_account_id)
        .first()
    )
    if existing_account:
        return existing_account.user

    # 2) Eyni email ilə LOCAL və ya başqa provider-dən hesab varmı?
    user = db.query(User).filter(User.email == email).first() if email else None

    if not user:
        user = User(
            email=email or f"{provider.value.lower()}_{provider_account_id}@no-email.qarabagtour.com",
            full_name=full_name or "İstifadəçi",
            avatar_url=avatar_url,
            is_verified=True,
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    account = Account(user_id=user.id, provider=provider, provider_account_id=provider_account_id)
    db.add(account)
    db.commit()

    return user

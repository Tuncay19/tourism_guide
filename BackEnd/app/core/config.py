from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str
    client_url: str = "http://localhost:3000"

    jwt_secret: str
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 10080  # 7 gün

    session_secret: str

    google_client_id: str = ""
    google_client_secret: str = ""
    google_redirect_uri: str = ""

    # Email göndərmə (Brevo HTTP API) — Render pulsuz planı SMTP-ni bloklayır
    brevo_api_key: str = ""
    mail_sender_email: str = ""
    mail_sender_name: str = "AzTurizm Guide"

    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "ignore"


settings = Settings()

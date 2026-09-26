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

    facebook_client_id: str = ""
    facebook_client_secret: str = ""
    facebook_redirect_uri: str = ""

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()

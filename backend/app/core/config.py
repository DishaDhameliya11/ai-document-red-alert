from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "AI Document Red Alert Detection System API"
    PROJECT_DESCRIPTION: str = (
        "Backend API for detecting risky, suspicious, and sensitive document content."
    )
    VERSION: str = "0.1.0"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    MAX_UPLOAD_SIZE_MB: int = 10

    MONGODB_URL: str = "mongodb://localhost:27017/"
    MONGODB_DB_NAME: str = "red_alert_db"

    JWT_SECRET_KEY: str = "change_this_secret_key_later"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    OCR_LANGUAGES: str = "eng+guj"
    
    FRONTEND_URL: str = "http://localhost:5173"

    API_V1_PREFIX: str = "/api/v1"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


settings = Settings()
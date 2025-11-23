from pydantic_settings import BaseSettings
from pydantic import field_validator
from typing import List, Union
import json
import os


class Settings(BaseSettings):
    # Application
    APP_NAME: str = "Portfolio API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True

    # Database
    DATABASE_URL: str = "sqlite:///./portfolio.db"

    # CORS
    CORS_ORIGINS: Union[List[str], str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "https://portfolio-frontend.mktdr8.easypanel.host",
        "https://portfolio.ikehara.dev.br"
    ]

    @field_validator('CORS_ORIGINS', mode='before')
    @classmethod
    def parse_cors_origins(cls, v):
        """
        Parse CORS_ORIGINS from environment variable.
        Aceita tanto uma lista quanto uma string JSON.
        """
        print(f"[CONFIG] Parsing CORS_ORIGINS: type={type(v)}, value={v}")

        if isinstance(v, str):
            try:
                # Tenta fazer parse como JSON
                parsed = json.loads(v)
                print(f"[CONFIG] Parsed as JSON: {parsed}")
                if isinstance(parsed, list):
                    return parsed
                return [parsed]
            except json.JSONDecodeError as e:
                print(f"[CONFIG] Not valid JSON, treating as CSV: {e}")
                # Se não for JSON válido, trata como string separada por vírgula
                result = [origin.strip() for origin in v.split(',')]
                print(f"[CONFIG] Parsed as CSV: {result}")
                return result

        print(f"[CONFIG] Using default value (list): {v}")
        return v

    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ALGORITHM: str = "HS256"

    # Google OAuth (configure via environment variables)
    GOOGLE_CLIENT_ID: str = ""
    GOOGLE_CLIENT_SECRET: str = ""
    GOOGLE_REDIRECT_URI: str = ""

    # Authorized Email (only this email can access admin)
    AUTHORIZED_EMAIL: str = "vhikehara@gmail.com"

    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60

    # File Upload
    MAX_FILE_SIZE: int = 5 * 1024 * 1024  # 5MB
    ALLOWED_IMAGE_TYPES: List[str] = ["image/jpeg", "image/png", "image/webp"]

    class Config:
        env_file = ".env"
        case_sensitive = True


# Inicializar settings com tratamento de erros
try:
    print("[CONFIG] Initializing settings...")
    settings = Settings()
    print(f"[CONFIG] Settings initialized successfully!")
    print(f"[CONFIG] CORS_ORIGINS final value: {settings.CORS_ORIGINS}")
    print(f"[CONFIG] DEBUG: {settings.DEBUG}")
except Exception as e:
    print(f"[CONFIG ERROR] Failed to initialize settings: {e}")
    import traceback
    traceback.print_exc()
    raise

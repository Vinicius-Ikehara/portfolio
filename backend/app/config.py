from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    # Application
    APP_NAME: str = "Portfolio API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True

    # Database
    DATABASE_URL: str = "sqlite:///./portfolio.db"

    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:5173"]

    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60

    # File Upload
    MAX_FILE_SIZE: int = 5 * 1024 * 1024  # 5MB
    ALLOWED_IMAGE_TYPES: List[str] = ["image/jpeg", "image/png", "image/webp"]

    # Supabase - Last.fm Analytics
    SUPABASE_URL: str = ""
    SUPABASE_KEY: str = ""

    # Supabase - Pokédex (Vector Store + Chat Memory)
    SUPABASE_POKEDEX_URL: str = ""
    SUPABASE_POKEDEX_KEY: str = ""

    # OpenAI API (para Pokédex RAG)
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-5.2"

    # LangSmith (opcional - para observabilidade)
    LANGCHAIN_TRACING_V2: bool = False
    LANGCHAIN_API_KEY: str = ""
    LANGCHAIN_PROJECT: str = "pokedex-agent"

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

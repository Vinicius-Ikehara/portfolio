from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    # Application
    APP_NAME: str = "Portfolio API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False

    # Database
    DATABASE_URL: str = "sqlite:///./portfolio.db"

    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:5173"]

    # Security
    SECRET_KEY: str = ""
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

    # Gemini API (Video Q&A)
    GEMINI_API_KEY: str = ""
    VIDEO_QA_MAX_DURATION_SECONDS: int = 180

    # Langfuse (opcional - para observabilidade LLM)
    LANGFUSE_ENABLED: bool = False
    LANGFUSE_PUBLIC_KEY: str = ""
    LANGFUSE_SECRET_KEY: str = ""
    LANGFUSE_BASE_URL: str = "http://localhost:3000"

    # ClickHouse (acidentes H3)
    CLICKHOUSE_URL: str = "http://localhost:8123"
    CLICKHOUSE_USER: str = "clickhouse"
    CLICKHOUSE_PASSWORD: str = "clickhouse"

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

if not settings.DEBUG and not settings.SECRET_KEY:
    import warnings
    warnings.warn("SECRET_KEY is empty in non-DEBUG mode — set it in .env before exposing to the internet.", RuntimeWarning)

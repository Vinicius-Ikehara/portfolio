from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from .database import engine, Base
from .routers import projects, experiences, profile
from .config import settings

# Criar as tabelas no banco de dados
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.APP_NAME,
    description="API para gerenciar portfólio de desenvolvedor IA",
    version=settings.APP_VERSION,
    docs_url="/docs" if settings.DEBUG else None,  # Desabilitar docs em produção
    redoc_url="/redoc" if settings.DEBUG else None,
)

# Security Headers Middleware
@app.middleware("http")
async def add_security_headers(request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    return response

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Comprimir respostas
app.add_middleware(GZipMiddleware, minimum_size=1000)

# Incluir routers
app.include_router(projects.router)
app.include_router(experiences.router)
app.include_router(profile.router)


@app.get("/")
def read_root():
    return {
        "message": "Portfolio API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.get("/debug/config")
def debug_config():
    """
    Endpoint temporário para debug de configurações.
    REMOVER em produção ou quando DEBUG=False!
    """
    if not settings.DEBUG:
        return {"error": "Debug mode is disabled"}

    return {
        "cors_origins": settings.CORS_ORIGINS,
        "database_url": settings.DATABASE_URL.replace("://", "://***@") if "://" in settings.DATABASE_URL else settings.DATABASE_URL,
        "debug": settings.DEBUG,
        "app_name": settings.APP_NAME,
        "app_version": settings.APP_VERSION,
    }

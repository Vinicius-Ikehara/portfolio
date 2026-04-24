from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse
from starlette.requests import Request
from .database import engine, Base
from .rate_limit import limiter
from .routers import projects, experiences, profile, webhook_proxy, lastfm, langfuse_dashboard, acidentes_h3, video_qa
from .config import settings

# Criar as tabelas no banco de dados
Base.metadata.create_all(bind=engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    try:
        from workflows.pokedex.observability import init_observability
        init_observability()
    except Exception as e:
        print(f"[Startup] Observability init skipped: {e}")
    yield
    # Shutdown
    try:
        from workflows.pokedex.observability import shutdown_observability
        shutdown_observability()
    except Exception:
        pass


app = FastAPI(
    title=settings.APP_NAME,
    description="API para gerenciar portfólio de desenvolvedor IA",
    version=settings.APP_VERSION,
    docs_url="/docs" if settings.DEBUG else None,  # Desabilitar docs em produção
    redoc_url="/redoc" if settings.DEBUG else None,
    lifespan=lifespan,
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

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
app.include_router(webhook_proxy.router)
app.include_router(lastfm.router)
app.include_router(langfuse_dashboard.router)
app.include_router(acidentes_h3.router)
app.include_router(video_qa.router)


@app.middleware("http")
async def mcp_bearer_auth(request: Request, call_next):
    if request.url.path.startswith("/mcp"):
        token = settings.MCP_API_TOKEN
        if token:
            auth = request.headers.get("Authorization", "")
            if not auth.startswith("Bearer ") or auth[7:] != token:
                return JSONResponse({"detail": "Unauthorized"}, status_code=401)
    return await call_next(request)


try:
    from .mcp_server import mcp
    app.mount("/mcp", mcp.streamable_http_app())
except Exception as e:
    print(f"[Startup] MCP server not mounted: {e}")


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

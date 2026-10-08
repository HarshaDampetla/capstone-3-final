import uuid
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from src.core.config import settings
from src.core.database import Base, engine
from src.core.logging import setup_logging
from src.api.health import router as health_router
from src.api.auth_router import router as auth_router
from src.api.admin_user_router import router as admin_user_router
from src.api.catalog_router import public_router as catalog_router, admin_router as admin_catalog_router
from src.api.watchlist_router import router as watchlist_router
from src.api.order_router import router as order_router
from src.api.portfolio_router import router as portfolio_router
from src.api.analytics_router import router as analytics_router

# Setup structured logging (NFR-06)
setup_logging()

# Initialize Database tables for local development
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.APP_NAME,
    description="MarketScope — Stock Trading & Portfolio Analytics Platform (BC-AINE-006)",
    version="0.1.0",
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Correlation ID Middleware (NFR-06)
@app.middleware("http")
async def add_correlation_id_middleware(request: Request, call_next):
    correlation_id = request.headers.get("X-Correlation-ID", str(uuid.uuid4()))
    request.state.correlation_id = correlation_id
    response: Response = await call_next(request)
    response.headers["X-Correlation-ID"] = correlation_id
    return response


# Mount Routers
app.include_router(health_router)
app.include_router(auth_router)
app.include_router(admin_user_router)
app.include_router(catalog_router)
app.include_router(admin_catalog_router)
app.include_router(watchlist_router)
app.include_router(order_router)
app.include_router(portfolio_router)
app.include_router(analytics_router)


@app.get("/")
def root():
    return {
        "app": settings.APP_NAME,
        "version": "0.1.0",
        "docs": "/docs",
        "status": "online",
    }

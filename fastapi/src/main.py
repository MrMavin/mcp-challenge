from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
import sentry_sdk
from starlette.middleware.cors import CORSMiddleware
from fastapi_mcp import FastApiMCP

from src.routes import cart, product
from src.config import app_configs, settings


@asynccontextmanager
async def lifespan(_application: FastAPI) -> AsyncGenerator:
    # Startup
    yield
    # Shutdown


app = FastAPI(**app_configs, lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_origin_regex=settings.CORS_ORIGINS_REGEX,
    allow_credentials=True,
    allow_methods=("GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"),
    allow_headers=settings.CORS_HEADERS,
)

app.include_router(cart.router)
app.include_router(product.router)


mcp = FastApiMCP(
    app,
    name="Store MCP",
    describe_all_responses=False,
    describe_full_response_schema=False
)

mcp.mount()

if settings.ENVIRONMENT.is_deployed:
    sentry_sdk.init(
        dsn=settings.SENTRY_DSN,
        environment=settings.ENVIRONMENT,
    )


@app.get("/healthcheck", include_in_schema=False)
async def healthcheck() -> dict[str, str]:
    return {"status": "ok"}

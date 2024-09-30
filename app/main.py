import logging
import sys
import time

from fastapi import FastAPI, Request
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware

from app.api.main import api_router
from app.core.config import settings
from app.core.db import SQLModel, engine

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="{asctime} | {levelname} | {message}",
    datefmt="%Y-%m-%d %H:%M:%S",
    style="{",
    stream=sys.stderr,
)
logger = logging.getLogger(__name__)

SQLModel.metadata.create_all(engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url="/openapi.json",
)

app.add_middleware(TrustedHostMiddleware, allowed_hosts=settings.allowed_hosts)


@app.middleware("http")
async def log_request_and_add_timing(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time

    user_agent = request.headers.get("User-Agent", "N/A")
    client_ip = request.headers.get("cf-connecting-ip", request.client.host)
    cf_ipcountry = request.headers.get("cf-ipcountry", "N/A")
    method = request.method
    url = request.url.path
    status_code = response.status_code

    log_str = f"{client_ip} ({cf_ipcountry}) - "
    log_str += f'"{method} {url} HTTP/{request.scope["http_version"]}" {status_code} - '
    log_str += f"User-Agent: {user_agent} - "
    log_str += f"Process-Time: {process_time:.4f}s"

    logger.info(log_str)

    response.headers["X-Process-Time"] = str(process_time)
    return response


# Set all CORS enabled origins
if settings.all_cors_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.all_cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


@app.get("/", response_class=HTMLResponse, include_in_schema=False)
async def read_items():
    with open("app/static/index.html") as f:
        html_content = f.read()

    return HTMLResponse(content=html_content, status_code=200)


app.mount("/static", StaticFiles(directory="app/static", html=True), name="static")
app.include_router(api_router, prefix=settings.API_V1_STR)

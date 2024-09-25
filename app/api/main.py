from fastapi import APIRouter

from app.api.routes import models

api_router = APIRouter()
api_router.include_router(models.router, prefix="/models", tags=["models"])

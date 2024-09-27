from sqlmodel import SQLModel, create_engine

from app import models
from app.core.config import settings

engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URI, connect_args={"check_same_thread": False}
)

from sqlmodel import SQLModel, create_engine

from app import models
from app.core.config import settings

engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))

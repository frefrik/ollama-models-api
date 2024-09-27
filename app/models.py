import uuid
from datetime import date, datetime

from sqlmodel import JSON, Column, DateTime, Field, SQLModel, func


class ModelBase(SQLModel):
    model_identifier: str
    namespace: str | None = None
    model_name: str
    model_type: str
    description: str | None = None
    capability: str | None = None
    labels: list[str] = Field(sa_column=Column(JSON, nullable=False))
    pulls: int
    tags: int
    last_updated: date
    last_updated_str: str
    url: str

    class Config:
        protected_namespaces = ()


class Model(ModelBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    timestamp: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            nullable=False,
            server_default=func.now(),
        )
    )


class ModelRead(ModelBase):
    class Config:
        from_attributes = True


class ModelsPublic(SQLModel):
    models: list[ModelRead]
    total_count: int
    limit: int
    skip: int
    data_updated: datetime | None = None

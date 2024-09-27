from typing import Annotated, Any, List, Literal

from dotenv import load_dotenv
from pydantic import AnyUrl, BeforeValidator, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


def parse_cors(v: Any) -> List[str] | str:
    if isinstance(v, str) and not v.startswith("["):
        return [i.strip() for i in v.split(",")]
    elif isinstance(v, list | str):
        return v
    raise ValueError(v)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="../.env",
        env_ignore_empty=True,
        extra="ignore",
    )
    API_V1_STR: str = "/api/v1"
    FRONTEND_HOST: str = "http://localhost:8000"
    ENVIRONMENT: Literal["local", "production"] = "local"

    BACKEND_CORS_ORIGINS: Annotated[list[AnyUrl] | str, BeforeValidator(parse_cors)] = (
        []
    )

    @computed_field
    @property
    def all_cors_origins(self) -> list[str]:
        return [str(origin).rstrip("/") for origin in self.BACKEND_CORS_ORIGINS] + [
            self.FRONTEND_HOST
        ]

    PROJECT_NAME: str
    SQLITE_DATABASE_PATH: str = "./ollama_models.db"

    @computed_field
    @property
    def SQLITE_DATABASE_URI(self) -> str:
        if self.ENVIRONMENT == "local":
            return self.SQLITE_DATABASE_PATH
        elif self.ENVIRONMENT == "production":
            return "./ollama_models.db"
        else:
            raise ValueError(f"Unknown ENVIRONMENT: {self.ENVIRONMENT}")

    @computed_field
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        return f"sqlite:///{self.SQLITE_DATABASE_URI}"


settings = Settings()

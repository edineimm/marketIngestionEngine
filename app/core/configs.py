from pydantic_settings import BaseSettings
from sqlalchemy.ext.declarative import declarative_base

DBBaseModel = declarative_base()


class Settings(BaseSettings):
    """App settings"""

    # Database
    API_V1_STR: str = "/api/v1"
    DB_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/market_db"
    PROJECT_NAME: str = "Market Data API"
    VERSION: str = "1.0"

    class Config:
        case_sensitive = True


settings = Settings()

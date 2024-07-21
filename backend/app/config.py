from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # App
    APP_PORT: int
    APP_HOME: str
    PYTHON_ENV: str

    # PostgreSQL
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    # Neo4j
    NEO4J_USER: str
    NEO4J_PASSWORD: str
    NEO4J_HTTP_PORT: int
    NEO4J_BOLT_PORT: int

    # Derived settings
    DATABASE_URL: str = None
    NEO4J_URI: str = None
    CELERY_BROKER_URL: str = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.DATABASE_URL = f"postgres://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@postgres:5432/{self.POSTGRES_DB}"
        self.NEO4J_URI = f"bolt://neo4j:{self.NEO4J_BOLT_PORT}"
        self.CELERY_BROKER_URL = "redis://redis:6379/0"

    class Config:
        env_file = ".env"

settings = Settings()
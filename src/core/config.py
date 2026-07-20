from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # App Configuration
    APP_NAME: str = "Project Sahyadri"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = True

    # Database Configuration
    DB_HOST: str = "localhost"  # Default to localhost for local script execution
    DB_PORT: int = 5432
    DB_USER: str = "sahyadri"
    DB_PASSWORD: str = "sahyadri_secret"
    DB_NAME: str = "sahyadri_db"

    # Redis Configuration
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379

    # MinIO Configuration
    MINIO_ENDPOINT: str = "localhost:9000"
    MINIO_ACCESS_KEY: str = "minioadmin"
    MINIO_SECRET_KEY: str = "minio_secret"

    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"

    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


settings = Settings()

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import AsyncGenerator

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://munde:munde_dev_password@127.0.0.1:5432/munde_core?ssl=disable"
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
async_url = settings.DATABASE_URL.replace("+psycopg2", "+asyncpg")

engine = create_async_engine(async_url, echo=False)
AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

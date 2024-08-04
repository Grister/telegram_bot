import os

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from database.models import Base

load_dotenv()

HOST = os.environ.get("POSTGRES_HOST")
PORT = os.environ.get("POSTGRES_PORT")
USER = os.environ.get("POSTGRES_USER")
NAME = os.environ.get("POSTGRES_NAME")
PASSWORD = os.environ.get("POSTGRES_PASSWORD")

DATABASE_URL = f"postgresql+asyncpg://{USER}:{PASSWORD}@{HOST}:{PORT}/{NAME}"

engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

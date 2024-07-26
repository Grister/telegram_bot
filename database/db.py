import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from database.models import Base

load_dotenv()

HOST = os.environ.get("POSTGRES_HOST")
PORT = os.environ.get("POSTGRES_PORT")
USER = os.environ.get("POSTGRES_USER")
NAME = os.environ.get("POSTGRES_NAME")
PASSWORD = os.environ.get("POSTGRES_PASSWORD")

DATABASE_URL = f"postgresql+asyncpg://{USER}:{PASSWORD}@{HOST}:{PORT}/{NAME}"

engine = create_async_engine(DATABASE_URL, echo=True)
async_session = async_sessionmaker(engine)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

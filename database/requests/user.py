from database.db import async_session
from database.models import User
from utils.db_utils import get_or_create


async def set_user(tg_id, username):
    async with async_session() as session:
        await get_or_create(session, User, tg_id=tg_id, username=username)

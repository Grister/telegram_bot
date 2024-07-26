from database.db import async_session
from utils.db_utils import get_or_create, get_user_by_id
from database.models import User, Tag, Note
from sqlalchemy import select


async def set_note(user_id, tag_name, note):
    async with async_session() as session:
        user = await get_user_by_id(session, user_id)
        tag = await get_or_create(session, Tag, user_id=user.id, name=tag_name)

        instance = Note(tag_id=tag.id, content=note)
        session.add(instance)

        await session.commit()


async def get_tags(user_id):
    async with async_session() as session:
        user = await get_user_by_id(session, user_id)

        return await session.scalars(select(Tag).where(Tag.user_id == user.id))

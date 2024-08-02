import utils.db_utils as db_tools

from typing import Optional, List
from database.db import async_session
from database.models import Tag, Note
from sqlalchemy import select, delete, update


async def set_note(user_id: int, tag_name: str, note: str) -> None:
    async with async_session() as session:
        user = await db_tools.get_user_by_id(session, user_id)
        tag = await db_tools.get_or_create(session, Tag, user_id=user.id, name=tag_name)

        return await db_tools.create_instance(session, Note, tag_id=tag.id, content=note)


async def get_tag_list(user_id: int) -> List[Tag]:
    async with async_session() as session:
        user = await db_tools.get_user_by_id(session, user_id)
        return await db_tools.get_list(session, Tag, user_id=user.id)


async def get_tag_instance(tag_id: int) -> Optional[Tag]:
    async with async_session() as session:
        return await db_tools.get_instance(session, Tag, id=tag_id)


async def get_notes_by_tag(tag_id: int) -> List[Note]:
    async with async_session() as session:
        return await db_tools.get_list(session, Note, order_by='created_at', tag_id=tag_id)


async def get_note(note_id: int) -> Optional[Note]:
    async with async_session() as session:
        return await db_tools.get_instance(session, Note, id=note_id)


async def delete_note(note_id: int) -> None:
    async with async_session() as session:
        await session.execute(
            delete(Note).where(Note.id == note_id)
        )
        await session.commit()


async def update_note(note_id: int, new_content: str) -> Optional[Note]:
    async with async_session() as session:
        result = await session.execute(
            update(Note)
            .where(Note.id == note_id)
            .values(content=new_content)
            .returning(Note)
        )
        await session.commit()
        return result.scalar_one_or_none()


async def delete_tag(tag_id: int) -> None:
    async with async_session() as session:
        await session.execute(
            delete(Tag).where(Tag.id == tag_id)
        )
        await session.commit()

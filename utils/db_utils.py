from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import User


async def get_or_create(session, model, **kwargs):
    instance = await session.scalar(select(model).filter_by(**kwargs))
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        session.add(instance)
        await session.commit()
        return instance


async def get_user_by_id(session: AsyncSession, user_tg_id: int) -> Optional[User]:
    return await session.scalar(select(User).where(User.tg_id == user_tg_id))

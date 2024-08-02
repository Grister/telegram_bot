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


async def get_instance(session, model, **kwargs):
    return await session.scalar(
        select(model).filter_by(**kwargs)
    )


async def get_list(session, model, order_by: str = None, **kwargs):
    result = await session.scalars(
        select(model).filter_by(**kwargs).order_by(order_by)
    )
    return result.all()


async def create_instance(session, model, **kwargs):
    instance = model(**kwargs)

    session.add(instance)
    await session.commit()
    await session.refresh(instance)

    return instance


async def get_user_by_id(session: AsyncSession, user_tg_id: int) -> Optional[User]:
    return await session.scalar(select(User).where(User.tg_id == user_tg_id))

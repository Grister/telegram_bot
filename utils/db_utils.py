from sqlalchemy import select

from database.models import User


async def get_or_create(session, model, **kwargs):
    obj = select(model).filter_by(**kwargs)
    result = await session.execute(obj)
    instance = result.scalar_one_or_none()

    if instance:
        return instance

    instance = model(**kwargs)
    session.add(instance)
    await session.commit()
    return instance


async def get_user_by_id(session, user_tg_id):
    return await session.scalar(select(User).where(User.tg_id == user_tg_id))

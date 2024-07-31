from typing import Optional

from database.db import async_session
from database.models import Goal
from utils.db_utils import get_user_by_id


async def set_year_goal(user_id: int, goal_name: str) -> Optional[Goal]:
    async with async_session() as session:
        user = await get_user_by_id(session, user_id)
        new_goal = Goal(user_id=user.id, title=goal_name)

        session.add(new_goal)
        await session.commit()
        await session.refresh(new_goal)

        return new_goal

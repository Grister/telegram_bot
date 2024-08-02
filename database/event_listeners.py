from sqlalchemy import event

from database.models import StatusEnum, MonthlyTask, WeeklyTask, DailyTask


# Event listeners to update progress and status
def update_goal_progress(mapper, connection, target):
    goal = target.goal
    if goal:
        total = len(goal.monthly_tasks)
        completed = len([task for task in goal.monthly_tasks if task.status == StatusEnum.COMPLETED])
        goal.progress = int((completed / total) * 100) if total > 0 else 0
        if goal.progress == 100:
            goal.status = StatusEnum.COMPLETED
        else:
            goal.status = StatusEnum.IN_PROGRESS if completed > 0 else StatusEnum.NOT_STARTED


def update_monthly_task_progress(mapper, connection, target):
    monthly_task = target.monthly_task
    if monthly_task:
        total = len(monthly_task.weekly_tasks)
        completed = len([task for task in monthly_task.weekly_tasks if task.status == StatusEnum.COMPLETED])
        monthly_task.progress = int((completed / total) * 100) if total > 0 else 0
        if monthly_task.progress == 100:
            monthly_task.status = StatusEnum.COMPLETED
        else:
            monthly_task.status = StatusEnum.IN_PROGRESS if completed > 0 else StatusEnum.NOT_STARTED


def update_weekly_task_progress(mapper, connection, target):
    weekly_task = target.weekly_task
    if weekly_task:
        total = len(weekly_task.daily_tasks)
        completed = len([task for task in weekly_task.daily_tasks if task.status == StatusEnum.COMPLETED])
        weekly_task.progress = int((completed / total) * 100) if total > 0 else 0
        if weekly_task.progress == 100:
            weekly_task.status = StatusEnum.COMPLETED
        else:
            weekly_task.status = StatusEnum.IN_PROGRESS if completed > 0 else StatusEnum.NOT_STARTED


event.listen(MonthlyTask, 'after_insert', update_goal_progress)
event.listen(MonthlyTask, 'after_update', update_goal_progress)
event.listen(WeeklyTask, 'after_insert', update_monthly_task_progress)
event.listen(WeeklyTask, 'after_update', update_monthly_task_progress)
event.listen(DailyTask, 'after_insert', update_weekly_task_progress)
event.listen(DailyTask, 'after_update', update_weekly_task_progress)

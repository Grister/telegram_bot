from datetime import datetime, timedelta
from typing import Optional, List

from sqlalchemy import String, ForeignKey, Text, DateTime, BigInteger, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs

import enum


class StatusEnum(enum.Enum):
    NOT_STARTED = 'Not Started'
    IN_PROGRESS = 'In Progress'
    COMPLETED = 'Completed'


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)
    username: Mapped[Optional[str]] = mapped_column(String(30))
    notes_tags: Mapped[List['Tag']] = relationship(
        argument='Tag',
        back_populates='user',
        lazy="selectin"
    )
    goals: Mapped[List['Goal']] = relationship(
        argument='Goal',
        back_populates='user',
        lazy="selectin"
    )


class Tag(Base):
    __tablename__ = 'tags'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(32))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped['User'] = relationship(
        argument='User',
        back_populates='notes_tags',
        lazy="selectin"
    )
    notes: Mapped[List['Note']] = relationship(
        argument='Note',
        back_populates='tag',
        lazy="selectin"
    )


class Note(Base):
    __tablename__ = 'notes'

    id: Mapped[int] = mapped_column(primary_key=True)
    tag_id: Mapped[int] = mapped_column(ForeignKey('tags.id'))
    tag: Mapped['Tag'] = relationship(
        argument='Tag',
        back_populates='notes',
        lazy="selectin"
    )
    content: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Goal(Base):
    __tablename__ = 'goals'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(32), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    status = mapped_column(Enum(StatusEnum), default=StatusEnum.NOT_STARTED)
    progress: Mapped[int] = mapped_column(default=0)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped['User'] = relationship(
        argument='User',
        back_populates='goals',
        lazy="selectin"
    )
    monthly_tasks = relationship(
        argument='MonthlyTask',
        back_populates='goal',
        cascade='all, delete-orphan'
    )

    def add_monthly_tasks(self, titles: list[str]):
        for i, title in enumerate(titles):
            monthly_task = MonthlyTask(
                title=title,
                goal=self,
                start_date=self.created_at + timedelta(days=30 * i)
            )
            self.monthly_tasks.append(monthly_task)


class MonthlyTask(Base):
    __tablename__ = 'monthly_tasks'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(32), nullable=False)
    goal_id: Mapped[int] = mapped_column(ForeignKey('goals.id'))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    start_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    status = mapped_column(Enum(StatusEnum), default=StatusEnum.NOT_STARTED)
    progress: Mapped[int] = mapped_column(default=0)

    goal = relationship(
        argument='Goal',
        back_populates='monthly_tasks'
    )
    weekly_tasks = relationship(
        argument='WeeklyTask',
        back_populates='monthly_task',
        cascade='all, delete-orphan'
    )

    def add_weekly_tasks(self, titles: list[str]):
        for i, title in enumerate(titles):
            weekly_task = WeeklyTask(
                title=title,
                monthly_task=self,
                start_date=self.start_date + timedelta(days=7 * i)
            )
            self.weekly_tasks.append(weekly_task)


class WeeklyTask(Base):
    __tablename__ = 'weekly_tasks'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(32), nullable=False)
    monthly_task_id: Mapped[int] = mapped_column(ForeignKey('monthly_tasks.id'))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    start_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    status = mapped_column(Enum(StatusEnum), default=StatusEnum.NOT_STARTED)
    progress: Mapped[int] = mapped_column(default=0)

    monthly_task = relationship(
        argument='MonthlyTask',
        back_populates='weekly_tasks'
    )
    daily_tasks = relationship(
        argument='DailyTask',
        back_populates='weekly_task',
        cascade='all, delete-orphan'
    )

    def add_daily_tasks(self, titles: list[str]):
        for i, title in enumerate(titles):
            daily_task = DailyTask(
                title=title,
                weekly_task=self,
                start_date=self.start_date + timedelta(days=i)
            )
            self.daily_tasks.append(daily_task)


class DailyTask(Base):
    __tablename__ = 'daily_tasks'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(32), nullable=False)
    weekly_task_id: Mapped[int] = mapped_column(ForeignKey('weekly_tasks.id'))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    start_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    status = mapped_column(Enum(StatusEnum), default=StatusEnum.NOT_STARTED)
    progress: Mapped[int] = mapped_column(default=0)

    weekly_task = relationship(
        argument='WeeklyTask',
        back_populates='daily_tasks'
    )

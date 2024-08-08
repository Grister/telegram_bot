import enum
from datetime import datetime
from typing import List, Optional

from sqlalchemy import BigInteger, DateTime, Enum, ForeignKey, String, Text
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class StatusEnum(enum.Enum):
    CANCELED = 'Canceled'
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
    tasks: Mapped[List['DailyTask']] = relationship(
        argument='DailyTask',
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


class DailyTask(Base):
    __tablename__ = 'daily_tasks'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(64), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped['User'] = relationship(
        argument='User',
        back_populates='tasks',
        lazy="selectin"
    )
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    status = mapped_column(Enum(StatusEnum), default=StatusEnum.IN_PROGRESS)

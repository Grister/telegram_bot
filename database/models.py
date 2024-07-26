from datetime import datetime
from typing import Optional, List

from sqlalchemy import String, ForeignKey, Text, DateTime, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs


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

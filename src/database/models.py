from datetime import datetime, timedelta, UTC
import uuid
from tracemalloc import Snapshot
from typing import List

from sqlalchemy import Column, String, DateTime, Index, func, UUID, Integer, ForeignKey
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, relationship


class Base(DeclarativeBase):
    pass

class Videos(Base):
    __tablename__ = 'videos'

    id: Mapped[uuid.UUID] = mapped_column(
        UUID,
        primary_key=True,
        default=uuid.uuid4
    )
    video_created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default="now()"
    )
    views_count: Mapped[int] = mapped_column(Integer,default=0)

    likes_count: Mapped[int] = mapped_column(Integer,default=0)

    reports_count: Mapped[int] = mapped_column(Integer,default=0)

    comments_count: Mapped[int] = mapped_column(Integer,default=0)

    creator_id: Mapped[str] = mapped_column(String(32),)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()

    )
    snapshots: Mapped[List["Snapshot"]] = relationship(
        back_populates="videos",
        cascade="all, delete-orphan",
        lazy="select"

    )

class Snapshots(Base):
    __tablename__ = 'snapshots'

    id: Mapped[str] = mapped_column(String(32), primary_key=True)

    video_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("videos.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    views_count: Mapped[int] = mapped_column(Integer, default=0)
    likes_count: Mapped[int] = mapped_column(Integer, default=0)
    reports_count: Mapped[int] = mapped_column(Integer, default=0)
    comments_count: Mapped[int] = mapped_column(Integer, default=0)

    delta_views_count: Mapped[int] = mapped_column(Integer, default=0)
    delta_likes_count: Mapped[int] = mapped_column(Integer, default=0)
    delta_reports_count: Mapped[int] = mapped_column(Integer, default=0)
    delta_comments_count: Mapped[int] = mapped_column(Integer, default=0)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )


    video: Mapped["Videos"] = relationship(back_populates="snapshots")
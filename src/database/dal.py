from uuid import UUID
from typing import Optional
from src.database.models import Videos, Snapshots
from src.exceptions import SqlRequestException
from src.database.session import async_session_maker
from sqlalchemy import text, func


class AnalyticsDAL:

    def __init__(self):
        self.session = async_session_maker()


    async def select_by_query(self, query: str) -> str | Exception:
        async with self.session as session:
            try:
                result = await session.execute(text(query))
                data = result.scalar_one_or_none()
                await session.commit()

                return data

            except Exception as e:
                await session.rollback()
                return e


    async def video_exists(self, video_id: str | UUID) -> bool | None:
        async with self.session as session:
            try:
                query = self.session.select(func.count()).select_from(Videos).where(Videos.id == video_id)
                result = await session.execute(query)
                return result.scalar() > 0
            except Exception as e:
                await session.rollback()


    async def get_video_by_id(self, video_id: str | UUID) -> Optional[Videos]:
        async with self.session as session:
            try:
                return await session.select(Videos).where(Videos.id == video_id).scalar_one()
            except Exception as e:
                await session.rollback()


    async def insert_video(self, video: Videos) -> None:
        async with self.session as session:
            try:
                session.add(video)
                await session.flush()
                await session.commit()
            except Exception as e:
                await session.rollback()


    async def snapshot_exists(self, snapshot_id: str | UUID) -> bool | None:
        async with self.session as session:
            try:
                query = self.session.select(func.count()).select_from(Snapshots).where(Snapshots.id == snapshot_id)
                result = await session.execute(query)
                return result.scalar() > 0
            except Exception as e:
                await session.rollback()


    async def get_snapshot_by_id(self, snapshot_id: str | UUID) -> Optional[Snapshots]:
        async with self.session as session:
            try:
                return await session.select(Videos).where(Snapshots.id == snapshot_id).scalar_one()
            except Exception as e:
                await session.rollback()


    async def insert_snapshot(self, snapshot: Snapshots) -> None:
        async with self.session as session:
            try:
                session.add(snapshot)
                await session.flush()
                await session.commit()
            except Exception as e:
                await session.rollback()
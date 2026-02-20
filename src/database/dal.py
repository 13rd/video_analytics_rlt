from src.exceptions import SqlRequestException
from src.database.session import async_session_maker
from sqlalchemy import text

class AnalyticsDAL:

    def __init__(self):
        self.session = async_session_maker()


    async def select_by_query(self, query: str) -> str | Exception:
        async with self.session() as session:
            try:
                result = await session.execute(text(query))
                data = result.scalar_one_or_none()
                await session.commit()

                return data

            except Exception as e:
                await session.rollback()
                return e
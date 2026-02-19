from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

import settings

engine = create_async_engine(settings.DATABASE_URL, echo=True, pool_pre_ping=True)


async_session_maker = async_sessionmaker(
    engine,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False
)


async def get_db_session() -> AsyncSession:
    """Возвращает сессию для использования вне DI (требуется ручное закрытие)."""
    return async_session_maker
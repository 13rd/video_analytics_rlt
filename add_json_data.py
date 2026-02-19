import asyncio
import json
import uuid
from datetime import datetime
from sqlalchemy import text, select, func
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.session import async_session_maker
from src.database.models import Videos, Snapshots


async def load_json_data(filepath: str) -> list:
    """Загружает данные из JSON файла."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


async def video_exists(session: AsyncSession, video_id: uuid.UUID) -> bool:
    """Проверяет, существует ли видео с таким ID."""
    query = select(func.count()).select_from(Videos).where(Videos.id == video_id)
    result = await session.execute(query)
    return result.scalar() > 0


async def import_video_data(session: AsyncSession, video_data: dict):
    """
    Импортирует одно видео и его снапшоты.
    Если видео существует — обновляет данные и добавляет новые снапшоты.
    """
    # 1. Подготовка данных для Видео
    video_id = uuid.UUID(video_data['id'])

    # Проверка на существование
    exists = await video_exists(session, video_id)

    if exists:
        # Обновление существующего видео
        video = (await session.execute(select(Videos).where(Videos.id == video_id))).scalar_one()
        video.views_count = video_data.get('views_count', 0)
        video.likes_count = video_data.get('likes_count', 0)
        video.reports_count = video_data.get('reports_count', 0)
        video.comments_count = video_data.get('comments_count', 0)
        video.updated_at = datetime.fromisoformat(video_data['updated_at'].replace('Z', '+00:00'))
    else:
        # Создание нового видео
        video = Videos(
            id=video_id,
            video_created_at=datetime.fromisoformat(video_data['video_created_at'].replace('Z', '+00:00')),
            views_count=video_data.get('views_count', 0),
            likes_count=video_data.get('likes_count', 0),
            reports_count=video_data.get('reports_count', 0),
            comments_count=video_data.get('comments_count', 0),
            creator_id=video_data['creator_id'],
            created_at=datetime.fromisoformat(video_data['created_at'].replace('Z', '+00:00')),
            updated_at=datetime.fromisoformat(video_data['updated_at'].replace('Z', '+00:00')),
        )
        session.add(video)
        # Коммит нужен, чтобы видео получило статус persistent перед добавлением снапшотов
        await session.flush()

    # 2. Обработка Снапшотов
    snapshots_data = video_data.get('snapshots', [])
    for snap_data in snapshots_data:
        snap_id = snap_data['id']

        # Проверка на дубликат снапшота
        exists_snap = await session.execute(
            select(func.count()).select_from(Snapshots).where(Snapshots.id == snap_id)
        )
        if exists_snap.scalar() > 0:
            continue

        snapshot = Snapshots(
            id=snap_id,
            video_id=video_id,
            views_count=snap_data.get('views_count', 0),
            likes_count=snap_data.get('likes_count', 0),
            reports_count=snap_data.get('reports_count', 0),
            comments_count=snap_data.get('comments_count', 0),
            delta_views_count=snap_data.get('delta_views_count', 0),
            delta_likes_count=snap_data.get('delta_likes_count', 0),
            delta_reports_count=snap_data.get('delta_reports_count', 0),
            delta_comments_count=snap_data.get('delta_comments_count', 0),
            created_at=datetime.fromisoformat(snap_data['created_at'].replace('Z', '+00:00')),
            updated_at=datetime.fromisoformat(
                snap_data.get('updated_at', snap_data['created_at']).replace('Z', '+00:00')),
        )
        session.add(snapshot)


async def main():
    print("🚀 Запуск импорта данных...")

    # Загрузка JSON
    data = await load_json_data('/home/nikita/Python/video_analytics_rlt/videos.json')
    data = data.get("videos")
    print(f"📄 Загружено {len(data)} записей из JSON.")

    success_count = 0

    # Используем контекстный менеджер для сессии
    async with async_session_maker() as session:
        try:
            for i, video_data in enumerate(data, 1):
                print(f"⏳ Обработка видео {i}/{len(data)}...")
                await import_video_data(session, video_data)
                success_count += 1

            # Финальный коммит всех изменений
            await session.commit()
            print(f"✅ Успешно импортировано {success_count} видео.")

        except Exception as e:
            # Откат при любой ошибке
            await session.rollback()
            print(f"❌ Ошибка импорта: {e}")
            raise
        finally:
            print("🏁 Импорт завершен.")


if __name__ == "__main__":
    asyncio.run(main())

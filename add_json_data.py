import asyncio
import json
import uuid
from datetime import datetime
from src.database.models import Videos, Snapshots
from src.database.dal import AnalyticsDAL


async def load_json_data(filepath: str) -> list:
    """Load data from JSON file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


async def import_video_data(video_data: dict):
    """
    Imports one video and its snapshots.
    If the video exists, it updates the data and adds new snapshots.
    """
    video_id = uuid.UUID(video_data['id'])

    exists = await AnalyticsDAL().video_exists(video_id)

    if exists:
        video = await AnalyticsDAL().get_video_by_id(video_id)
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
        await AnalyticsDAL().insert_video(video)

    snapshots_data = video_data.get('snapshots', [])
    for snap_data in snapshots_data:
        snap_id = snap_data['id']

        if await AnalyticsDAL().snapshot_exists(snap_id):
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
        await AnalyticsDAL().insert_snapshot(snapshot)


async def main():
    print("🚀 Запуск импорта данных...")

    data = await load_json_data('/home/nikita/Python/video_analytics_rlt/videos.json').get("videos")
    print(f"📄 Загружено {len(data)} записей из JSON.")

    success_count = 0

    try:
        for i, video_data in enumerate(data, 1):
            print(f"⏳ Обработка видео {i}/{len(data)}...")
            await import_video_data(video_data)
            success_count += 1

        print(f"✅ Успешно импортировано {success_count} видео.")

    except Exception as e:
        print(f"❌ Ошибка импорта: {e}")
        raise
    finally:
        print("🏁 Импорт завершен.")


if __name__ == "__main__":
    asyncio.run(main())

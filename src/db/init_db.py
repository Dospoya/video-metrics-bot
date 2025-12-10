import asyncio
import json
import pathlib
from datetime import datetime

import asyncpg

from src.db.conn import get_pool, init_pool

BASE_DIR = pathlib.Path(__file__).parent.parent

FILE_NAME = "videos.json"
FILE_PATH = BASE_DIR / FILE_NAME


def _mapping_video(item: dict) -> tuple[dict, list[dict]]:
    video = {
        "id": item["id"],
        "video_created_at": parse_ts(item["video_created_at"]),
        "views_count": item["views_count"],
        "likes_count": item["likes_count"],
        "reports_count": item["reports_count"],
        "comments_count": item["comments_count"],
        "creator_id": item["creator_id"],
        "created_at": parse_ts(item["created_at"]),
        "updated_at": parse_ts(item["updated_at"]),
    }
    snapshots = item.get("snapshots", [])
    return video, snapshots


def _mapping_snapshot(snapshot: dict) -> tuple:
    return (
        snapshot["id"],
        snapshot["video_id"],
        snapshot["views_count"],
        snapshot["likes_count"],
        snapshot["comments_count"],
        snapshot["reports_count"],
        snapshot["delta_views_count"],
        snapshot["delta_likes_count"],
        snapshot["delta_comments_count"],
        snapshot["delta_reports_count"],
        parse_ts(snapshot["created_at"]),
        parse_ts(snapshot["updated_at"]),
    )


async def save_video(video: dict, conn: asyncpg.pool.PoolConnectionProxy):
    await conn.execute(
        """
        INSERT INTO videos (
            id, video_created_at, views_count,
            likes_count, reports_count, comments_count,
            creator_id, created_at, updated_at
        ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
        """,
        video["id"],
        video["video_created_at"],
        video["views_count"],
        video["likes_count"],
        video["reports_count"],
        video["comments_count"],
        video["creator_id"],
        video["created_at"],
        video["updated_at"],
    )


async def save_snapshots_batch(
    snapshot_data: list[tuple], conn: asyncpg.pool.PoolConnectionProxy
):
    if not snapshot_data:
        return
    await conn.executemany(
        """
        INSERT INTO video_snapshots (
            id, video_id, views_count,
            likes_count, reports_count, comments_count,
            delta_views_count, delta_likes_count,
            delta_comments_count, delta_reports_count,
            created_at, updated_at
        ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12)
        """,
        snapshot_data,
    )


def parse_ts(ts) -> datetime:
    return datetime.fromisoformat(ts)


async def load_json(pool: asyncpg.Pool):
    total, inserted, skipped = 0, 0, 0
    with open(FILE_PATH, encoding="utf-8") as f:
        data = json.load(f)
        ary = data.get("videos")
        for item in ary:
            total += 1
            video, snapshots = _mapping_video(item)
            snapshot_data = []
            async with pool.acquire() as conn:
                try:
                    async with conn.transaction():
                        _ = await save_video(video, conn)
                        for snapshot in snapshots:
                            sh = _mapping_snapshot(snapshot)
                            snapshot_data.append(sh)
                        await save_snapshots_batch(snapshot_data, conn)
                        inserted += 1
                except Exception as e:
                    print(f"[ERROR] Video {video['id']} skipped: {e}")
                    skipped += 1
        return total, inserted, skipped


async def main():
    await init_pool()
    pool = get_pool()
    total, inserted, skipped = await load_json(pool)
    print(f"Total: {total}, Inserted: {inserted}, Skipped: {skipped}")


if __name__ == "__main__":
    asyncio.run(main())

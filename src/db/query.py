from datetime import datetime

import asyncpg

# «Сколько разных видео получали новые просмотры 27 ноября 2025?»


async def total_videos(pool: asyncpg.Pool) -> int:
    async with pool.acquire() as conn:
        return await conn.fetchval("SELECT COUNT(*) FROM videos")


async def creator_videos_in_period(
    pool: asyncpg.Pool, creator_id, start_date: datetime, end_date: datetime
) -> int:
    async with pool.acquire() as conn:
        return await conn.fetchval(
            """
            SELECT COUNT(*) FROM videos
            WHERE creator_id = $1 AND video_created_at::date BETWEEN $2 AND $3
            """,
            creator_id,
            start_date,
            end_date,
        )


async def videos_over_views(pool: asyncpg.Pool, views: int) -> int:
    async with pool.acquire() as conn:
        return await conn.fetchval(
            """
            SELECT COUNT(*) FROM videos
            WHERE views_count > $1
        """,
            views,
        )


async def views_growth_on_date(pool: asyncpg.Pool, dt: datetime) -> int:
    async with pool.acquire() as conn:
        return await conn.fetchval(
            """
            SELECT SUM(delta_views_count) FROM video_snapshot
            WHERE created_at::date = $1
        """,
            dt,
        )

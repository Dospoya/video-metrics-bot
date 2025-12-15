from datetime import date

import asyncpg


async def total_videos(pool: asyncpg.Pool) -> int:
    async with pool.acquire() as conn:
        return await conn.fetchval("SELECT COUNT(*) FROM videos")


async def creator_videos_in_period(
    pool: asyncpg.Pool, creator_id, start_date: date, end_date: date
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


async def views_growth_on_date(pool: asyncpg.Pool, on_date: date) -> int:
    async with pool.acquire() as conn:
        return await conn.fetchval(
            """
            SELECT SUM(delta_views_count) FROM video_snapshot
            WHERE created_at::date = $1
        """,
            on_date,
        )


async def videos_with_growth_on_date(pool: asyncpg.Pool, on_date: date) -> int:
    async with pool.acquire() as conn:
        return await conn.fetchval(
            """
            SELECT COUNT(distinct video_id) FROM video_snapshots
            WHERE created_at::date = $1
                and delta_views_count > 0
            """,
            on_date,
        )

import asyncpg

from src.db.query import (
    creator_videos_in_period,
    total_videos,
    videos_over_views,
    views_growth_on_date,
)
from src.schemas.intent import Query


async def execute_query(query: Query, pool: asyncpg.Pool):
    q = query.query
    match q.intent:
        case "total_videos":
            return await total_videos(pool)
        case "creator_videos_in_period":
            p = q.params
            return await creator_videos_in_period(
                pool, p.creator_id, p.start_date, p.end_date
            )
        case "videos_over_views":
            return await videos_over_views(pool, q.params.views)
        case "views_growth_on_date":
            return await views_growth_on_date(pool, q.params.on_date)

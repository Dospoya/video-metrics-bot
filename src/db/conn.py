import asyncpg

from src.config.config import settings

DATABASE_URL = settings.database_url

pool: None | asyncpg.Pool = None


async def init_pool():
    global pool
    if not DATABASE_URL:
        raise ValueError("DATABASE_URL is not set")
    pool = await asyncpg.create_pool(DATABASE_URL)


def get_pool() -> asyncpg.Pool:
    if not pool:
        raise RuntimeError("Pool not initialized")
    return pool

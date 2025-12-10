import os

import asyncpg
from dotenv import load_dotenv

_ = load_dotenv(".env")

DATABASE_URL = os.getenv("DATABASE_URL", "")

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

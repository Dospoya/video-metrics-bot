import asyncpg
from aiogram import Bot, Dispatcher

from src.bot.routers import main_router
from src.bot.utils import set_commands
from src.config.config import settings

bot = Bot(token=settings.bot_token)
dp = Dispatcher()
dp.include_router(main_router)


async def main():
    pool = await asyncpg.create_pool(dsn=settings.database_url)
    dp["pool"] = pool
    try:
        await set_commands(bot)
        await dp.start_polling(bot)
    finally:
        await pool.close()

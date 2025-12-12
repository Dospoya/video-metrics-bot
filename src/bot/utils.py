from aiogram import Bot
from aiogram.types import BotCommand


async def set_commands(bot: Bot):
    _ = await bot.set_my_commands(
        [BotCommand(command="start", description="Start the bot")]
    )

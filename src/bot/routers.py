from aiogram import Router
from aiogram.filters import Command

from src.bot.handlers import router as handlers_router
from src.bot.handlers import start

main_router = Router()
main_router.message.register(start, Command(commands=["start"]))
main_router.include_router(handlers_router)

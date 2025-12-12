import asyncpg
from aiogram import F, Router, types
from aiogram.filters import Command

from src.service.executor import execute_query
from src.service.query_interpreter import converter

router = Router()


async def start(message: types.Message):
    _ = await message.answer("Введите ваш вопрос")


@router.message(F.text, ~Command(commands=["start"]))
async def handle_question(message: types.Message, pool: asyncpg.Pool):
    try:
        query = converter(message.text)
    except Exception as e:
        _ = await message.answer(f"Неподдерживаемый запрос. {repr(e)}")
    else:
        result = await execute_query(query, pool)
        _ = await message.answer(str(result))

import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from settings import BOT_TOKEN
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from src.services.llm.llm_service import get_sql_request
from src.database.dal import AnalyticsDAL

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer(
        text="Введите свой запрос по аналитике видео."
    )

@dp.message()
async def user_request(message: types.Message):
    if not message.text or message.text.startswith('/'):
        return

    query_text = await get_sql_request(user_request=message.text)
    print(query_text)
    query: str = query_text

    data = await AnalyticsDAL().select_by_query(query=query)

    await message.answer(text=str(data))


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
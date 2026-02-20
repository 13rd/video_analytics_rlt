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
    """
    Start the bot.
    :param message:
    :return:
    """
    await message.answer(
        text="Введите свой запрос по аналитике видео."
    )

@dp.message()
async def user_request(message: types.Message):
    """
    Get user request and return aggregated data of bot error
    :param message:
    :return:
    """
    if not message.text or message.text.startswith('/'):
        return

    query_text = await get_sql_request(user_request=message.text)
    print(query_text)
    query: str = query_text

    try:
        data = await AnalyticsDAL().select_by_query(query=query)

        await message.answer(text=str(data))
    except Exception as e:
        print(e)


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
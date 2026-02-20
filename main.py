from src.services.llm.llm_service import get_sql_request
import asyncio
from dotenv import load_dotenv

load_dotenv()

async def main():
    print("Hello from video-analytics-rlt!")
    user_request = ("сколько видео набрало более двадцати тысяч лайков")
    result = await get_sql_request(user_request)
    print(result)


if __name__ == "__main__":
    asyncio.run(main())

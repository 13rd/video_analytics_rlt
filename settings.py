from envparse import Env
from dotenv import load_dotenv

load_dotenv()
env = Env()

DATABASE_URL = env.str(
    "DATABASE_URL",
    default="postgresql+asyncpg://postgres:postgres@0.0.0.0:5432/postgres"
)

BOT_TOKEN = env.str("BOT_TOKEN")

LLM_API_KEY=env.str("LLM_API_KEY")
LLM_MODEL=env.str("LLM_MODEL", default="deepseek/deepseek-r1-0528:free")
SITE_URL=env.str("SITE_URL", default="http://localhost:8000")
SITE_NAME=env.str("SITE_NAME", default="Local SQL Bot")
from os import getenv
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from typing import List, Optional

load_dotenv()

TOKEN = getenv("TOKEN")

env_admins_ID = getenv("admins")
IDS: List[int] = [int(id) for id in (env_admins_ID or "").split(",") if id.strip()]

bot = Bot(token=TOKEN)
dp = Dispatcher()
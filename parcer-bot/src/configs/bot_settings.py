import datetime
from os import getenv
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from typing import List

load_dotenv()

TOKEN = getenv("TOKEN")

env_admins_ID = getenv("admins")
IDS: List[int] = [int(id) for id in (env_admins_ID or "").split(",") if id.strip()]

bot = Bot(token=TOKEN)
dp = Dispatcher()

year = datetime.date.today().year

group_name = 'кб-103'
semester = '1'
semester_part = '1'

url = f'https://student{year}.lpnu.ua/students_schedule?studygroup_abbrname={group_name}&semestr={semester}&semestrduration={semester_part}'

text: list[str] = []

day_pairs: dict[str, list[str]] = {
    'Пн': [],
    'Вт': [],
    'Ср': [],
    'Чт': [],
    'Пт': [],
    'Сб': [],
    'Нд': []
}

search_ids: list[str] =["group_full", "sub_1_chys", "sub_2_chys"
                        "sub_2_znam", "sub_1_znam", "sub_1_full","igroup_chys", "group_znam" ] 

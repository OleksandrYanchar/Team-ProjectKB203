import re
from aiogram import F
from aiogram.types import Message
from src.parser.schedule_parcer import Schedule
from src.configs.bot_settings import dp, bot, url, text, day_pairs
from src.configs.bot_answers import greet_text
from src.bot.kbs import main_kb

parser = Schedule(day_pairs=day_pairs, url=url, text=text)

@dp.message(F.text == '/start')
async def get_group_info(message: Message):
    await message.answer(greet_text, reply_markup=main_kb)


@dp.message(F.text == '/schedule')
async def parse(message: Message): 
    await message.answer(url) 
    parser.get_schedule() 


# main function to start polling bot
async def bot_main():
    await dp.start_polling(bot, skip_updates=True)

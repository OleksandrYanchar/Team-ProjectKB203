import re
from aiogram import F, Router
from aiogram.types import Message
from src.parser.schedule_parcer import Schedule
from src.configs.bot_settings import dp, bot,  text, day_pairs, search_ids, year
from src.configs.bot_answers import greet_text
from src.bot.kbs import main_kb

get_group = False

url = ''
user_urls= {}


@dp.message(F.text == '/start')
async def cmd_start(message: Message):
    user_id = message.from_user.id
    url = user_urls.get(user_id)
    await message.answer(greet_text, reply_markup=main_kb)
    if url is not None:
        try:
            await message.answer(f'Ваш поточний юрл: {url}')
        except Exception as e:
            await message.answer(str(e))
    else:
        await message.answer("ви не вказали юрл")


@dp.message(F.text == '/info')
async def send_group_info(message: Message):
    user_id = message.from_user.id
    url = user_urls.get(user_id)
    if url is not None:
        try:
            await message.answer(f'Ваш поточний юрл: {url}')
        except Exception as e:
            await message.answer(str(e))
    else:
        await message.answer("ви не вказали юрл")  
    await message.answer(f'/selectGroup  за допомогою цієї команди ви можете встановити групу розклад якої будете шкати \n'
                         f'/schedule ця комнада починає парсинг сайту та виводить розкда для встановленої групи\n'
                         f'/dict відправляє словник який створює парсер')               

@dp.message(F.text == '/schedule')
async def parse(message: Message):
    try:
        user_id = message.from_user.id
        url = user_urls[user_id]
        await message.answer(url)  # Print the current URL
        parser = Schedule(day_pairs=day_pairs, url=url, search_ids=search_ids, text=text)
        parser.get_schedule(url)
    
        formatted_schedule= ''
        for day, lessons in day_pairs.items():
            if lessons:
                formatted_schedule = f"*{day}*\n\n"
                for lesson in lessons:
                    formatted_schedule += f"{lesson.strip()}\n\n"
                if     formatted_schedule== '':
                    await message.answer('Невдалося дістати розклад')
                else:
                    await message.answer(formatted_schedule)
        formatted_schedule= ''
    except Exception:
        await message.answer(f'Невдалося дістати розклад\n')

@dp.message(F.text == '/dict')
async def get_lessons_dict(message: Message):
    try:
        user_id = message.from_user.id
        url = user_urls[user_id]
        await message.answer(url)  # Print the current URL
        parser = Schedule(day_pairs=day_pairs, url=url, search_ids=search_ids, text=text)
        parser.get_schedule(url)
        
        # Split the dictionary into smaller chunks
        chunk_size = 4096  # Maximum message length supported by Telegram
        day_pairs_str = str(day_pairs)

        for i in range(0, len(day_pairs_str), chunk_size):
            chunk = day_pairs_str[i:i + chunk_size]
            await message.answer(chunk)
    except Exception:
        await message.answer('An error occurred while sending the dictionary.')

    



@dp.message(F.text == '/selectGroup')
async def parse(message: Message):
    global get_group 
    get_group = True
    await message.answer('Відправте номер групи семестр та яка частина\n Наприклад(кб-203 1 1)\n а після цього /schedule щоб отримати розклад\n'
                         f' 1 - цілий семестр \n'
                           f' 2 - перша частина \n'
                            f'3 - друга частина\n')
    
@dp.message(F.text == '🦽Звязок з авторами')
async def send_url(message: Message):
    await message.answer('https://github.com/OleksandrYanchar')

@dp.message()
async def get_group(message: Message):
    global url, get_group, parser
    pattern = r"(\S+) (\d+) (\d+)"
    input_string = message.text
    match = re.search(pattern, input_string)
    
    if get_group:
        if match:
            group_name = match.group(1)
            semester = match.group(2)
            semester_part = match.group(3)
            user_id = message.from_user.id
            user_urls[user_id] = f'https://student{year}.lpnu.ua/students_schedule?studygroup_abbrname={group_name}&semestr={semester}&semestrduration={semester_part}'
            get_group = False
            await message.answer(f"ваша група: {group_name} семестр:{semester} частина семестру: {semester_part}")

        else:
            await message.answer("Помилка: не вдалося знайти всі значення")
   
        
# main function to start polling bot
async def bot_main():
    await dp.start_polling(bot, skip_updates=True)
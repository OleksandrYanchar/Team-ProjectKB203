from aiogram import executor
from configs.bot_settings import dp, bot





# main function to start poling bot
async def bot_main():
    await dp.start_polling(bot, skip_updates=True)
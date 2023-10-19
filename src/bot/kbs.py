from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

main_kb = ReplyKeyboardMarkup(keyboard=[
        [
            KeyboardButton(text='👨‍🎓⛓️ Розклад занять'),
            KeyboardButton(text='🦽Звязок з авторами'),
                        KeyboardButton(text='/start'),
                                    KeyboardButton(text='/selectGroup'),
                                    KeyboardButton(text='/schedule')


        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder='Виберіть дію',
    selective=True

)

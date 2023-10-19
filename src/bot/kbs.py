from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from src.configs.settings import half_group

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
def select_group(update, context):
    chat_id = update.effective_chat.id
    group_select = InlineKeyboardMarkup()

    button1 = InlineKeyboardButton(text='| група', callback_data='group1')
    button2 = InlineKeyboardButton(text='|| група', callback_data='group1')
    


    group_select.row(button1, button2)

    context.bot.send_message(chat_id, text="Оберіть групу:", reply_markup=group_select)

    context.user_data['half_group'] = half_group

    return half_group
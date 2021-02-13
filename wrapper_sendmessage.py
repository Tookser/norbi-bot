from telebot import types
import telebot

import baseconfig

def create_keyboard(labels):
    ''' создаёт клавиатуру из непустого набора меток'''
    # keyboard = types.InlineKeyboardMarkup(one_time_keyboard=True)
    # assert labels is not None
    if not labels:
        keyboard = types.ReplyKeyboardRemove()
    else:
        keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        for label in labels:
            key = types.KeyboardButton(text=label)
            keyboard.add(key)

    return keyboard

def send_message(user, message, keyboard=None):
    '''посылает поддерживающее сообщение. по умолчанию с кнопками
    можно и без
    Возвращение сообщения нужно для дальнейшей работки'''

    if keyboard is None:
        keyboard = types.ReplyKeyboardRemove()

    print(f'''{"Bot to " + str(user):>20}: {message}''')
    return baseconfig.bot.send_message(user, message, reply_markup=keyboard)

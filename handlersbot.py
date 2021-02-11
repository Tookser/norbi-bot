
import os
import shelve
from os.path import join
from random import choice
import shutil
from functools import wraps

from telebot import types
import telebot

import baseconfig
from baseconfig import *
from load import *
import userdblib
from userdblib import UserState
import admin
from textprocess import *
from stepics import CBTTest, Step


def get_phrase(userdb, id, lst_of_phrases):
    all_phrases = set(lst_of_phrases)
    user = userdb.setdefault(str(id), userdblib.get_empty_shelve_value())
    forbidden_phrases = set(user['forbidden_phrases'])

    possible_phrases = all_phrases - forbidden_phrases
    msg = choice(list(possible_phrases))

    # так как модификация значения
    # не воспринимается shelve как присваивание

    user['forbidden_phrases'].add(msg)
    userdb[str(id)] = user

    return msg

def create_keyboard_with_helping_buttons():
    ''' создаёт клавиатуру '''
    # keyboard = types.InlineKeyboardMarkup(one_time_keyboard=True)
    keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    for button_text in phrases_by_type:
        text = button_text
        key = types.KeyboardButton(text=button_text)
        keyboard.add(key)

    return keyboard

def send_support_message(user, message, keyboard=True):
    '''посылает поддерживающее сообщение. по умолчанию с кнопками
    можно и без
    Возвращение сообщения нужно для дальнейшей работки'''

    if keyboard:
        keyboard = create_keyboard_with_helping_buttons()
    else:
        keyboard = types.ReplyKeyboardRemove()

    print(f'''{"Bot to " + str(user):>20}: {message}''')
    return bot.send_message(user, message, reply_markup=keyboard)


@bot.message_handler(commands=['setname'])
@bot.message_handler(func = lambda message: is_set_name(message.text))
def read_name(message):
    '''предлагает установить имя'''
    id = message.from_user.id
    msg = send_support_message(id, \
                            'Введите имя, по которому к вам стоит обращаться.',
                            keyboard=False)
    bot.register_next_step_handler(msg, has_read_name)

def interrupt_if_request(func):
    '''декоратор.
    возвращает функцию,
    которая обрабатывает request_handler,
    если мы были на полшаге'''

    @wraps(func)
    def result_func(message):#, *args, **kwargs):
        if is_request(message.text):
            request_handler(message)
        else:
            func(message) #, *args, **kwargs)

    return result_func


@interrupt_if_request
def has_read_name(message):
    '''следующий шаг после read_name
    устанавливает имя пользователя если всё хорошо'''

    name = message.text.strip()
    id = message.from_user.id

    if is_name_ok(name):
        with shelve.open(baseconfig.USERDB_FILENAME) as userdb:
            if str(id) not in userdb:
                userdb[str(id)] = userdblib.get_empty_shelve_value()
            db_record = userdb[str(id)]
            db_record['name'] = name
            userdb[str(id)] = db_record
            send_support_message(id, f'Ваше имя установлено, {name}')
    else:
        send_support_message(id, '__Это__ имя неприемлемо :(')

@bot.message_handler(content_types=['text'],
                     func=lambda message: is_request(message.text))
def request_handler(message):
    '''обработка запроса (на ругань, например)'''
    id = message.from_user.id
    text = message.text
    user = message.from_user

    try:
        with shelve.open(baseconfig.USERDB_FILENAME) as userdb:
            bot_msg_text = \
                get_phrase(userdb, id, phrases_by_type[text].lst)

    except IndexError:
        bot_msg_text = "В данный момент для вас нет сообщений"

    msg = send_support_message(id, bot_msg_text)

    # эти полторы строки - для прерывания потока сообщений
    # bot.register_next_step_handler(msg, after_first_message, \
                                   # bot_msg_text, id)

@bot.message_handler(content_types=['text'],
                     func=lambda message: is_start_message(message.text))
def hello_handler(message):
    '''обработка приветствия'''
    id = message.from_user.id
    text = message.text
    user = message.from_user

    print(f'''{id:>20}: {text}''')

    db_record = None
    with shelve.open(baseconfig.USERDB_FILENAME) as userdb:
        if str(id) not in userdb:
            userdb[str(id)] = userdblib.get_empty_shelve_value()
        db_record = userdb[str(id)]

    # with shelve.open(baseconfig.USERDB_FILENAME) as userdb:
        name = None
        if str(id) in userdb:
            name = userdb[str(id)]['name']

        if name is None:
            try:
                name = user.first_name + user.last_name
            except TypeError:
                name = "Неуловимый"

        send_support_message(id, f"Приветствую, {name}! \nЧем могу помочь?")




ExampleTest = CBTTest(keyword='test',
                           name='Test',
                           steps=[Step('Привет из будующего!'),
                                  Step('Как ты себя чувствуешь?'),
                                  Step('*незначащий вопрос*')],
                   process_function=lambda l: f'''Вы здороваетесь так: "{l[0]}", а чувствуете себя так:{l[1]}'''
                            )


def after_first_message(message, bot_msg_text, user_id):
    '''после посылки первого сообщения
    сейчас не используется, но может потом понадобиться'''
    send_support_message(user_id,
                         "Я же уже говорил, " + bot_msg_text.lower())

@bot.message_handler(content_types=['text'])
def unknown_handler(message):
    '''если сообщение непонятное'''
    id = message.from_user.id
    text = message.text
    user = message.from_user

    send_support_message(id, "Я вас не понимаю.")


def main():
    # REMOVE 2 strings BEFORE PRODUCTION
    admin.clean_db()
    shutil.rmtree('.handler-saves/', ignore_errors=True)

    # словарь настроек
    global config
    config = baseconfig.config

    # словарь объектов PhrasesList
    global phrases_by_type
    phrases_by_type = load_phrases()

    # для поддержки добавления хэндлеров
    # bot.enable_save_next_step_handlers(delay=2)
    # bot.load_next_step_handlers()

    # bot.polling()

main()

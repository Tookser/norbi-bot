#!/usr/bin/python3

import os
import shelve
from os.path import join
from random import choice
import shutil

from telebot import types
import telebot

import baseconfig
from load import *
import userdblib
from userdblib import UserState
import admin
from textprocess import is_start_message

bot = telebot.TeleBot(get_token());

def get_phrase(userdb, id, lst_of_phrases):
    all_phrases = set(lst_of_phrases)
    forbidden_phrases = set(userdb[str(id)]['forbidden_phrases'])

    possible_phrases = all_phrases- forbidden_phrases
    msg = choice(list(possible_phrases))

    # так как модификация значения
    # не воспринимается shelve как присваивание
    record = userdb[str(id)]
    record['forbidden_phrases'].add(msg)
    userdb[str(id)] = record

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

def send_support_message(user, message, with_keyboard=True):
    '''посылает поддерживающее сообщение. по умолчанию с кнопками
    можно и без
    Возвращение сообщения нужно для дальнейшей работки'''

    if with_keyboard:
        keyboard = create_keyboard_with_helping_buttons()
    else:
        keyboard = None

    print(f'''{"Bot to " + str(user):>20}: {message}''')
    return bot.send_message(user, message, reply_markup=keyboard)

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    '''выдаёт сообщение на приветствие'''
    id = message.from_user.id
    text = message.text
    user = message.from_user

    print(f'''{id:>20}: {text}''')

    # print(type(id))
    with shelve.open(baseconfig.USERDB_FILENAME) as userdb:
        if str(id) not in userdb:
            userdb[str(id)] = userdblib.get_empty_shelve_value()


    if text in phrases_by_type:
        try:
            with shelve.open(baseconfig.USERDB_FILENAME) as userdb:
                bot_msg_text = \
                    get_phrase(userdb, id, phrases_by_type[text].lst)

        except IndexError:
            bot_msg_text = "В данный момент для вас нет сообщений"

        msg = send_support_message(id, bot_msg_text)
        bot.register_next_step_handler(msg, after_first_message, \
                                       bot_msg_text, id)

    elif is_start_message(text):
        send_support_message(id, f"Приветствую, \
{user.first_name + user.last_name}! \n\
Чем могу помочь?")
    else:
        send_support_message(id, "Я вас не понимаю.")
    # print(id, text)

def after_first_message(message, bot_msg_text, user_id):
    '''после посылки первого сообщения'''
    send_support_message(user_id,
                         "Я же уже говорил, " + bot_msg_text.lower())

# @bot.callback_query_handler(func=lambda call: True)
# def callback_worker(call):
#     '''обрабатывает нажатия на кнопочки'''
#     if call.data in messages_by_type:
#         print(call.data)
#         msg = choice(messages_by_type[call.data])
#         send_support_message(call.message.chat.id, msg)

def main():
    # REMOVE BEFORE PRODUCTION
    admin.clean_db()
    shutil.rmtree('.handler-saves/', ignore_errors=True)

    # словарь настроек
    global config
    config = baseconfig.config

    # словарь объектов PhrasesList
    global phrases_by_type
    phrases_by_type = load_phrases()

    # для поддержки добавления хэндлеров
    bot.enable_save_next_step_handlers(delay=2)
    bot.load_next_step_handlers()

    bot.polling()

if __name__ == '__main__':
    main()

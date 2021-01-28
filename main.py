#!/usr/bin/python3

import os
from os.path import join
from random import choice

from telebot import types
import telebot

import baseconfig
from load import *


bot = telebot.TeleBot(get_token());


def create_keyboard_with_helping_buttons():
    ''' создаёт клавиатуру '''
    # keyboard = types.InlineKeyboardMarkup(one_time_keyboard=True)
    keyboard = types.InlineKeyboardMarkup()
    for name in config['keyboard']:
        text = config['keyboard'][name]
        key = types.InlineKeyboardButton(text=text,  callback_data=name)
        keyboard.add(key)

    return keyboard

def send_support_message(user, message, with_keyboard=True):
    '''посылает поддерживающее сообщение. по умолчанию с кнопками
    можно и без'''

    if with_keyboard:
        keyboard = create_keyboard_with_helping_buttons()
    else:
        keyboard = None

    bot.send_message(user, message, reply_markup=keyboard)

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    '''выдаёт сообщение на приветствие'''
    print(message.from_user.id, message.text)
    send_support_message(message.from_user.id,
                         "Привет! Я могу тебе помочь.")

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    '''обрабатывает нажатия на кнопочки'''
    if call.data in messages_by_type:
        print(call.data)
        msg = choice(messages_by_type[call.data])
        send_support_message(call.message.chat.id, msg)


def main():
    global config
    config = load_config()
    global messages_by_type
    messages_by_type = load_data()

    bot.polling()

if __name__ == '__main__':
    main()

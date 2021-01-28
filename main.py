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
    keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    for button_text in phrases_by_type:
        text = button_text
        key = types.KeyboardButton(text=button_text)
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
    id = message.from_user.id
    text = message.text

    print(text)
    if text in phrases_by_type:
        msg = choice(phrases_by_type[text].lst)
        send_support_message(id, msg)
    else:
        send_support_message(id, "Приветствую! Чем могу помочь?")
    print(id, text)

# @bot.callback_query_handler(func=lambda call: True)
# def callback_worker(call):
#     '''обрабатывает нажатия на кнопочки'''
#     if call.data in messages_by_type:
#         print(call.data)
#         msg = choice(messages_by_type[call.data])
#         send_support_message(call.message.chat.id, msg)

def main():
    # словарь настроек
    global config
    config = baseconfig.config

    # словарь объектов PhrasesList
    global phrases_by_type
    phrases_by_type = load_phrases()


    bot.polling()

if __name__ == '__main__':
    main()

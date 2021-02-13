from os.path import join
import os
import configparser
from collections import OrderedDict
from functools import lru_cache

import telebot

cache = lru_cache(maxsize=None)


BOT_ENABLE = True # True если токен есть

DATA_DIRECTORY = 'data' # директория с информацией и настройками
CONFIG_FILENAME = join(DATA_DIRECTORY, 'config.ini')
PRIVATE_CONFIG_FILENAME = join(DATA_DIRECTORY, 'config_private.ini')

USERDB_FILENAME = join(DATA_DIRECTORY, 'userdb.db')
PHRASES_DIRNAME = join(DATA_DIRECTORY, 'messages_for_users_by_type')
TESTS_DIRNAME = join(DATA_DIRECTORY, 'cbt_tests')

class PhrasesList:
    def __init__(self, lst, filename='BLANK', button_text='---'):
        self.lst = lst
        self.filename = filename # без .txt
        self.button_text = button_text

@cache
def load_config():
    '''загружает из файла конфигурации'''
      # импортируем библиотеку
    config = configparser.ConfigParser()
    config.read(CONFIG_FILENAME)

    return config

config = load_config()

@cache
def get_token():
    '''возвращает токен, сам токен'''
    config = configparser.ConfigParser()
    config.read(PRIVATE_CONFIG_FILENAME)

    return config['token']['token']

bot = telebot.TeleBot(get_token());

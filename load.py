'''функции для загрузки всяких данных'''

import os
import configparser
from collections import OrderedDict
from functools import lru_cache
cache = lru_cache(maxsize=None)

from baseconfig import *



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

def load_list_from_file(file):
    # загружат список сообщений из файла
    result = []
    for line in file:
        line = line.strip()
        # одинарный хештег не подходит как символ комментария
        # т.к. мб сообщения с хештегами
        if not line.startswith('//') and bool(line):
            result.append(line)
    return result

@cache
def load_phrases():
    ''' загружает все типы сообщения (PhrasesList) в УПОРЯДОЧЕННЫЙ словарь
    возвращает этот словарь'''

    def get_name_of_list(filename):
        # возвращает имя файла без расширения
        return filename.split('.')[0]

    phrases = []
    dir_name = 'data/messages_for_users_by_type/'
    for file in os.listdir(dir_name):
        with open(join(dir_name, file)) as f:
            key = get_name_of_list(file)
            phrases.append(PhrasesList(load_list_from_file(f),
                            filename=key,
                            button_text=config['keyboard'][key]))


    # print(messages_by_type)
    phrases_by_filename = {phrase.filename:phrase
                                        for phrase
                                        in phrases}
    phrases_by_button_text = OrderedDict()

    for filename in config['keyboard']:
        current = phrases_by_filename[filename]
        phrases_by_button_text[current.button_text] = current

    return phrases_by_button_text


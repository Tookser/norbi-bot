'''функции для загрузки всяких данных'''

import os
import configparser

from baseconfig import *

def load_config():
    '''загружает из файла конфигурации'''
      # импортируем библиотеку
    config = configparser.ConfigParser()
    config.read(CONFIG_FILENAME)

    return config

def get_token():
    '''возвращает токен, сам токен'''
    config = configparser.ConfigParser()
    config.read(PRIVATE_CONFIG_FILENAME)

    return config['token']['token']

def load_list_from_file(file):
    # загружат список сообщений из файла
    result = []
    for line in file:
        # одинарный хештег не подходит как символ комментария
        # т.к. мб сообщения с хештегами
        if not line.startswith('//') and bool(line):
            result.append(line.strip())
    return result

def load_data():
    # загружает все типы сообщения в словарь
    # возвращает этот словарь

    def get_name_of_list(filename):
        # возвращает имя файла без расширения
        return filename.split('.')[0]

    messages_by_type = {}
    dir_name = 'data/messages_for_users_by_type/'
    for file in os.listdir(dir_name):
        with open(join(dir_name, file)) as f:
            key = get_name_of_list(file)
            messages_by_type[key] = load_list_from_file(f)

    # print(messages_by_type)
    return messages_by_type

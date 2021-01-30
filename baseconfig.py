from os.path import join

BOT_ENABLE = True # True если токен есть

DATA_DIRECTORY = 'data' # директория с информацией и настройками
CONFIG_FILENAME = join(DATA_DIRECTORY, 'config.ini')
PRIVATE_CONFIG_FILENAME = join(DATA_DIRECTORY, 'config_private.ini')

USERDB_FILENAME = join(DATA_DIRECTORY, 'userdb.db')
PHRASES_DIRNAME = join(DATA_DIRECTORY, 'messages_for_users_by_type')

import load

config = load.load_config()

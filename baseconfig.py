from os.path import join



DATA_DIRECTORY = 'data' # директория с информацией и настройками
CONFIG_FILENAME = join(DATA_DIRECTORY, 'config.ini')
PRIVATE_CONFIG_FILENAME = join(DATA_DIRECTORY, 'config_private.ini')
USERDB_FILENAME = join(DATA_DIRECTORY, 'userdb.db')

import load

config = load.load_config()

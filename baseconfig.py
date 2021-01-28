from os.path import join



DATA_DIRECTORY = 'data' # директория с информацией и настройками
CONFIG_FILENAME = join(DATA_DIRECTORY, 'config.ini')
PRIVATE_CONFIG_FILENAME = join(DATA_DIRECTORY, 'config_private.ini')

import load

config = load.load_config()

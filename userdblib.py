import time
import shelve

import baseconfig

class UserState:
    '''состояние пользователя - в какой он позиции в чате он сейчас
    name - имя состояния
    current_time - когда в него попал (нужно, чтобы сбрасывать неактивные сессии)'''
    def __init__(self, name='start', current_time=None):
        self.name = name

        if current_time is None:
            current_time = time.time()
        self.time = current_time

    def update_state(self, name):
        self.name = name
        self.time = time.time()

    def __repr__(self):
        return f'''{self.__class__.__name__}({self.name}, {self.time})'''


def get_empty_shelve_value():
    '''возвращает пустую запись базы данных
    name == None <==> когда обращаться по имени из профиля'''
    return {'state':UserState(),
            'forbidden_phrases':set(),
            'name':None,
            'step':0,}

class UserDB:
    '''key-value хранилище, по str(id) хранит инфу о пользователе'''
    # __obj = None
    # def __new__(cls, *args):
    #     '''только одна DB'''
    #     if cls.__obj is None:
    #         cls.__obj = super().__new__(cls, *args)
    #     return cls.__obj

    def __init__(self, file_name):
        self._file_name = file_name


    def __getitem__(self, id):
        '''возвращает запись о человеке
        id мб числом - превращается в строку всё равно'''
        with shelve.open(self._file_name) as userdb:
            if str(id) not in userdb:
                userdb[str(id)] = get_empty_shelve_value()
            db_record = userdb[str(id)]
            # db_record = name
            return db_record


    def __setitem__(self, id, value):
        '''устанавливает значение записи пользователя'''
        with shelve.open(self._file_name) as userdb:
            userdb[str(id)] = value


db = UserDB(baseconfig.USERDB_FILENAME)

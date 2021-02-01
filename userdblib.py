import time

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
            'name':None}

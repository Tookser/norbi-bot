'''здесь будут храниться тесты (шкала Бека/Альтмана), процедуры КПТ и прочее'''
from abc import ABC, abstractmethod
import configparser
from collections import namedtuple

import userdblib
import handlersbot as hb
import baseconfig
from wrapper_sendmessage import *

bot = baseconfig.bot
db = userdblib.db

all_handlers = []

class CBTTest:
    # для хранения в глобальной области хендлеров
    number_of_handler = 0
    handler_prefix = 'cbtest_handler'

    def __init__(self, *, name='Test', keyword='test', steps=None,
                 process_function=None):
        '''объекты этого класса - тесты
        name - имя в базе данных, дб уникально
        keyword - команда для входа в тест, типа beck (если команда /beck)
        steps - шаги - объекты класса Step
        process_function - функция, выдающая результат по списку из бд
        '''
        # config = configparser.ConfigParser()
        # config.read(config_file_name)
        # self._process(config)
        assert steps is not None
        assert process_function is not None

        self._bot = hb.bot
        self._name = name
        self._process_function = process_function

        first_step = steps[0]
        other_steps = steps[1:]

        # перевёрнутый список хендлеров
        self._handlers_reversed_list = []

        self._last_handler = self._create_last_handler()

        for step in reversed(other_steps):
            self._handlers_reversed_list.append(self._create_middle_handler(step))

        self._first_handler = self._create_first_handler(first_step, keyword)

        self._handlers_reversed_list = \
            [self._last_handler] + \
             self._handlers_reversed_list + \
            [self._first_handler]

        self._handlers_list = self._handlers_reversed_list[::-1]

    @staticmethod
    def _get_next_handler(self, handler):
        '''DEPRECATED'''
        raise NotImplementedError
        i = self._handlers_reversed_list.find(handler) - 1
        return i


    def _next_handler(self, id):
        '''обращается к БД чтобы определить, на каком ты сейчас шаге'''
        return self._handlers_list[db[id]['step']]


    @property
    def _last_existing_handler(self):
        '''возвращает последний уже созданный хендлер, он же первый в тесте'''

        if self._handlers_reversed_list:
            print('first branch')
            print(self._handlers_reversed_list)
            return self._handlers_reversed_list[-1]
        else:
            print('second branch')
            return self._last_handler

    def _create_first_handler(self, step, keyword):
        '''создаёт первый хендлер - который будет работать всегда
        по команде типа /beck'''


        #TODO вернуть
        # @bot.message_handler(commands=[keyword])
        @bot.message_handler(commands=['test'])
        def handler(message):
            '''TODO прописать поподробнее, клавиатурку и тд'''
            id = message.from_user.id
            msg = send_message(id, step.text, keyboard=False)
            # заполнение идёт в обратном порядке

            record = db[id]
            record['step'] = 1
            db[id] = record

            bot.register_next_step_handler(msg, self._next_handler(id))
            print(hash(self._last_existing_handler))

            # ВАЖНО: не разбирает сообщение, т.к. оно /test или типа
        # print(hash(handler))
        # globals()[self.handler_prefix + str(self.number_of_handler)] = handler
        # self.number_of_handler += 1

        return handler

    def _create_middle_handler(self, step):
        '''создаёт хендлер из середины'''
        def handler(message):
            '''TODO прописать поподробнее, клавиатурку и тд'''
            id = message.from_user.id
            self._write_to_db(id, message.text)

            msg = send_message(id, step.text, keyboard=False)

            record = db[id]
            record['step'] += 1
            db[id] = record

            bot.register_next_step_handler(msg,
                                           self._next_handler(id))
        globals()[self.handler_prefix + str(self.number_of_handler)] = handler
        # self.number_of_handler += 1

        return handler

    def _process(self, id):
        return self._process_function(self._get_from_db(id))

    def _create_last_handler(self):
        '''создаёт финальный хендлер, который всё обрабатывает'''
        global handler
        def handler(message):
            id = message.from_user.id

            self._write_to_db(id, message.text)

            msg = send_message(id, self._process(id), keyboard=False)
        # globals()[self.handler_prefix + str(self.number_of_handler)] = handler
        # self.number_of_handler += 1

        return handler

    def _write_to_db(self, id, info):
        '''записывает в key-value кусочек информации, полученной от человека
        в ходе теста.
        хранит в списке'''
        record = db[id]


        if self._name not in record:
            record[self._name] = []
        record[self._name].append(info)

        db[id] = record

    def _get_from_db(self, id):
        '''получает список из кусков информации'''
        return userdblib.db[id].get(self._name, [])




class Step:
    '''элементарный шаг'''
    def __init__(self, text, buttons=None):
        self._text = text
        # raise NotImplementedError

    @property
    def text(self):
        return self._text

    def __str__(self):
        return self.text

# ExampleTest = Test(keyword='test',
#                    name='Test',
#                    steps=[Step('Привет!'),
#                           Step('Как ты себя чувствуешь?')],
#                    process_function=lambda l: f'''Вы здороваетесь так: "{l[0]}", а чувствуете себя так:{l[1]}'''
#                             )


# Эта штука хранится в базе данных у каждого пользователя
# TestState = namedtuple('TestState', ['test_class', 'num_of_step'])


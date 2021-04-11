'''здесь будут храниться тесты (шкала Бека/Альтмана), процедуры КПТ и прочее'''
# from abc import ABC, abstractmethod
# import configparser
from collections import namedtuple
import configparser
from functools import wraps
import os
from baseconfig import TESTS_DIRNAME

from telebot import types

import userdblib
# import handlersbot as hb
import baseconfig
from wrapper_sendmessage import send_message, create_keyboard

bot = baseconfig.bot
db = userdblib.db

all_handlers = []


def stop_when_stop(func):
    '''декоратор.
    возвращает функцию,
    которая обрабатывает request_handler,
    если мы были на полшаге'''
    #  мб сделать DEPRECATED
    # TODO перенести логику в textprocess

    def is_stop(s):
        return s.strip().lower() in ['/stop', 'stop', 'остановись', 'прервись']

    @wraps(func)
    def result_func(message):#, *args, **kwargs):
        if is_stop(message.text):
            send_message(message.from_user.id, "Вы вернулись назад.")
        else:
            func(message) #, *args, **kwargs)

    return result_func

class CBTTest:
    # для хранения в глобальной области хендлеров
    number_of_handler = 0
    handler_prefix = 'cbtest_handler'

    def __init__(self, *, name='Test', keyword='test', steps=None,
                 process_function=None,
                 all_handlers_decorator=stop_when_stop,
                 middle_handlers_decorator=lambda x: x):
        '''объекты этого класса - тесты
        name - имя в базе данных, дб уникально
        keyword - команда для входа в тест, типа beck (если команда /beck)
        steps - шаги - объекты класса Step
        process_function - функция, выдающая результат по списку из бд
        all_handlers_decorator - декоратор, обрамляющий все хендлеры.
                                 по умолчанию - stop_when_stop, останавливается при остановке
        middle_handlers_decorator - декоратор, обрамляющий хендлеры из середины
        '''
        assert steps is not None
        assert process_function is not None

        # self._bot = bot
        self._name = name
        self._keyword = keyword
        self._process_function = process_function

        self._all_handlers_decorator = all_handlers_decorator
        self._middle_handlers_decorator = middle_handlers_decorator

        self._steps = steps[:]

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

    @property
    def name(self):
        return self._name

    @property
    def keyword(self):
        return self._keyword

    @property
    def steps(self):
        return self._steps


    def _next_handler(self, id):
        '''обращается к БД чтобы определить, на каком ты сейчас шаге'''
        return self._handlers_list[db[id]['step']]

    @property
    def _last_existing_handler(self):
        '''возвращает последний уже созданный хендлер, он же первый в тесте'''
        raise NotImplementedError
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
        @bot.message_handler(commands=[keyword])
        @self._all_handlers_decorator
        # @bot.message_handler(commands=['test'])
        def handler(message):
            '''TODO прописать поподробнее, клавиатурку и тд'''
            id = message.from_user.id
            print('keyboard:', step.keyboard)
            msg = send_message(id, step.text, keyboard=step.keyboard)

            record = db[id]
            record['step'] = 1
            db[id] = record

            bot.register_next_step_handler(msg, self._next_handler(id))

        return handler

    def _create_middle_handler(self, step):
        '''создаёт хендлер из середины'''
        @self._all_handlers_decorator
        @self._middle_handlers_decorator
        def handler(message):
            '''TODO прописать поподробнее, клавиатурку и тд'''
            id = message.from_user.id
            self._write_to_db(id, message.text)

            msg = send_message(id, step.text, keyboard=step.keyboard)

            record = db[id]
            record['step'] += 1
            db[id] = record

            bot.register_next_step_handler(msg,
                                           self._next_handler(id))

        return handler

    def _process(self, id):
        return self._process_function(self._get_from_db(id))

    def _create_last_handler(self):
        '''создаёт финальный хендлер, который всё обрабатывает'''
        @self._all_handlers_decorator
        def handler(message):
            id = message.from_user.id

            self._write_to_db(id, message.text)

            msg = send_message(id, self._process(id), keyboard=None)

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
    def __init__(self, text, answers=None):
        '''text - текст вопроса
        answers - список возможных ответов, если пустой - принимается так
        TODO сделать валидацию ответа и повторно спросить, если непонятно'''
        # def create_keyboard(lst):
        #     keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        #     for button_text in lst:
        #        key = types.KeyboardButton(text=button_text)
        #        keyboard.add(key)
        #     return keyboard

        self._text = text

        self._keyboard = create_keyboard(answers)

    @property
    def text(self):
        return self._text

    @property
    def keyboard(self):
        return self._keyboard

    def __str__(self):
        return self.text


class NumericTest(CBTTest):
    '''тест с клавиатуркой и числами, типа шкалы Бека
    questions - вопросы'''
    def __init__(self, *, name, keyword, steps, process_function=None):
        super().__init__(name=name, keyword=keyword, steps=steps,
                         process_function=process_function,)

    @classmethod
    def create_from_file(cls, file_name, *, process_function=None):
        #  Считывает тест из конфига
        if process_function is None:
            '''если обработчик результата не задан'''
            def process_function(lst):
                '''просто посчитать баллы'''
                result = 0
                for i, val in enumerate(lst):
                    # TODO сделать больше 9 баллов возможно
                    result += int(val[1])
                return result

        test = configparser.ConfigParser()
        test.read(file_name)

        general_info = test['general']
        name = general_info['name']
        keyword = general_info['keyword']

        _number_of_questions = int(general_info['number_of_questions'])
        assert _number_of_questions > 0
        _number_of_answers = int(general_info['number_of_answers'])
        assert _number_of_answers > 0

        steps = []

        for i in range(1, _number_of_questions + 1):
            question = test['question' + str(i)]
            text = question['text']
            answers = []
            for j in range(1, _number_of_answers + 1):
                try:
                    answers.append(question['answer' + str(j)])
                except IndexError:
                    # TODO сделать динамическое количество ответов
                    raise
            steps.append(Step(text, answers))



        return NumericTest(name=name, keyword=keyword, steps=steps,
                           process_function=process_function)

'''здесь будут храниться тесты (шкала Бека/Альтмана), процедуры КПТ и прочее'''
from abc import ABC, abstractmethod
import configparser
from collections import namedtuple

import handlersbot as hb

bot = hb.bot

class Test:
    def __init__(self, trigger, steps):
        '''объекты этого класса - тесты
        trigger - триггер для входа в тест, типа /beck
        steps - шаги - объекты класса Step'''
        # config = configparser.ConfigParser()
        # config.read(config_file_name)
        # self._process(config)

        first_step = steps[0]
        other_steps = steps[1:]

        self._handlers = []

        # first_handler(self._create_first_handler(first_step, trigger))

        last_handler = ...

        for st in reversed(other_step):
            self._handlers.append(self._create_handler(step))



    def _create_first_handler(self, step, keyword):
        '''создаёт первый хендлер'''
        @bot.message_handler(commands=[keyword])
        def handler(message):
            '''TODO прописать поподробнее, клавиатурку и тд'''
            id = message.from_user.id
            msg = send_support_message(id, step.text, keyboard=False)
            bot.register_next_step_handler(msg, self._handlers)

        return handler

    def _create_handler(self, step):
        pass

    def final_handler(self):
        pass

    @abstractmethod
    def process(self):
        '''обрабатывает собранные данные, возвращает результат'''
        pass



class Step:
    '''элементарный шаг'''
    def __init__(self, text, buttons=None):
        pass
        # raise NotImplementedError

ExampleTest = Test(
    steps = [Step('Привет!'),
             Step('Как ты себя чувствуешь?')])


# Эта штука хранится в базе данных у каждого пользователя
TestState = namedtuple('TestState', ['test_class', 'num_of_step'])


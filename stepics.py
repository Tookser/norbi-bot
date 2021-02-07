'''здесь будут храниться тесты (шкала Бека/Альтмана), процедуры КПТ и прочее'''
from abc import ABC, abstractmethod
import configparser
from collections import namedtuple

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

        handlers = []

        handlers.append(self._create_first_handler(first_step, trigger))

        for st in other_steps:
            handlers.append(self._create_handler(step))



    def _create_first_handler(self, step, keyword):
        '''создаёт первый хендлер'''
        pass

    def _create_handler(self, step):
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


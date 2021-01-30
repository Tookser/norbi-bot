import sys
sys.path.append('..')
from os.path import join
from random import randint
import random
import string

import pytest

import baseconfig
import load
import textprocess

is_start_message = textprocess.is_start_message


########### load.py . load_config() ######

def test_buttons_part_exists():
    conf = load.load_config()
    assert 'keyboard' in conf
    d = dict(conf['keyboard'])

def test_buttons_more_than_0():
    conf = load.load_config()
    d = dict(conf['keyboard'])
    assert len(d)

def test_all_buttons_len():
    conf = load.load_config()
    d = dict(conf['keyboard'])

    for k, d in d.items():
        assert len(k)
        assert len(d)

########### textprocess.py ###############

def test_hi_basic():
    assert not is_start_message('')
    assert is_start_message('hi')
    assert is_start_message('/start')

def test_hi_different_languages():
    assert is_start_message('привет')
    assert is_start_message('hello')

def test_hi_case():
    assert is_start_message('ПрИвЕт')

def test_compound():
    assert is_start_message('!ПрИвЕт ботик!')
    assert is_start_message('прИвки, ты, герой кнопчни')
    assert is_start_message('Good morning and hellO, bottie...')

def test_hi_no():
    assert not is_start_message('rwiwo1')
    assert not is_start_message('DfDfgaAHe')

########## load.py tests #############

@pytest.fixture
def phrases():
    return load.load_phrases()


def test_load_get_token():
    assert baseconfig.BOT_ENABLE or load.get_token()

def test_load_phrases_non_empty_lists(phrases):
    assert phrases
    for k, v in phrases.items():
        assert(v)

def test_load_phrases_non_empty_strings(phrases):
    for k in phrases:
        for s in phrases:
            assert s.strip()

@pytest.fixture
def phrases_lst(tmp_path):
    name = join(tmp_path, 'test.txt')
    lst = ['', '1', '431', 'sjfagkl', '', 'Привет.', '   ', ' ', 'Fdfds.', '//comment', 'DfdsDdd', '', '']

    with open(name, 'w') as f:
        for s in lst:
            f.write(s + '\n')

    with open(name) as f:
        lst = load.load_list_from_file(f)

    return lst

def write_list_in_file(lst, tmp_path):
    ''' in 'test.txt' '''
    with open(join(tmp_path, 'test.txt'), 'w') as f:
        for s in lst:
            f.write(s + '\n')

def test_load_list_from_file_non_empty(phrases_lst):
    for s in phrases_lst:
        assert s


def test_load_list_from_file_number(phrases_lst):
    assert len(phrases_lst) == 6

def test_load_list_from_file_result(phrases_lst):
    assert phrases_lst == \
            ['1', '431', 'sjfagkl', 'Привет.', 'Fdfds.', 'DfdsDdd']

def test_load_list_from_file_result(tmp_path):
    def random_string(k):
        return ''.join(random.choices(string.ascii_uppercase + \
                                      string.digits, k=k))

    def strings_gen():
        return [(random_string(randint(1, 50)), True)
                for i in range(randint(20, 100))]

    for i in range(10):
        spaces = [(' ' * randint(0, 5), False) for i in range(randint(5, 10))]
        strings = strings_gen()
        comments = [('//' + s[0], False) for s in strings_gen()]
        result = spaces + strings + comments
        random.shuffle(result)

        correct_result_of_function = [s[0] for s in result if s[1]]

        to_file = [s[0] for s in result]
        write_list_in_file(to_file, tmp_path)

        with open(join(tmp_path, 'test.txt')) as f:
            result_lst = load.load_list_from_file(f)
            assert correct_result_of_function == result_lst

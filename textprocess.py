import load

phrases = load.load_phrases()

def is_start_message(text):
    '''проверяет, является ли текст приветствием'''
    text = text.lower().strip()
    words = ['прив', 'здравств', 'здраст', 'hi', 'hello', '/start',
             'рш', 'руддщ', 'ghbd', 'plhfdcnd', '.ыефке']
    return any((word in text) for word in words)


def is_request(text):
    '''проверяет, является ли запросом на похвалу/ругань'''
    return text in phrases

def is_set_name(text):
    '''проверяет, является ли сообщение запросом на смену имени'''
    text_words = text.lower().strip().split(' ')

    set_words = ['имя', 'смен', 'име', 'name']
    for set_word in set_words:
        for text_word in text_words:
            if set_word in text_word:
                return True

    return False

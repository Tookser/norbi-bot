def is_start_message(text):
    text = text.lower().strip()
    words = ['прив', 'здравств', 'здраст', 'hi', 'hello', '/start']
    return any((word in text) for word in words)

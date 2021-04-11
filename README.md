# norbi-bot
Telegram bot on pytelegrambotapi created to help people with mental issues.

В данный момент реализует 
* [Тест Альтмана](https://ru.wikipedia.org/wiki/%D0%A8%D0%BA%D0%B0%D0%BB%D0%B0_%D0%90%D0%BB%D1%8C%D1%82%D0%BC%D0%B0%D0%BD%D0%B0_%D0%B4%D0%BB%D1%8F_%D1%81%D0%B0%D0%BC%D0%BE%D0%BE%D1%86%D0%B5%D0%BD%D0%BA%D0%B8_%D0%BC%D0%B0%D0%BD%D0%B8%D0%B8) (самодиагностика [мании/гипомании](https://ru.wikipedia.org/wiki/%D0%93%D0%B8%D0%BF%D0%BE%D0%BC%D0%B0%D0%BD%D0%B8%D1%8F)). В планах реализация и остальных тестов (таких как шкала Бека).
* Посылание поддерживающих сообщений. В данный момент посылает каждый раз новое сообщение, пока они не будут исчерпаны.

В планах:
* Новые тесты
* Привязка событий ко времени
* Индивидуализация
* Другое...

Перед использование нужно создать файл config_private.ini в папке data с содержимым:

[token]

token=ТОКЕНВАШЕГОБОТА


#!/usr/bin/python3
'''тут почти ничего нет, всё в handlersbot'''

import handlersbot as hb

def main():
    hb.bot.enable_save_next_step_handlers(delay=2)
    hb.bot.load_next_step_handlers()

    hb.bot.polling()

if __name__ == '__main__':
    main()

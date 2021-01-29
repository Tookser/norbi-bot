
import shelve
from pprint import pprint
import sys

import baseconfig



def main():
    with shelve.open(baseconfig.USERDB_FILENAME) as userdb:
        if len(sys.argv) == 1:
            pprint(dict(userdb))
        elif sys.argv[1] in ['-c', '--clean'] or True:
            userdb.clear()
            print('DB cleaned')


if __name__ == '__main__':
    main()
else:
    def clean_db():
        with shelve.open(baseconfig.USERDB_FILENAME) as userdb:
            userdb.clear()
            print('DB cleaned')

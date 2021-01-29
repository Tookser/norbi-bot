
import shelve
from pprint import pprint
import sys

import baseconfig

with shelve.open(baseconfig.USERDB_FILENAME) as userdb:
    if len(sys.argv) == 1:
        pprint(dict(userdb))
    elif sys.argv[1] in ['-c', '--clean'] or True:
        userdb.clear()
        print('DB cleaned')

#
#
#

import os


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


def printsyspath():
    import sys
    for p in sys.path:
        print( "path:", p )

import sys

from spotify_api.func_api import Func_api

def main(args=None):
    if args is None:
        args = sys.argv[1:]

    app = Func_api()

if __name__ == '__main__':
    sys.exit(main())
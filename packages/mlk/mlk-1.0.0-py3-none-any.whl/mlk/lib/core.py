import os
import sys
import json
import getpass
import platform

from pprint import pprint
from datetime import datetime, timedelta
from os.path import expanduser

from mlk.mlk.checker.checkutils import CheckUtils


class Config():

    def __init__(s):

        if s.is_debug():
            print('DEBUG: Init global config: swissarmykit_conf')


    @staticmethod
    def is_debug():
        return os.environ.get('MLK_DEBUG')


    def show_data(self):
        pprint(vars(self))


    def info(self):
        return CheckUtils.info()

    def __repr__(self):
        try:
            if not os.environ.get('_FROM_CONSOLE'):
                pprint(vars(self))
                print(sys.version)
        except Exception as e:
            print(e)
        return ''

if __name__ == '__main__':
    print(os.environ.get('AI_ENV', 'dev'))

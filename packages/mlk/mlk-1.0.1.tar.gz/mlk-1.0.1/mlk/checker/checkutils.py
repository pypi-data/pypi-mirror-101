import os
import sys
import importlib

from swissarmykit.conf import *

class CheckUtils:

    @staticmethod
    def info():
        import tensorflow as tf
        physical_devices = tf.config.list_physical_devices('GPU')

        print('\n\n----------------------------------')
        print(f'python      : {sys.version}')
        print(f'tensorflow  : {CheckUtils.ger_version("tensorflow")}')
        print(f'keras       : {CheckUtils.ger_version("keras")}')
        print(f'autokeras   : {CheckUtils.ger_version("autokeras")}')
        print(f'pandas      : {CheckUtils.ger_version("pandas")}')
        print(f'numpy       : {CheckUtils.ger_version("numpy")}')
        print(f'sklearn     : {CheckUtils.ger_version("sklearn")}') # pip install scikit-learn, but import sklearn

        print()
        print(physical_devices)
        print()

        print(appConfig.brief())
        print('\n\n----------------------------------')


    @staticmethod
    def ger_version(module_name):
        try:
            mod = importlib.import_module(module_name)
            return mod.__version__
        except ImportError as e:
            print(e)
        return 0

    @staticmethod
    def get_modules(modules='viz'):
        modules = modules if isinstance(modules, list) else [modules]
        import glob
        modules = glob.glob(os.path.join(os.path.dirname(__file__), "*.py"))
        __all__ = [os.path.basename(f)[:-3] for f in modules if os.path.isfile(f) and not f.endswith('__init__.py')]
        return __all__

    @staticmethod
    def tensorflow_ver():
        return CheckUtils.ger_version("tensorflow")

if __name__ == '__main__':
    CheckUtils.info()


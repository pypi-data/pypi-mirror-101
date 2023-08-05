import functools
import inspect
import datetime
import sys


class _StdoutHandler:
    def __init__(self, filename):
        self.filename = filename

    def write(self, text):
        with open(self.filename, 'a') as f:
            f.write(text)

    def flush(self):
        pass


class _Print2File:
    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        original_stdout = sys.stdout
        sys.stdout = _StdoutHandler(f'{inspect.stack()[2].filename.replace(".py", "")}-{self.func.__name__}.txt')
        try:
            result = self.func(*args, **kwargs)
            return result
        finally:
            sys.stdout = original_stdout

    def __get__(self, instance, owner):
        return functools.partial(self.__call__, instance)


def print2file(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return _Print2File(func)(*args, **kwargs)

    return wrapper

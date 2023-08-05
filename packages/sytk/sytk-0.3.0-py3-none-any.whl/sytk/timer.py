import time
import functools


class _Timer:
    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        start = time.time()
        return_value = self.func(*args, **kwargs)
        end = time.time()
        duration = end - start
        return return_value, duration

    def __get__(self, instance, owner):
        return functools.partial(self.func, instance)


def timer(func):

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return _Timer(func)(*args, **kwargs)

    return wrapper

import logging

_LEVEL = logging.INFO
_FORMAT = '[%(name)s] - %(levelname)s - %(message)s'


class Logger(logging.Logger):
    def __init__(self, name: str):
        super().__init__(name)
        formatter = logging.Formatter(fmt=_FORMAT)
        handler = logging.StreamHandler()
        handler.setLevel(_LEVEL)
        handler.setFormatter(formatter)
        self.addHandler(handler)
        self.setLevel(_LEVEL)

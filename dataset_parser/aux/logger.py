import logging


class Logger:
    def __init__(self):
        pass

    @classmethod
    def set(cls, filename):
        logging.basicConfig(format='%(message)s', filename=filename, level=logging.DEBUG)
        # log to file and print to stdout (https://stackoverflow.com/a/13733863/4547232)
        logging.getLogger().addHandler(logging.StreamHandler())

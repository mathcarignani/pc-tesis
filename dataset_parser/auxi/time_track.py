import time

class TimeTrack:
    def __init__(self):
        self.start_time = time.time()

    def elapsed(self, figures=None):
        elapsed_time = time.time() - self.start_time
        elapsed_time = round(elapsed_time, figures) if figures else elapsed_time
        return elapsed_time

    @classmethod
    def time_str(cls, value):
        return time.strftime("%M:%S", time.gmtime(value))

# -*- coding: utf-8 -*-
# BASED ON: https://gist.github.com/aubricus/f91fb55dc6ba5557fbab06119420dd6a
import sys

class ProgressBar:
    def __init__(self, total):
        self.total = total
        self.total_float = float(total)

    # Print iterations progress
    def print_progress(self, iteration, prefix = 'Progress:', suffix = 'Complete', decimals=1, bar_length = 25):
        """
        Call in a loop to create terminal progress bar
        @params:
            iteration   - Required  : current iteration (Int)
            total       - Required  : total iterations (Int)
            prefix      - Optional  : prefix string (Str)
            suffix      - Optional  : suffix string (Str)
            decimals    - Optional  : positive number of decimals in percent complete (Int)
            bar_length  - Optional  : character length of bar (Int)
        """
        str_format = "{0:." + str(decimals) + "f}"
        percents = str_format.format(100 * (iteration / self.total_float))
        filled_length = int(round(bar_length * iteration / self.total_float))
        bar = '█' * filled_length + '-' * (bar_length - filled_length)

        sys.stdout.write('\r%s |%s| %s%s %s' % (prefix, bar, percents, '%', suffix)),

        if iteration == self.total:
            sys.stdout.write('\n')
        sys.stdout.flush()

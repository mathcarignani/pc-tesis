# -*- coding: utf-8 -*-
# BASED ON: https://gist.github.com/aubricus/f91fb55dc6ba5557fbab06119420dd6a
import sys


class ProgressBar:
    def __init__(self, total, mod_range=1000, prefix='Progress:', suffix='Complete', decimals=1, bar_length=25):
        self.total = total
        self.total_float = float(total)
        self.mod_range = mod_range
        self.prefix = prefix
        self.suffix = suffix
        self.str_format = "{0:." + str(decimals) + "f}"
        self.bar_length = bar_length

    def print_progress(self, current_line):
        if (current_line != self.total) and (current_line % self.mod_range != 0):
            return
        percents = self.str_format.format(100 * (current_line / self.total_float))
        filled_length = int(round(self.bar_length * current_line / self.total_float))
        bar = '█' * filled_length + '-' * (self.bar_length - filled_length)

        sys.stdout.write('\r%s |%s| %s%s %s' % (self.prefix, bar, percents, '%', self.suffix)),
        if current_line == self.total:
            sys.stdout.write('\n')
        sys.stdout.flush()

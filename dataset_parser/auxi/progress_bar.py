# -*- coding: utf-8 -*-
# BASED ON: https://gist.github.com/aubricus/f91fb55dc6ba5557fbab06119420dd6a
import sys
from auxi.time_track import TimeTrack

#
# EXAMPLE USAGE:
# array = [1] * 100
# progress_bar = ProgressBar(len(array))
# count = 0
# for element in array:
#   count += 1
#   progress_bar.print_progress(count)
#
class ProgressBar:
    def __init__(self, total, mod_range=1000, prefix='Progress:', suffix='Complete', decimals=1, bar_length=25):
        self.total = total
        self.total_float = float(total)
        self.mod_range = mod_range
        self.prefix = prefix
        self.suffix = suffix
        self.str_format = "{0:." + str(decimals) + "f}"
        self.bar_length = bar_length
        self.time_track = TimeTrack()
        self.current_line = 0

    def print_progress(self):
        self.current_line += 1
        if (self.current_line != self.total) and (self.current_line % self.mod_range != 0):
            return
        percentage = self.current_line / self.total_float
        percents = self.str_format.format(100 * percentage)
        filled_length = int(round(self.bar_length * self.current_line / self.total_float))
        bar = '█' * filled_length + '-' * (self.bar_length - filled_length)

        elapsed_s, remaining_s = self._elapsed_and_remaining(percentage)

        progress_str = '%s |%s|' % (self.prefix, bar)
        percentage_str = '%s%s %s' % (percents, '%', self.suffix)

        line = '\r%s %s - Elapsed: %s - Remaining: %s' % (progress_str, percentage_str, elapsed_s, remaining_s)
        sys.stdout.write(line),
        if self.current_line == self.total:
            sys.stdout.write('\n')
        sys.stdout.flush()

    def _elapsed_and_remaining(self, percentage):
        elapsed = self.time_track.elapsed()
        elapsed_s = TimeTrack.time_str(elapsed)

        if elapsed < 5 or percentage < 0.05:  # less than 5 seconds or less than 5% processed
            remaining_s = "???"
        else:
            remaining = elapsed / percentage - elapsed
            remaining_s = TimeTrack.time_str(remaining)

        return elapsed_s, remaining_s

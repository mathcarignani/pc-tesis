import sys
sys.path.append('.')

from scripts.avances14.single_plot import SinglePlot


class RowPlot(object):
    def __init__(self, error_threshold):
        self.plots = []
        self.single_plot = None
        self.error_threshold = error_threshold

    def begin_algorithm(self, algorithm):
        self.single_plot = SinglePlot(algorithm)

    def end_algorithm(self):
        self.single_plot.check_windows()
        self.plots.append(self.single_plot)

    def add_values(self, window, value0, value3):
        self.single_plot.add_values(window, value0, value3)

    def y_lim(self):
        max_y_lim = 0
        for single_plot in self.plots:
            ylim = single_plot.ylim()
            if ylim > max_y_lim:
                max_y_lim = ylim
        return max_y_lim

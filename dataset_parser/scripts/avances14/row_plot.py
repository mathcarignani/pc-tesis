import sys
sys.path.append('.')

from scripts.avances14.single_plot import SinglePlot
from scripts.avances11.utils import average


class RowPlot(object):
    def __init__(self, error_threshold):
        self.plots = []
        self.single_plot = None
        self.error_threshold = error_threshold
        self.plot_values = []

    def begin_algorithm(self, algorithm):
        self.single_plot = SinglePlot(algorithm)

    def end_algorithm(self):
        self.single_plot.check_windows()
        self.plots.append(self.single_plot)

    def plot_stats(self, ax, ylim, extra):
        values = {
            'max': max(self.plot_values),
            'avg': average(self.plot_values),
            'min': min(self.plot_values)
        }
        SinglePlot.plot_stats(ax, ylim, self.error_threshold, values, extra)

    def add_values(self, window, value0, value3, basic_value0):
        plot_value = SinglePlot.plot_value(value0, value3)
        self.single_plot.add_values(window, value0, value3, plot_value, basic_value0)
        self.plot_values.append(plot_value)

    def y_lim_row(self):
        max_y_lim = 0
        for single_plot in self.plots:
            ylim = single_plot.ylim()
            if ylim > max_y_lim:
                max_y_lim = ylim
        return max_y_lim

    ####################################################################################################################

    @classmethod
    def sum(cls, row_plot1, row_plot2):
        assert(row_plot1.error_threshold == row_plot2.error_threshold)
        assert(len(row_plot1.plots) == len(row_plot2.plots))
        row_plot = RowPlot(row_plot1.error_threshold)
        for single_plot1, single_plot2 in zip(row_plot1.plots, row_plot2.plots):
            row_plot.single_plot = SinglePlot.sum(single_plot1, single_plot2)
            row_plot.end_algorithm()
        return row_plot

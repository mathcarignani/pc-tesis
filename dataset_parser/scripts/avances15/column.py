import sys
sys.path.append('.')

from scripts.avances15.compression_ratio_plot import CompressionRatioPlot
from scripts.avances15.relative_difference_plot import RelativeDifferencePlot
from scripts.avances15.total_bits_plot import TotalBitsPlot
from scripts.avances15.windows_plot import WindowsPlot


class Column(object):
    def __init__(self, algorithm):
        self.total_bits_plot = TotalBitsPlot(algorithm)
        self.compression_ratio_plot = CompressionRatioPlot(algorithm)
        self.relative_difference_plot = RelativeDifferencePlot(algorithm)
        self.windows_plot = WindowsPlot(algorithm)
        self.stats_table = None
        self.y_min_bits, self.y_max_bits, self.y_min_rel, self.y_max_rel, self.y_min_ratio, self.y_max_ratio = [None] * 6

    def add_values(self, best_values):
        value0, value3 = best_values['value0']['min'], best_values['value3']['min']
        basic_value0 = best_values['basic_value0']
        self.total_bits_plot.add_values(value0, value3, basic_value0)
        self.compression_ratio_plot.add_values(value0, value3, basic_value0)
        self.relative_difference_plot.add_value(value0, value3)
        self.windows_plot.add_values(best_values['value0']['window'], best_values['value3']['window'])

    def close(self):
        self.total_bits_plot.close()
        self.compression_ratio_plot.close()
        self.relative_difference_plot.close()
        self.windows_plot.close()

    def add_mins_maxs(self, y_min_bits, y_max_bits, y_min_rel, y_max_rel, y_min_ratio, y_max_ratio):
        self.y_min_bits = y_min_bits
        self.y_max_bits = y_max_bits
        self.y_min_rel = y_min_rel
        self.y_max_rel = y_max_rel
        self.y_min_ratio = y_min_ratio
        self.y_max_ratio = y_max_ratio

    def rows(self):
        return [self.total_bits_plot, self.compression_ratio_plot, self.relative_difference_plot, self.windows_plot]

    def plot(self, row_i, ax, extra):
        if row_i == 0:
            self.total_bits_plot.plot(ax, self.y_min_bits, self.y_max_bits, extra)
        elif row_i == 1:
            self.compression_ratio_plot.plot(ax, self.y_min_ratio, self.y_max_ratio, extra)
        elif row_i == 2:
            self.relative_difference_plot.plot(ax, self.y_min_rel, self.y_max_rel, extra)
        else:
            self.windows_plot.plot(ax, extra)

import sys
sys.path.append('.')

from scripts.informe.plots.compression_ratio_plot import CompressionRatioPlot
from scripts.informe.plots.relative_difference_plot import RelativeDifferencePlot
from scripts.informe.plots.stats import RelativeDifferenceStats, WindowsStats
from scripts.informe.plots.total_bits_plot import TotalBitsPlot


class Matrix(object):
    def __init__(self):
        self.columns = []
        self.relative_difference_stats = RelativeDifferenceStats()
        self.windows_stats = WindowsStats()

    def set_colors(self, value0_color, value3_color, label0, label3):
        for column in self.columns:
            column.set_colors(value0_color, value3_color)
        for column in [self.relative_difference_stats, self.windows_stats]:
            column.set_colors_and_labels(value0_color, value3_color, label0, label3)

    def empty(self):
        return len(self.columns) == 0

    def total_rows_columns(self):
        return len(self.columns[0].rows()), len(self.columns)

    def add_values(self, best_values):
        self.relative_difference_stats.add_values(best_values['value0']['min'], best_values['value3']['min'])
        self.windows_stats.add_values(best_values['value0']['window'], best_values['value3']['window'])

    def add_column(self, column):
        self.columns.append(column)

    def close(self):
        if len(self.columns) != 6:
            print "len(self.columns) = " + str(len(self.columns))
            assert(len(self.columns) == 6)
        self.relative_difference_stats.close()
        self.windows_stats.close()

        y_min_bits, y_max_bits = self.__ylims_total_bits_plot()
        y_min_ratio, y_max_ratio = self.__ylims_compression_ratio_plot()
        y_min_rel, y_max_rel = self.__ylims_relative_difference_plot()
        for column in self.columns:
            column.add_mins_maxs(y_min_bits, y_max_bits, y_min_rel, y_max_rel, y_min_ratio, y_max_ratio)

    def __ylims_total_bits_plot(self):
        plots = [column.total_bits_plot for column in self.columns]
        total_min, total_max = self.__min_max(plots)
        return TotalBitsPlot.ylims(total_min, total_max)

    def __ylims_compression_ratio_plot(self):
        plots = [column.compression_ratio_plot for column in self.columns]
        total_min, total_max = self.__min_max(plots)
        return CompressionRatioPlot.ylims(total_min, total_max)

    def __ylims_relative_difference_plot(self):
        plots = [column.relative_difference_plot for column in self.columns]
        total_min, total_max = self.__min_max(plots)
        return RelativeDifferencePlot.ylims(total_min, total_max)

    def print_values(self):
        column = self.columns[0]
        column.print_values()

    @classmethod
    def __min_max(cls, plots):
        total_min, total_max = None, None
        for plot in plots:
            current_min, current_max = plot.min_max()
            if total_max is None:
                total_min, total_max = current_min, current_max
            else:
                total_min = current_min if current_min < total_min else total_min
                total_max = current_max if current_max > total_max else total_max
        return total_min, total_max

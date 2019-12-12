import sys
sys.path.append('.')

import matplotlib.pyplot as plt

from scripts.avances.avances15.compression_ratio_plot import CompressionRatioPlot
from scripts.avances.avances15.relative_difference_plot import RelativeDifferencePlot
from scripts.avances.avances15.windows_plot import WindowsPlot
from scripts.avances.avances15.stats import RelativeDifferenceStats, WindowsStats
from scripts.informe.plot.plot_utils import PlotUtils


class PdfPage(object):
    PLOT_MAPPER = {
        'compression': CompressionRatioPlot,
        'relative': RelativeDifferencePlot,
        'window': WindowsPlot,
        'relative_stats': RelativeDifferenceStats,
        'window_stats': WindowsStats
    }

    def __init__(self, panda_utils_0, panda_utils_3, filename, col_index, figsize_h, figsize_v, plots_options=None):
        self.panda_utils_0 = panda_utils_0
        self.panda_utils_3 = panda_utils_3
        self.filename = filename
        self.col_index = col_index
        self.plots_options = plots_options
        self.fig = PlotUtils.create_figure(figsize_h, figsize_v, filename + ' - col = ' + str(col_index))

    def create(self, coders_array, plots_array, plots_matrix):
        plots_obj = {}
        for plot_key in plots_array:
            options = self.plots_options and self.plots_options.get(plot_key)
            plot_klass = PdfPage.PLOT_MAPPER[plot_key]
            plots = plot_klass.create_plots(coders_array, self.panda_utils_0, self.panda_utils_3, self.col_index, options)
            plots_obj[plot_key] = plots

        self.__add_plots(plots_matrix, plots_obj)
        # self.fig.set_tight_layout(True)
        # self.fig.subplots_adjust(hspace=0.1)
        return self.fig, plt

    def __add_plots(self, plots_matrix, plots_obj):
        self.total_rows, self.total_columns = len(plots_matrix), len(plots_matrix[0])
        current_subplot = 1
        for row_index, row in enumerate(plots_matrix):
            for col_index, matrix_entry in enumerate(row):
                ax = self.fig.add_subplot(self.total_rows, self.total_columns, current_subplot)
                self.__add_plot(matrix_entry, ax, plots_obj, row_index, col_index)
                current_subplot += 1

    def __add_plot(self, matrix_entry, ax, plots_obj, row_index, col_index):
        coder_name, plot_key = matrix_entry
        if coder_name is not None:
            plot_instance = plots_obj[plot_key][coder_name]
            extra = {
                'show_title': row_index in [0, 3],
                'last_row': row_index == (self.total_rows - 1),
                'show_ylabel': col_index == 0,
                'last_column': col_index == (self.total_columns - 2)
            }
            plot_instance.plot2(ax, extra)
        else:
            plot_instance = plots_obj[plot_key]
            plot_instance.plot(ax)

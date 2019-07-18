import sys
sys.path.append('.')

import matplotlib.pyplot as plt

from scripts.avances.avances15.compression_ratio_plot import CompressionRatioPlot
from scripts.avances.avances15.relative_difference_plot import RelativeDifferencePlot
from scripts.avances.avances15.windows_plot import WindowsPlot
from scripts.avances.avances15.stats import RelativeDifferenceStats, WindowsStats
from scripts.informe.plot.plot_utils import PlotUtils
from scripts.informe.results_parsing.results_to_pandas import ResultsToPandas


class Plotter(object):
    FIGSIZE_H = 10
    FIGSIZE_V = 25

    def __init__(self, panda_utils_0, panda_utils_3, filename, col_index):
        self.panda_utils_0 = panda_utils_0
        self.panda_utils_3 = panda_utils_3
        self.filename = filename
        self.col_index = col_index

    def create(self):
        fig_title = self.filename + ' - col = ' + str(self.col_index)
        self.fig = PlotUtils.create_figure(Plotter.FIGSIZE_H, Plotter.FIGSIZE_V, fig_title)

        coders_array = ['CoderPCA', 'CoderAPCA', 'CoderCA', 'CoderPWLH', 'CoderPWLHInt', 'CoderGAMPSLimit']
        plots_obj = {
            'compression': CompressionRatioPlot.create_plots(coders_array, self.panda_utils_0, self.panda_utils_3, self.col_index),
            'relative': RelativeDifferencePlot.create_plots(coders_array, self.panda_utils_0, self.panda_utils_3, self.col_index),
            'window': WindowsPlot.create_plots(coders_array, self.panda_utils_0, self.panda_utils_3, self.col_index),
            'relative_stats': RelativeDifferenceStats.create_plot(coders_array, self.panda_utils_0, self.panda_utils_3, self.col_index),
            'window_stats': WindowsStats.create_plot(coders_array, self.panda_utils_0, self.panda_utils_3, self.col_index)
        }
        plots_matrix = [
            [['CoderPCA', 'compression'],  ['CoderAPCA', 'compression'],    ['CoderCA', 'compression']],
            [['CoderPCA', 'relative'],     ['CoderAPCA', 'relative'],       ['CoderCA', 'relative']],
            [['CoderPCA', 'window'],       ['CoderAPCA', 'window'],         ['CoderCA', 'window']],
            [['CoderPWLH', 'compression'], ['CoderPWLHInt', 'compression'], ['CoderGAMPSLimit', 'compression']],
            [['CoderPWLH', 'relative'],    ['CoderPWLHInt', 'relative'],    ['CoderGAMPSLimit', 'relative']],
            [['CoderPWLH', 'window'],      ['CoderPWLHInt', 'window'],      ['CoderGAMPSLimit', 'window']],
            [[None, 'relative_stats'],     [None, 'window_stats']]
        ]
        self.__add_plots(plots_matrix, plots_obj)
        # self.fig.set_tight_layout(True)
        # self.fig.subplots_adjust(hspace=0.1)
        return self.fig, plt

    def __add_plots(self, plots_matrix, plots_obj):
        self.total_rows, self.total_columns = len(plots_matrix), len(plots_matrix[0])
        current_subplot = 1
        for row_index, row in enumerate(plots_matrix):
            for col_index, entry in enumerate(row):
                ax = self.fig.add_subplot(self.total_rows, self.total_columns, current_subplot)
                self.__add_plot(entry, ax, plots_obj, row_index, col_index)
                current_subplot += 1

    def __add_plot(self, entry, ax, plots_obj, row_index, col_index):
        coder_name, plot_key = entry
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

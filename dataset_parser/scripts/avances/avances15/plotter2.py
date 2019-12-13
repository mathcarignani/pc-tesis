import sys
sys.path.append('.')

# import numpy as np
import matplotlib.pyplot as plt

from scripts.compress.experiments_utils import ExperimentsUtils
from scripts.informe.plot.plot_utils import PlotUtils
from scripts.avances.avances15.column import Column
from scripts.avances.avances15.matrix import Matrix


class Plotter2(object):
    FIGSIZE_H = 10
    FIGSIZE_V = 25

    def __init__(self, plotter):
        self.plotter = plotter
        self.matrix = Matrix()
        self.init_with_matrix = False

    def set_colors(self, value0_color, value3_color, label0, label3):
        self.matrix.set_colors(value0_color, value3_color, label0, label3)

    def set_matrix(self, matrix):
        self.matrix = matrix

    def plot(self):
        fig = PlotUtils.create_figure(Plotter2.FIGSIZE_H, Plotter2.FIGSIZE_V, self.plotter.column_title())
        if self.matrix.empty():
            self.__collect_data_plot()
        return self.__plot(fig)

    def __plot(self, fig):
        # plot
        total_rows, total_columns = self.matrix.total_rows_columns()
        # print "(total_rows, total_columns) = ", (total_rows, total_columns)
        self.__plot_data(fig, total_rows)
        self.__plot_stats(fig)
        return fig, plt

    # TODO: remove this method
    @staticmethod
    def __map_subplot(row_i, col_j):
        val = row_i*6 + col_j + 1
        if val in [1, 2, 3]:
            pass
        elif val in [4, 5, 6]:
            val += 6
        elif val in [7, 8, 9]:
            val -= 3
        elif val in [10, 11, 12]:
            val += 3
        elif val in [13, 14, 15]:
            val -= 6
        elif val in [16, 17, 18]:
            pass
        else:
            raise(StandardError, "error => " + str(val))
        extra_options = {
            'first_column': val in [1, 4, 7, 10, 13, 16],
            'last_column': val in [3, 6, 9, 12, 15, 18],
            'first_row': val in [1, 2, 3, 10, 11, 12],
            'last_row': val in [16, 17, 18]
        }
        return 7, 3, val, extra_options

    def __plot_data(self, fig, total_rows):
        for col_j, column in enumerate(self.matrix.columns):
            for row_i in range(total_rows):
                row, col, current_subplot, extra_options = self.__map_subplot(row_i, col_j)
                # print(row, col, current_subplot)
                ax = fig.add_subplot(row, col, current_subplot)
                column.plot(row_i, ax, extra_options)

    def __plot_stats(self, fig):
        ax = fig.add_subplot(7, 3, 19)
        self.matrix.relative_difference_stats.plot(ax)

        ax = fig.add_subplot(7, 3, 20)
        self.matrix.windows_stats.plot(ax)

    def __collect_data_plot(self):
        for algorithm_index, algorithm in enumerate(ExperimentsUtils.ALGORITHMS):
            column = Column(algorithm, True)
            for row_index, row_plot in enumerate(self.plotter.row_plots):  # threshold row
                single_plot = row_plot.plots[algorithm_index]  # algorithm
                best_values = single_plot.best_values()  # get best values for <threshold, algorithm>
                column.add_values(best_values)
                self.matrix.add_values(best_values)
            column.close()
            self.matrix.add_column(column)
        self.matrix.close()

    def print_values(self):
        print "Plotter 2 - print_values"
        self.matrix.print_values()

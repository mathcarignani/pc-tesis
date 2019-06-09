import sys
sys.path.append('.')

# import numpy as np
import matplotlib.pyplot as plt
from scripts.avances14.constants import Constants
from scripts.avances14.plot_utils import PlotUtils
from scripts.avances15.column import Column
from scripts.avances15.matrix import Matrix


class Plotter2(object):
    def __init__(self, plotter):
        self.plotter = plotter
        self.matrix = Matrix()

    def plot(self):
        fig = PlotUtils.create_figure(20, 10, self.plotter.column_title())
        self.collect_data()
        
        # plot
        total_rows, total_columns = self.matrix.total_rows_columns()
        total_columns += 1  # stats column

        # plot data
        for col_j, column in enumerate(self.matrix.columns):
            first_column = (col_j == 0)
            last_column = (col_j == total_columns - 1)

            for row_i in range(total_rows):
                first_row = (row_i == 0)
                last_row = (row_i == total_rows - 1)

                current_subplot = row_i*total_columns + col_j + 1
                # print(total_rows, total_columns, current_subplot)
                ax = fig.add_subplot(total_rows, total_columns, current_subplot)
                extra = {
                    'first_column': first_column, 'last_column': last_column,
                    'first_row': first_row, 'last_row': last_row
                }
                column.plot(row_i, ax, extra)

        # plot stats
        current_subplot = 2*total_columns + total_columns  # third row
        ax = fig.add_subplot(total_rows, total_columns, current_subplot)
        self.matrix.relative_difference_stats.plot(ax)

        current_subplot = 3*total_columns + total_columns  # fourth row
        ax = fig.add_subplot(total_rows, total_columns, current_subplot)
        self.matrix.windows_stats.plot(ax)

        return fig, plt

    def collect_data(self):
        # collect data
        for algorithm_index, algorithm in enumerate(Constants.ALGORITHMS):
            column = Column(algorithm)
            for row_index, row_plot in enumerate(self.plotter.row_plots):  # threshold row
                single_plot = row_plot.plots[algorithm_index]  # algorithm
                best_values = single_plot.best_values()
                column.add_values(best_values)
                self.matrix.add_values(best_values)
            column.close()
            self.matrix.add_column(column)
        self.matrix.close()

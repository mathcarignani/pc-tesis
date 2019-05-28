import sys
sys.path.append('.')

import numpy as np
import matplotlib.pyplot as plt


class Plotter(object):
    def __init__(self, filename, column_index):
        self.filename = filename
        self.column_index = column_index
        self.row_plots = []

    def add_row_plot(self, row_plot):
        if len(self.row_plots) > 0 and len(self.row_plots[0].plots) != len(row_plot.plots):
            raise Exception("ERROR: add_horizontal_plot")
        self.row_plots.append(row_plot)

    def plot(self):
        white_background = (1, 1, 1)
        figsize = (20, 30)
        fig = plt.figure(figsize=figsize, facecolor=white_background)
        fig.suptitle(self.filename + ' - col = ' + str(self.column_index), fontsize=20)

        y_lim = self.__y_lim()
        total_vertical_plots = len(self.row_plots)
        for vertical_index, row_plot in enumerate(self.row_plots):
            first_row = (vertical_index == 0)
            # y_lim = row_plot.y_lim_row()
            # total_horizontal_plots the same in each iteration
            total_horizontal_plots = len(row_plot.plots) + 1  # +1 because of the stats plot
            for horizontal_index, single_plot in enumerate(row_plot.plots):
                current_subplot = total_horizontal_plots*vertical_index + horizontal_index + 1
                ax = fig.add_subplot(total_vertical_plots, total_horizontal_plots, current_subplot)
                extra = {
                    'first_row': first_row,
                    'last_row': vertical_index == total_vertical_plots - 1,
                    'first_column': horizontal_index == 0,
                    'last_column': False
                }
                single_plot.plot(ax, y_lim, extra)

            current_subplot = total_horizontal_plots*vertical_index + total_horizontal_plots
            ax = fig.add_subplot(total_vertical_plots, total_horizontal_plots, current_subplot)
            extra = {'first_row': first_row, 'last_column': True}
            row_plot.plot_stats(ax, y_lim, extra)

        fig.set_tight_layout(True)
        fig.subplots_adjust(hspace=0.1)

        # plt.savefig(self.__fig_name())
        # plt.show()

        return fig, plt

    def __y_lim(self):
        max_y_lim = 0
        for row_plot in self.row_plots:
            y_lim_row = row_plot.y_lim_row()
            if y_lim_row > max_y_lim:
                max_y_lim = y_lim_row
        return max_y_lim

    def __fig_name(self):
        return self.filename + "-" + str(self.column_index) + ".pdf"

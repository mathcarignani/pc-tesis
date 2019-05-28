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
        figsize = (15, 30)
        fig = plt.figure(figsize=figsize, facecolor=white_background)
        fig.suptitle(self.filename + ' - col = ' + str(self.column_index), fontsize=20)

        total_vertical_plots = len(self.row_plots)
        for vertical_index, horizontal_plot in enumerate(self.row_plots):
            y_lim = horizontal_plot.y_lim()
            total_horizontal_plots = len(horizontal_plot.plots)  # the same in each iteration
            for horizontal_index, single_plot in enumerate(horizontal_plot.plots):
                current_subplot = total_horizontal_plots*vertical_index + horizontal_index + 1
                ax = fig.add_subplot(total_vertical_plots, total_horizontal_plots, current_subplot)
                extra = {
                    'first_row': vertical_index == 0,
                    'last_row': vertical_index == total_vertical_plots - 1,
                    'first_column': horizontal_index == 0,
                    'last_column': horizontal_index == total_horizontal_plots - 1
                }
                single_plot.plot(ax, y_lim, horizontal_plot.error_threshold, extra)

        # fig.subplots_adjust(wspace=0.05)
        # # fig.set_tight_layout(True)
        # fig.subplots_adjust(left=0.06, right=0.95, top=0.88)

        fig.subplots_adjust(hspace=0.1)
        # plt.savefig(self.filename)
        plt.show()

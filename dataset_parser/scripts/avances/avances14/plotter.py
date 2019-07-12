import sys
sys.path.append('.')

import matplotlib.pyplot as plt
from scripts.informe.plot.plot_utils import PlotUtils
from scripts.avances.avances14 import RowPlot


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
        fig = PlotUtils.create_figure(20, 30, self.column_title())
        y_lim = self.__y_lim()
        total_vertical_plots = len(self.row_plots)
        for vertical_index, row_plot in enumerate(self.row_plots):
            first_row = (vertical_index == 0)
            last_row = (vertical_index == total_vertical_plots - 1)
            # total_horizontal_plots the same in each iteration
            total_horizontal_plots = len(row_plot.plots) + 1  # +1 because of the stats plot
            for horizontal_index, single_plot in enumerate(row_plot.plots):
                first_column = (horizontal_index == 0)
                current_subplot = total_horizontal_plots*vertical_index + horizontal_index + 1
                ax = fig.add_subplot(total_vertical_plots, total_horizontal_plots, current_subplot)
                extra = {
                    'first_row': first_row,
                    'last_row': last_row,
                    'first_column': first_column,
                    'last_column': False
                }
                single_plot.plot(ax, y_lim, extra)

            current_subplot = total_horizontal_plots*vertical_index + total_horizontal_plots
            ax = fig.add_subplot(total_vertical_plots, total_horizontal_plots, current_subplot)
            extra = {'first_row': first_row, 'last_column': True}
            row_plot.plot_stats(ax, y_lim, extra)

        fig.set_tight_layout(True)
        fig.subplots_adjust(hspace=0.1)
        return fig, plt

    def column_title(self):
        return self.filename + ' - col = ' + str(self.column_index)

    def __y_lim(self):
        max_y_lim = 0
        for row_plot in self.row_plots:
            y_lim_row = row_plot.y_lim_row()
            if y_lim_row > max_y_lim:
                max_y_lim = y_lim_row
        return max_y_lim

    def __fig_name(self):
        return self.filename + "-" + str(self.column_index) + ".pdf"

    ####################################################################################################################

    @classmethod
    def sum(cls, plotter1, plotter2):
        # assert(plotter1.filename == plotter2.filename)
        assert(len(plotter1.row_plots) == len(plotter2.row_plots))
        plotter = Plotter(plotter1.filename, 0)  # column_index param doesn't matter
        for row_plot1, row_plot2 in zip(plotter1.row_plots, plotter2.row_plots):
            row_plot = RowPlot.sum(row_plot1, row_plot2)
            plotter.add_row_plot(row_plot)
        return plotter

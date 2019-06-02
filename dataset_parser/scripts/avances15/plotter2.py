import sys
sys.path.append('.')

import matplotlib.pyplot as plt
from scripts.avances14.constants import Constants
from scripts.avances14.single_plot import SinglePlot


class Plotter2(object):
    VALUE0_COLOR = Constants.COLOR_RED
    VALUE3_COLOR = Constants.COLOR_LIGHT_BLUE
    VALUE_SAME = Constants.COLOR_YELLOW

    def __init__(self, plotter):
        self.plotter = plotter
        self.matrix = Matrix()

    def plot(self):
        fig = self.plotter.create_fig(20, 10)

        # collect data
        for algorithm_index, algorithm in enumerate(Constants.ALGORITHMS):
            column = Column(algorithm)
            for row_index, row_plot in enumerate(self.plotter.row_plots):  # threshold row
                single_plot = row_plot.plots[algorithm_index]  # algorithm
                best_values = single_plot.best_values()
                column.add_values(best_values)
            column.close()
            self.matrix.add_column(column)

        y_min_bits, y_max_bits = self.matrix.ylims_total_bits_plot()
        y_min_rel, y_max_rel = self.matrix.ylims_relative_difference_plot()
        
        # plot
        total_rows, total_columns = self.matrix.total_rows_columns()
        for j, column in enumerate(self.matrix.columns):
            first_column = (j == 0)
            last_column = (j == total_columns - 1)

            for i, row in enumerate(column.rows()):
                first_row = (i == 0)
                last_row = (i == total_rows - 1)

                current_subplot = i*total_columns + j + 1
                # print(total_rows, total_columns, current_subplot)
                ax = fig.add_subplot(total_rows, total_columns, current_subplot)
                extra = {'first_column': first_column, 'first_row': first_row, 'last_row': last_row}
                if i == 0:
                    row.plot(ax, y_min_rel, y_max_rel, extra)
                elif i == 1:
                    row.plot(ax, y_min_bits, y_max_bits, extra)
                else:  # last_row
                    row.plot(ax, extra)

        # total_vertical_plots = len(self.row_plots)
        # for vertical_index, row_plot in enumerate(self.row_plots):
        #     first_row = (vertical_index == 0)
        #     last_row = (vertical_index == total_vertical_plots - 1)
        #     # total_horizontal_plots the same in each iteration
        #     total_horizontal_plots = len(row_plot.plots) + 1  # +1 because of the stats plot
        #     for horizontal_index, single_plot in enumerate(row_plot.plots):
        #         first_column = (horizontal_index == 0)
        #         current_subplot = total_horizontal_plots*vertical_index + horizontal_index + 1
        #         ax = fig.add_subplot(total_vertical_plots, total_horizontal_plots, current_subplot)
        #         extra = {
        #             'first_row': first_row,
        #             'last_row': last_row,
        #             'first_column': first_column,
        #             'last_column': False
        #         }
        #         single_plot.plot(ax, y_lim, extra)
        #
        #     current_subplot = total_horizontal_plots*vertical_index + total_horizontal_plots
        #     ax = fig.add_subplot(total_vertical_plots, total_horizontal_plots, current_subplot)
        #     extra = {'first_row': first_row, 'last_column': True}
        #     row_plot.plot_stats(ax, y_lim, extra)

        # fig.set_tight_layout(True)
        # fig.subplots_adjust(hspace=0.1)
        # plt.savefig(self.__fig_name())
        # plt.show()
        return fig, plt


class Matrix(object):
    def __init__(self):
        self.columns = []

    def total_rows_columns(self):
        return len(self.columns[0].rows()), len(self.columns)

    def add_column(self, column):
        self.columns.append(column)

    def close(self):
        assert(len(self.columns) == 3)
        
    def ylims_total_bits_plot(self):
        plots = [column.total_bits_plot for column in self.columns]
        total_min, total_max = self.__min_max(plots)
        return TotalBitsPlot.ylims(total_min, total_max)
        
    def ylims_relative_difference_plot(self):
        plots = [column.relative_difference_plot for column in self.columns]
        total_min, total_max = self.__min_max(plots)
        return RelativeDifferencePlot.ylims(total_min, total_max)

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

    
class Column(object):
    def __init__(self, algorithm):
        self.total_bits_plot = TotalBitsPlot(algorithm)
        self.relative_difference_plot = RelativeDifferencePlot(algorithm)
        self.windows_plot = WindowsPlot(algorithm)

    def add_values(self, best_values):
        self.total_bits_plot.add_values(best_values['value0']['min'], best_values['value3']['min'])
        self.relative_difference_plot.add_value(best_values['value0']['min'], best_values['value3']['min'])
        self.windows_plot.add_values(best_values['value0']['window'], best_values['value3']['window'])

    def close(self):
        self.total_bits_plot.close()
        self.relative_difference_plot.close()
        self.windows_plot.close()

    def rows(self):
        return [self.relative_difference_plot, self.total_bits_plot, self.windows_plot]


class TotalBitsPlot(object):
    def __init__(self, algorithm):
        self.algorithm = algorithm
        self.values0 = []
        self.values3 = []
    
    def add_values(self, value0, value3):
        self.values0.append(value0)
        self.values3.append(value3)
    
    def close(self):
        assert(len(self.values0) == len(Constants.THRESHOLDS))
        assert(len(self.values3) == len(Constants.THRESHOLDS))
    
    def min_max(self):
        return [min([min(self.values0), min(self.values3)]), max([max(self.values0), max(self.values3)])]

    def plot(self, ax, ymin, ymax, extra):
        # print self.algorithm + " Total Bits"
        # print "self.values0 = " + str(self.values0)
        # print "self.values3 = " + str(self.values3)

        # scatter plot
        x_axis = list(xrange(len(self.values0)))
        ax.scatter(x=x_axis, y=self.values0, c=Plotter2.VALUE0_COLOR)
        ax.scatter(x=x_axis, y=self.values3, c=Plotter2.VALUE3_COLOR)
        ax.grid(b=True, color=Constants.COLOR_SILVER)
        ax.set_axisbelow(True)

        if extra['first_row']:
            ax.title.set_text(self.algorithm)
        if not extra['last_row']:
            ax.set_xticklabels([])
        if extra['first_column']:
            ax.set_ylabel('Total Bits')
            self.format_x_ticks(ax)
        else:
            ax.set_yticklabels([])
        RelativeDifferencePlot.set_lim(ax, ymin, ymax)

    @classmethod
    def format_x_ticks(cls, ax):
        ylabels = [format(label, ',.0f') for label in ax.get_yticks()]
        ax.set_yticklabels(ylabels)

    @classmethod
    def ylims(cls, total_min, total_max):
        assert(total_min > 0)
        assert(total_max > 0)

        diff = total_max - total_min
        return total_min - diff * 0.1, total_max + diff * 0.1


class RelativeDifferencePlot(object):
    def __init__(self, algorithm):
        self.algorithm = algorithm
        self.values = []

    def add_value(self, value0, value3):
        plot_value = SinglePlot.plot_value(value0, value3)
        self.values.append(plot_value)

    def close(self):
        assert(len(self.values) == len(Constants.THRESHOLDS))

    def min_max(self):
        return [min(self.values), max(self.values)]

    def plot(self, ax, ymin, ymax, extra):
        # print self.algorithm + " Relative Difference"
        # print "self.values = " + str(self.values)

        # scatter plot
        x_axis = list(xrange(len(self.values)))
        ax.scatter(x=x_axis, y=self.values, c=Plotter2.VALUE3_COLOR)
        ax.grid(b=True, color=Constants.COLOR_SILVER)
        ax.set_axisbelow(True)

        if extra['first_row']:
            ax.title.set_text(self.algorithm)
        if not extra['last_row']:
            ax.set_xticklabels([])
        if extra['first_column']:
            ax.set_ylabel('Relative Difference')
        else:
            ax.set_yticklabels([])
        self.set_lim(ax, ymin, ymax)

    @classmethod
    def set_lim(cls, ax, ymin, ymax):
        ax.set_xlim(left=-1, right=8)  # 8 thresholds
        ax.set_ylim(bottom=ymin, top=ymax)

    @classmethod
    def ylims(cls, total_min, total_max):
        if total_max > 0:
            total_max *= 1.1
        elif total_max == 0:
            total_max = 0.1
        else:  # total_max < 0
            total_max *= 0.9

        if total_min > 0:
            total_min -= (total_max - total_min) * 0.1
        elif total_min == 0:
            total_min = - 0.1
        else:  # total_min < 0
            total_min *= 1.1

        return total_min, total_max


class WindowsPlot(object):
    def __init__(self, algorithm):
        self.algorithm = algorithm
        self.windows0 = []
        self.windows3 = []

    def add_values(self, window0, window3):
        self.windows0.append(window0)
        self.windows3.append(window3)

    def close(self):
        total_thresholds = len(Constants.THRESHOLDS)
        assert(len(self.windows0) == total_thresholds)
        assert(len(self.windows3) == total_thresholds)

    def plot(self, ax, extra):
        # print self.algorithm + " Windows"
        # print "self.windows0 = " + str(self.windows0)
        # print "self.windows3 = " + str(self.windows3)

        x_axis_0, y_axis_0, x_axis_3, y_axis_3, x_axis_same, y_axis_same = [], [], [], [], [], []
        for i, values in enumerate(zip(self.windows0, self.windows3)):
            value0, value3 = values
            pos_value0 = self.__position(value0)
            if value0 == value3:
                x_axis_same.append(i); y_axis_same.append(pos_value0)
            else:
                x_axis_0.append(i); y_axis_0.append(pos_value0)
                pos_value3 = self.__position(value3)
                x_axis_3.append(i); y_axis_3.append(pos_value3)

        ax.scatter(x=x_axis_0, y=y_axis_0, c=Plotter2.VALUE0_COLOR)
        ax.scatter(x=x_axis_3, y=y_axis_3, c=Plotter2.VALUE3_COLOR)
        ax.scatter(x=x_axis_same, y=y_axis_same, c=Plotter2.VALUE_SAME)
        ax.grid(b=True, color=Constants.COLOR_SILVER)
        ax.set_axisbelow(True)
        ax.set_xticklabels([''] + Constants.THRESHOLDS)

        if extra['first_column']:
            ax.set_ylabel('Window Size')
            ax.set_yticklabels([''] + Constants.WINDOWS)
        else:
            ax.set_yticklabels([])
        ax.set_ylim(top=len(Constants.WINDOWS), bottom=-1)

    @classmethod
    def __position(cls, window):
        return Constants.WINDOWS.index(window)
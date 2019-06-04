import sys
sys.path.append('.')

import numpy as np
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

        self.collect_data()
        
        # plot
        total_rows, total_columns = self.matrix.total_rows_columns()
        total_columns += 1  # stats column
        # print (total_rows, total_columns)
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
                # if last_column:
                #     row.plot(ax)
                #     continue
                column.plot(row_i, ax, extra)

        # plot stats
        current_subplot = 1*total_columns + total_columns  # second row
        ax = fig.add_subplot(total_rows, total_columns, current_subplot)
        self.matrix.relative_difference_stats.plot(ax)

        current_subplot = 2*total_columns + total_columns  # third row
        ax = fig.add_subplot(total_rows, total_columns, current_subplot)
        self.matrix.windows_stats.plot(ax)

        # fig.set_tight_layout(True)
        # fig.subplots_adjust(hspace=0.1)
        # plt.savefig(self.__fig_name())
        # plt.show()
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


class Matrix(object):
    def __init__(self):
        self.columns = []
        self.relative_difference_stats = RelativeDifferenceStats()
        self.windows_stats = WindowsStats()

    def total_rows_columns(self):
        return len(self.columns[0].rows()), len(self.columns)

    def add_values(self, best_values):
        self.relative_difference_stats.add_values(best_values['value0']['min'], best_values['value3']['min'])
        self.windows_stats.add_values(best_values['value0']['window'], best_values['value3']['window'])

    def add_column(self, column):
        self.columns.append(column)

    def close(self):
        assert(len(self.columns) == 6)
        self.relative_difference_stats.close()
        self.windows_stats.close()

        y_min_bits, y_max_bits = self.__ylims_total_bits_plot()
        y_min_rel, y_max_rel = self.__ylims_relative_difference_plot()
        for column in self.columns:
            column.add_mins_maxs(y_min_bits, y_max_bits, y_min_rel, y_max_rel)

    def __ylims_total_bits_plot(self):
        plots = [column.total_bits_plot for column in self.columns]
        total_min, total_max = self.__min_max(plots)
        return TotalBitsPlot.ylims(total_min, total_max)
        
    def __ylims_relative_difference_plot(self):
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

    @classmethod
    def sorted(cls, array):
        return all(array[i] <= array[i+1] for i in xrange(len(array)-1))

    @classmethod
    def sorted_dec(cls, array):
        return all(array[i] >= array[i+1] for i in xrange(len(array)-1))


class Column(object):
    def __init__(self, algorithm):
        self.total_bits_plot = TotalBitsPlot(algorithm)
        self.relative_difference_plot = RelativeDifferencePlot(algorithm)
        self.windows_plot = WindowsPlot(algorithm)
        self.stats_table = None
        self.y_min_bits, self.y_max_bits, self.y_min_rel, self.y_max_rel = [None] * 4

    def add_values(self, best_values):
        value0, value3 = best_values['value0']['min'], best_values['value3']['min']
        self.total_bits_plot.add_values(value0, value3)
        self.relative_difference_plot.add_value(value0, value3)
        self.windows_plot.add_values(best_values['value0']['window'], best_values['value3']['window'])

    def close(self):
        self.total_bits_plot.close()
        self.relative_difference_plot.close()
        self.windows_plot.close()

    def add_mins_maxs(self, y_min_bits, y_max_bits, y_min_rel, y_max_rel):
        self.y_min_bits = y_min_bits
        self.y_max_bits = y_max_bits
        self.y_min_rel = y_min_rel
        self.y_max_rel = y_max_rel

    def rows(self):
        return [self.total_bits_plot, self.relative_difference_plot, self.windows_plot]

    def plot(self, row_i, ax, extra):
        if row_i == 0:
            self.total_bits_plot.plot(ax, self.y_min_bits, self.y_max_bits, extra)
        elif row_i == 1:
            self.relative_difference_plot.plot(ax, self.y_min_rel, self.y_max_rel, extra)
        else:
            self.windows_plot.plot(ax, extra)


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
        self.__check_sorted()
    
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

    def __check_sorted(self):
        assert(Matrix.sorted_dec(self.values0))
        assert(Matrix.sorted_dec(self.values3))

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
        colors = [self.__color_code(item) for item in self.values]
        ax.scatter(x=x_axis, y=self.values, c=colors)
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

    @classmethod
    def __color_code(cls, value):
        if value > 0:
            return Plotter2.VALUE3_COLOR
        elif value < 0:
            return Plotter2.VALUE0_COLOR
        else:  # value == 0
            return Plotter2.VALUE_SAME


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
        self.__check_sorted()

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

        if extra['last_row']:
            ax.set_xlabel('Error Threshold (%)')
        if extra['first_column']:
            ax.set_ylabel('Window Size')
            ax.set_yticklabels([''] + Constants.WINDOWS)
        else:
            ax.set_yticklabels([])
        ax.set_ylim(top=len(Constants.WINDOWS), bottom=-1)

    def __check_sorted(self):
        if self.algorithm != "CoderPCA":
            assert(Matrix.sorted(self.windows0))
            assert(Matrix.sorted(self.windows3))

    @classmethod
    def __position(cls, window):
        return Constants.WINDOWS.index(window)


class RelativeDifferenceStats(object):
    def __init__(self):
        self.total_results = 0
        self.best0_results = 0
        self.best3_results = 0
        self.same_results = 0

    def add_values(self, value0, value3):
        self.total_results += 1
        if value0 == value3:
            self.same_results += 1
        elif value0 < value3:
            self.best0_results += 1
        else:  # value3 < value0
            self.best3_results += 1

    def close(self):
        assert(self.total_results == self.best0_results + self.best3_results + self.same_results)
        assert(self.total_results == 6 * 8)

    def plot(self, ax):
        col_labels = ['BEST', '#', '%']
        row_labels = ['MM=0', 'SAME', 'MM=3']
        results = [self.best0_results, self.same_results, self.best3_results]
        colors = [Plotter2.VALUE0_COLOR, Plotter2.VALUE_SAME, Plotter2.VALUE3_COLOR]
        self.plot_aux(ax, col_labels, zip(results, row_labels, colors))

    def plot_aux(self, ax, col_labels, zipped_values):
        table_values, table_colors = [], []
        for total, label, color in zipped_values:
            percentage = self.percentage(self.total_results, total)
            table_values.append([label, total, percentage])
            cell_color = Constants.COLOR_WHITE if total == 0 else color
            table_colors.append([cell_color, Constants.COLOR_WHITE, Constants.COLOR_WHITE])

        # Draw table
        the_table = ax.table(cellText=table_values, colWidths=[0.12, 0.1, 0.12], cellColours=table_colors,
                             colLabels=col_labels,
                             loc='center right')
        # the_table.auto_set_font_size(True)
        the_table.set_fontsize(14)
        the_table.scale(3, 2)

        # Removing ticks and spines enables you to get the figure only with table
        ax.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
        ax.tick_params(axis='y', which='both', right=False, left=False, labelleft=False)

        for pos in ['right', 'top', 'bottom', 'left']:
            ax.spines[pos].set_visible(False)

    @classmethod
    def percentage(cls, total, value):
        return round((float(100) / float(total)) * value, 2)


class WindowsStats(RelativeDifferenceStats):
    def plot(self, ax):
        col_labels = ['BIG', '#', '%']
        row_labels = ['MM=0', 'SAME', 'MM=3']
        results = [self.best3_results, self.same_results, self.best0_results]
        colors = [Plotter2.VALUE0_COLOR, Plotter2.VALUE_SAME, Plotter2.VALUE3_COLOR]
        self.plot_aux(ax, col_labels, zip(results, row_labels, colors))

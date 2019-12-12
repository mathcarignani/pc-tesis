import sys
sys.path.append('.')

from scripts.compress.experiments_utils import ExperimentsUtils
from scripts.informe.math_utils import MathUtils
from scripts.informe.plot.plot_constants import PlotConstants
from scripts.informe.plot.plot_utils import PlotUtils


class SinglePlot(object):
    def __init__(self, algorithm):
        self.algorithm = algorithm
        self.values0 = []
        self.values3 = []
        self.basic_values0 = []
        self.current_plot = []

        self.windows = []
        self.expected_window = 4

    def add_values(self, window, value0, value3, plot_value, basic_value0):
        self.__check_window(window)
        self.values0.append(value0)
        self.values3.append(value3)
        self.basic_values0.append(basic_value0)
        self.current_plot.append(plot_value)

    def best_values(self):
        assert(len(ExperimentsUtils.WINDOWS) == len(self.values0))
        assert(len(ExperimentsUtils.WINDOWS) == len(self.values3))
        assert(len(ExperimentsUtils.WINDOWS) == len(self.basic_values0))
        assert(len(set(self.basic_values0)) == 1)  # check that all the values in the list match
        value0_min, value3_min = min(self.values0), min(self.values3),
        value0_min_index, value3_min_index = self.values0.index(value0_min), self.values3.index(value3_min)
        res = {
            'value0': {'min': value0_min, 'window': ExperimentsUtils.WINDOWS[value0_min_index]},
            'value3': {'min': value3_min, 'window': ExperimentsUtils.WINDOWS[value3_min_index]},
            'basic_value0': self.basic_values0[0]
        }
        return res

    def check_windows(self):
        if self.windows != ExperimentsUtils.WINDOWS:
            raise Exception("ERROR: check_windows")

    def ylim(self):
        max_value = max([abs(value) for value in self.current_plot])  # 1.27
        return max_value * 1.1  # 1.397

    def plot(self, ax, ylim, extra_options={}):
        # scatter plot
        color = [self.__color_code(item) for item in self.current_plot]
        x_axis = list(xrange(len(self.current_plot)))
        ax.scatter(x=x_axis, y=self.current_plot, c=color)
        ax.grid(b=True, color=PlotConstants.COLOR_SILVER)

        if extra_options['first_row']:
            # only write the algorithm name in the first row
            ax.title.set_text(self.algorithm)

        if extra_options['last_row']:
            # only write window tick labels in the last row
            ax.set_xticklabels(self.__xticklabels())
        else:
            ax.set_xticklabels([])

        if extra_options['first_column']:
            ax.set_ylabel('Relative Difference')
        else:
            ax.set_yticklabels([])

        self.__set_lim(ax, ylim)

        # horizontal lines
        PlotUtils.horizontal_line(ax, 0, PlotConstants.COLOR_SILVER)
        avg = MathUtils.average(self.current_plot)
        PlotUtils.horizontal_line(ax, avg, self.__color_code(avg))

        self.stats_box(ax, max(self.current_plot), avg, min(self.current_plot), PlotConstants.COLOR_WHITE)

    @classmethod
    def plot_stats(cls, ax, ylim, error_threshold, values, extra_options={}):
        ax.grid(b=True, color=PlotConstants.COLOR_SILVER)

        if extra_options['first_row']:
            # only write 'STATS' in the first row
            ax.title.set_text("Threshold Stats")

        ax.set_xticklabels([])
        ax.set_yticklabels([])

        if extra_options['last_column']:
            ax.yaxis.set_label_position("right")
            ax.set_ylabel('Error Thresold = {}%'.format(error_threshold))

        cls.__set_lim(ax, ylim)

        # horizontal lines
        PlotUtils.horizontal_line(ax, 0, PlotConstants.COLOR_SILVER)
        PlotUtils.horizontal_line(ax, values['max'], PlotConstants.COLOR_BLUE)
        PlotUtils.horizontal_line(ax, values['avg'], cls.__color_code(values['avg']))
        PlotUtils.horizontal_line(ax, values['min'], PlotConstants.COLOR_BLUE)

        cls.stats_box(ax, values['max'], values['avg'], values['min'], PlotConstants.COLOR_WHEAT)

    @classmethod
    def __set_lim(cls, ax, ylim):
        ax.set_xlim(left=-1, right=7)  # 7 windows
        ax.set_ylim(top=ylim, bottom=-ylim)

    @classmethod
    def stats_box(cls, ax, max_val, avg_val, min_val, facecolor):
        string = '\n'.join(('MAX = %.2f' % max_val, 'AVG = %.2f' % avg_val, 'MIN = %.2f' % min_val))
        props = dict(boxstyle='round', facecolor=facecolor, alpha=0.5)
        ax.text(0.45, 0.05, string, transform=ax.transAxes, fontsize=14, horizontalalignment='left', bbox=props, family='monospace')

    @classmethod
    def __color_code(cls, value):
        if value > 0:
            return PlotConstants.COLOR_GREEN
        elif value < 0:
            return PlotConstants.COLOR_RED
        else:  # value == 0
            return PlotConstants.COLOR_BLACK

    @classmethod
    def plot_value(cls, value0, value3):
        dividend = value0 - value3
        value = float(dividend) / float(value0) if dividend != 0 else 0
        return value
    # def plot_value(cls, value0, value3):
    #     if value0 == value3:
    #         return 0
    #     elif value0 > value3:  # map to positive
    #         return float(value0) / float(value3) - 1
    #     else:  # value3 > value0  # map to negative
    #         return -float(value3) / float(value0) + 1

    def __check_window(self, window):
        if window != self.expected_window:
            raise Exception("ERROR: check_window")
        self.windows.append(window)
        self.expected_window *= 2

    @classmethod
    def __xticklabels(cls):
        xticklabels = ['']
        for index, value in enumerate(ExperimentsUtils.WINDOWS):
            power = index + 2
            label = r"$2^{}$".format(power)  # 2^power
            xticklabels.append(label)
        return xticklabels

    ####################################################################################################################

    @classmethod
    def sum(cls, single_plot1, single_plot2):
        assert(single_plot1.algorithm == single_plot2.algorithm)
        single_plot = SinglePlot(single_plot1.algorithm)
        values0 = cls.sum_arrays(single_plot1.values0, single_plot2.values0)
        values3 = cls.sum_arrays(single_plot1.values3, single_plot2.values3)
        basic_values0 = cls.sum_arrays(single_plot1.basic_values0, single_plot2.basic_values0)
        for index, (value0, value3, basic_value0) in enumerate(zip(values0, values3, basic_values0)):
            window = ExperimentsUtils.WINDOWS[index]
            single_plot.add_values(window, value0, value3, 0, basic_value0)  # plot_value = 0, doesn't matter
        return single_plot

    @classmethod
    def sum_arrays(cls, array1, array2):
        assert(len(array1) == len(array2))
        return [x + y for x, y in zip(array1, array2)]

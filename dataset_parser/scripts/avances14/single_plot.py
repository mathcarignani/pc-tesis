import sys
sys.path.append('.')

from scripts.avances11.utils import average


class SinglePlot(object):
    WINDOWS = [4, 8, 16, 32, 64, 128, 256]
    COLOR_SILVER = 'silver'
    COLOR_BLUE = 'blue'
    COLOR_RED = 'red'
    COLOR_WHITE = 'white'
    COLOR_GREEN = 'limegreen'
    COLOR_WHEAT = 'wheat'
    COLOR_BLACK = 'black'

    def __init__(self, algorithm):
        self.algorithm = algorithm
        self.values0 = []
        self.values3 = []
        self.current_plot = []

        self.windows = []
        self.expected_window = 4

    def add_values(self, window, value0, value3, plot_value):
        self.__check_window(window)
        self.values0.append(value0)
        self.values3.append(value3)
        self.current_plot.append(plot_value)

    def check_windows(self):
        if self.windows != self.WINDOWS:
            raise Exception("ERROR: check_windows")

    def ylim(self):
        max_value = max([abs(value) for value in self.current_plot])  # 1.27
        return max_value * 1.1  # 1.397

    def plot(self, ax, ylim, extra):
        # scatter plot
        color = [self.__color_code(item) for item in self.current_plot]
        x_axis = list(xrange(len(self.current_plot)))
        ax.scatter(x=x_axis, y=self.current_plot, c=color)
        ax.grid(b=True, color=self.COLOR_SILVER)

        if extra['first_row']:
            # only write the algorithm name in the first row
            ax.title.set_text(self.algorithm)

        if extra['last_row']:
            # only write window tick labels in the last row
            ax.set_xticklabels(self.__xticklabels())
        else:
            ax.set_xticklabels([])

        if extra['first_column']:
            ax.set_ylabel('Relative Difference')
        else:
            ax.set_yticklabels([])

        self.__set_lim(ax, ylim)

        # horizontal lines
        self.__plot_horizontal_line(ax, 0, self.COLOR_SILVER)
        avg = average(self.current_plot)
        self.__plot_horizontal_line(ax, avg, self.__color_code(avg))

        self.stats_box(ax, max(self.current_plot), avg, min(self.current_plot), self.COLOR_WHITE)

    @classmethod
    def plot_stats(cls, ax, ylim, error_threshold, values, extra):
        ax.grid(b=True, color=cls.COLOR_SILVER)

        if extra['first_row']:
            # only write 'STATS' in the first row
            ax.title.set_text("Threshold Stats")

        ax.set_xticklabels([])
        ax.set_yticklabels([])

        if extra['last_column']:
            ax.yaxis.set_label_position("right")
            ax.set_ylabel('Error Thresold = {}%'.format(error_threshold))

        cls.__set_lim(ax, ylim)

        # horizontal lines
        cls.__plot_horizontal_line(ax, 0, cls.COLOR_SILVER)
        cls.__plot_horizontal_line(ax, values['max'], cls.COLOR_BLUE)
        cls.__plot_horizontal_line(ax, values['avg'], cls.__color_code(values['avg']))
        cls.__plot_horizontal_line(ax, values['min'], cls.COLOR_BLUE)

        cls.stats_box(ax, values['max'], values['avg'], values['min'], cls.COLOR_WHEAT)

    @classmethod
    def __set_lim(cls, ax, ylim):
        ax.set_xlim(left=-1, right=7)
        ax.set_ylim(top=ylim, bottom=-ylim)

    @classmethod
    def stats_box(cls, ax, max_val, avg_val, min_val, facecolor):
        string = '\n'.join(('MAX = %.2f' % max_val, 'AVG = %.2f' % avg_val, 'MIN = %.2f' % min_val))
        props = dict(boxstyle='round', facecolor=facecolor, alpha=0.5)
        ax.text(0.45, 0.05, string, transform=ax.transAxes, fontsize=14, horizontalalignment='left', bbox=props, family='monospace')

    @classmethod
    def __color_code(cls, value):
        if value > 0:
            return cls.COLOR_GREEN
        elif value < 0:
            return cls.COLOR_RED
        else:  # value == 0
            return cls.COLOR_BLACK

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
        for index, value in enumerate(cls.WINDOWS):
            power = index + 2
            label = r"$2^{}$".format(power)  # 2^power
            xticklabels.append(label)
        return xticklabels

    @classmethod
    def __plot_horizontal_line(cls, ax, y, color):
        ax.axhline(y=y, color=color, linestyle='-', zorder=0)
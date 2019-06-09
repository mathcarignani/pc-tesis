import sys
sys.path.append('.')

from scripts.avances14.constants import Constants
from scripts.avances14.plot_utils import PlotUtils
from scripts.avances14.single_plot import SinglePlot
from scripts.avances15.plotter2_constants import Plotter2Constants


class RelativeDifferencePlot(object):
    def __init__(self, algorithm):
        self.algorithm = algorithm
        self.values = []

    def add_value(self, value0, value3):
        plot_value = 100 * SinglePlot.plot_value(value0, value3)
        self.values.append(plot_value)

    def close(self):
        assert(len(self.values) == len(Constants.THRESHOLDS))

    def min_max(self):
        return [min(self.values), max(self.values)]

    def plot(self, ax, ymin, ymax, extra):
        # self.__print()

        # scatter plot
        x_axis = list(xrange(len(self.values)))
        colors = [self.__color_code(item) for item in self.values]
        ax.scatter(x=x_axis, y=self.values, c=colors)
        ax.grid(b=True, color=Constants.COLOR_SILVER)
        ax.set_axisbelow(True)

        self.set_lim(ax, ymin, ymax)

        if extra['first_row']:
            ax.title.set_text(self.algorithm)
        if not extra['last_row']:
            ax.set_xticklabels([])
        if extra['first_column']:
            ax.set_ylabel('Relative Difference (%)')
        else:
            ax.set_yticklabels([])
        PlotUtils.hide_ticks(ax)

    def __print(self):
        print self.algorithm + " Relative Difference"
        print "self.values = " + str(self.values)

    @classmethod
    def set_lim(cls, ax, ymin, ymax):
        ax.set_xlim(left=-1, right=8)  # 8 thresholds
        ax.set_ylim(bottom=ymin, top=ymax)

    @classmethod
    def ylims(cls, total_min, total_max):
        if total_max > 0:
            total_max *= 1 + Plotter2Constants.Y_DIFF
        elif total_max == 0:
            total_max = Plotter2Constants.Y_DIFF
        else:  # total_max < 0
            total_max *= 1 - Plotter2Constants.Y_DIFF

        if total_min > 0:
            total_min -= (total_max - total_min) * Plotter2Constants.Y_DIFF
        elif total_min == 0:
            total_min = - Plotter2Constants.Y_DIFF
        else:  # total_min < 0
            total_min *= 1 + Plotter2Constants.Y_DIFF

        return total_min, total_max

    @classmethod
    def __color_code(cls, value):
        if value > 0:
            return Plotter2Constants.VALUE3_COLOR
        elif value < 0:
            return Plotter2Constants.VALUE0_COLOR
        else:  # value == 0
            return Plotter2Constants.VALUE_SAME

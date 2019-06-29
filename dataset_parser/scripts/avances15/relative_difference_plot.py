import sys
sys.path.append('.')

from scripts.avances14.constants import Constants
from scripts.avances14.plot_utils import PlotUtils
from scripts.avances14.single_plot import SinglePlot
from scripts.avances15.common_plot import CommonPlot
from scripts.avances15.plotter2_constants import Plotter2Constants


class RelativeDifferencePlot(CommonPlot):
    def __init__(self, algorithm, value3_smaller):
        self.algorithm = algorithm
        self.value3_smaller = value3_smaller
        self.values = []
        super(RelativeDifferencePlot, self).__init__()

    def add_value(self, value0, value3):
        values = (value0, value3) if self.value3_smaller else (value3, value0)
        plot_value = 100*SinglePlot.plot_value(*values)
        self.values.append(plot_value)

    def close(self):
        assert(len(self.values) == len(Constants.THRESHOLDS))

    def min_max(self):
        return [min(self.values), max(self.values)]

    def plot(self, ax, ymin, ymax, extra):
        self.print_values()

        # scatter plot
        x_axis = list(xrange(len(self.values)))
        colors = [self.color_code(item, self.value3_smaller) for item in self.values]
        ax.scatter(x=x_axis, y=self.values, c=colors)
        ax.grid(b=True, color=Constants.COLOR_SILVER)
        ax.set_axisbelow(True)

        self.set_lim(ax, ymin, ymax)

        if extra['first_row']:
            ax.title.set_text(self.algorithm)
        if not extra['last_row']:
            ax.set_xticklabels([])
        if extra['first_column']:
            ax.set_ylabel(Constants.RELATIVE_DIFF)
        else:
            ax.set_yticklabels([])
        ax.set_xticklabels([''] + Constants.THRESHOLDS)
        ax.set_xlabel(Constants.ERROR_THRE)
        PlotUtils.hide_ticks(ax)

    def print_values(self):
        print self.algorithm + " Relative Difference"
        print "self.values = " + str(self.values)
        min_value = min(self.values)
        max_value = max(self.values)
        if min_value < 0:
            print "min_value = " + str(min_value)
        if max_value > 0:
            print "max_value = " + str(max_value)

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

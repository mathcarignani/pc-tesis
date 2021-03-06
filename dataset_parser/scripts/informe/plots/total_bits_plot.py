import sys
sys.path.append('.')

from scripts.compress.experiments_utils import ExperimentsUtils
from scripts.informe.plot.plot_constants import PlotConstants
from scripts.informe.plot.plot_utils import PlotUtils
from scripts.informe.plots.common_plot import CommonPlot
from scripts.informe.plots.relative_difference_plot import RelativeDifferencePlot


class TotalBitsPlot(CommonPlot):
    def __init__(self, information):
        self.algorithm = information.get('algorithm')
        self.filename = information.get('filename')
        self.values0 = []
        self.values3 = []
        self.base_value0 = None
        super(TotalBitsPlot, self).__init__()

    def add_values(self, value0, value3, base_value0):
        self.base_value0 = base_value0 if self.base_value0 is None else self.base_value0
        assert(self.base_value0 == base_value0)  # check that base_value0 never changes

        self.values0.append(value0)
        self.values3.append(value3)

    def close(self):
        assert(len(self.values0) == len(ExperimentsUtils.THRESHOLDS))
        assert(len(self.values3) == len(ExperimentsUtils.THRESHOLDS))
        self.__check_sorted()

    def min_max(self):
        return [min([min(self.values0), min(self.values3)]), max([max(self.values0), max(self.values3)])]

    def plot(self, ax, ymin, ymax, extra_options):
        # self.print_values()

        # scatter plot
        x_axis = list(range(len(self.values0)))
        colors0, colors3 = self.generate_colors()
        ax.scatter(x=x_axis, y=self.values0, c=colors0, zorder=self.values0)
        ax.scatter(x=x_axis, y=self.values3, c=colors3, zorder=self.values3)
        ax.grid(b=True, color=PlotConstants.COLOR_SILVER)
        ax.set_axisbelow(True)

        if ymax >= self.base_value0:
            PlotUtils.horizontal_line(ax, self.base_value0, PlotConstants.COLOR_SILVER)

        RelativeDifferencePlot.set_lim(ax, ymin, ymax)

        if extra_options['first_row']:
            ax.title.set_text(self.algorithm)
        if not extra_options['last_row']:
            ax.set_xticklabels([])
        if extra_options['first_column']:
            ax.set_ylabel('Total Bits')
            self.format_x_ticks(ax)
        else:
            ax.set_yticklabels([])

    def print_values(self):
        print(self.algorithm + " Total Bits")
        print("self.values0 = " + str(self.values0))
        print("self.values3 = " + str(self.values3))

    def __check_sorted(self):
        if self.additional_checks:
            assert(PlotUtils.sorted_dec(self.values0))
            assert(PlotUtils.sorted_dec(self.values3))

    @classmethod
    def format_x_ticks(cls, ax):
        ylabels = [format(label, ',.0f') for label in ax.get_yticks()]
        ax.set_yticklabels(ylabels)

    @classmethod
    def ylims(cls, total_min, total_max):
        assert(total_min > 0)
        assert(total_max > 0)

        diff = total_max - total_min
        total_min = 0 if total_min > 0 else total_min - diff * PlotConstants.Y_DIFF
        return total_min, total_max + diff * PlotConstants.Y_DIFF

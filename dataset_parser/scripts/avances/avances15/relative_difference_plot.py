import sys
sys.path.append('.')

from scripts.compress.experiments_utils import ExperimentsUtils
from scripts.informe.plot.plot_constants import PlotConstants
from scripts.informe.plot.plot_utils import PlotUtils
from scripts.avances.avances14.single_plot import SinglePlot
from scripts.avances.avances15.common_plot import CommonPlot
from scripts.avances.avances15.plotter2_constants import Plotter2Constants
from scripts.avances.avances15.compression_ratio_plot import CompressionRatioPlot


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
        assert(len(self.values) == len(ExperimentsUtils.THRESHOLDS))

    def min_max(self):
        return [min(self.values), max(self.values)]

    def plot(self, ax, ymin, ymax, extra):
        # self.print_values()

        # scatter plot
        x_axis = list(xrange(len(self.values)))
        colors = [self.get_color_code(item) for item in self.values]
        ax.scatter(x=x_axis, y=self.values, c=colors)
        ax.grid(b=True, color=PlotConstants.COLOR_SILVER)
        ax.set_axisbelow(True)

        CommonPlot.set_lim(ax, ymin, ymax)

        if extra.get('first_row') or extra.get('show_title'):
            ax.title.set_text(self.algorithm)
        if not extra.get('last_row'):
            ax.set_xticklabels([])
        if extra.get('first_column') or extra.get('show_ylabel'):
            ax.set_ylabel(PlotConstants.RELATIVE_DIFF)
        else:
            ax.set_yticklabels([])
        ax.set_xticklabels([''] + ExperimentsUtils.THRESHOLDS)
        ax.set_xlabel(PlotConstants.ERROR_THRE)
        PlotUtils.hide_ticks(ax)

    @staticmethod
    def get_color_code(value):
        color = PlotConstants.COLOR_GRAY
        if value > 50.59:
            color = PlotConstants.COLOR_LIGHT_BLUE
        elif value < -0.28:
            color = PlotConstants.COLOR_RED
        return color

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

    ##############################################

    @staticmethod
    def create_plots(coders_array, panda_utils_0, panda_utils_3, col_index):
        plots_obj = {}
        total_min, total_max = sys.maxint, -sys.maxint
        for coder_name in coders_array:
            values0, _, _ = CompressionRatioPlot.get_values(coder_name, col_index, panda_utils_0)
            values3, _, _ = CompressionRatioPlot.get_values(coder_name, col_index, panda_utils_3)
            assert(len(values0) == len(values3))

            plot_instance = RelativeDifferencePlot(coder_name, True)
            for index, value0 in enumerate(values0):
                plot_instance.add_value(value0, values3[index])
            plot_instance.close()
            plots_obj[coder_name] = plot_instance

            coder_min, coder_max = plot_instance.min_max()
            total_min = coder_min if coder_min < total_min else total_min
            total_max = coder_max if coder_max > total_max else total_max

        # calculate and set ymin and ymax
        ymin, ymax = RelativeDifferencePlot.ylims(total_min, total_max)
        for coder in coders_array:
            plots_obj[coder].set_ymin_ymax(ymin, ymax)

        return plots_obj

    def set_ymin_ymax(self, ymin, ymax):
        self.ymin = ymin
        self.ymax = ymax

    def plot2(self, ax, extra):
        self.plot(ax, self.ymin, self.ymax, extra)

    ##############################################

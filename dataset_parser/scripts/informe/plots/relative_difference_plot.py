import sys
sys.path.append('.')

from matplotlib.patches import Ellipse
from scripts.compress.experiments_utils import ExperimentsUtils
from scripts.informe.plot.plot_constants import PlotConstants
from scripts.informe.plot.plot_utils import PlotUtils
from scripts.avances.avances14.single_plot import SinglePlot
from scripts.informe.plots.common_plot import CommonPlot
from scripts.informe.plots.compression_ratio_plot import CompressionRatioPlot


class RelativeDifferencePlot(CommonPlot):
    def __init__(self, algorithm, value3_smaller, options={}):
        self.algorithm = algorithm
        self.value3_smaller = value3_smaller
        self.options = options
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

    def plot(self, ax, ymin, ymax, extra_options={}):
        # self.print_values()
        extra_options.update(self.options); self.options = extra_options

        if self.options.get('check_never_negative'):
            assert(min(self.values) >= 0)

        # scatter plot
        x_axis = list(xrange(len(self.values)))
        colors = [self.get_color_code(_) for _ in self.values]
        ax.scatter(x=x_axis, y=self.values, c=colors, marker='x')
        ax.grid(b=True, color=PlotConstants.COLOR_SILVER)
        ax.set_axisbelow(True)
        ax.legend()

        if self.options.get('add_min_max_circles'):
            self._add_min_max_circles(ax)

        CommonPlot.set_lim(ax, ymin, ymax)
        self._labels(ax, self.options)

    #
    # This method is used to make a circle around the min/max values
    #
    def _add_min_max_circles(self, ax):
        maximum, minimum = max(self.values), min(self.values)
        if maximum > 50.59:
            circle = Ellipse((7, maximum), 1, 3.5, color=PlotConstants.VALUE0_COLOR, fill=False)
            ax.add_artist(circle)
        if minimum < -0.28:
            circle = Ellipse((7, minimum), 1, 0.02, color=PlotConstants.VALUE3_COLOR, fill=False)
            ax.add_artist(circle)

    def _labels(self, ax, options):
        CommonPlot.label_title(ax, options, self.algorithm)
        CommonPlot.label_y(ax, options, PlotConstants.RELATIVE_DIFF)
        CommonPlot.label_x(ax, options, PlotConstants.ERROR_THRE, [''] + ExperimentsUtils.THRESHOLDS)
        PlotUtils.hide_ticks(ax)

    @staticmethod
    def get_color_code(_):
        return PlotConstants.COLOR_BLACK

    def print_values(self):
        print self.algorithm + " Relative Difference"
        # print "self.values = " + str(self.values)
        min_value = min(self.values)
        max_value = max(self.values)
        if min_value < 0:
            print "min_value = " + str(min_value)
        if max_value > 0:
            print "max_value = " + str(max_value)

    @classmethod
    def ylims(cls, total_min, total_max):
        if total_max > 0:
            total_max *= 1 + PlotConstants.Y_DIFF
        elif total_max == 0:
            total_max = PlotConstants.Y_DIFF
        else:  # total_max < 0
            total_max *= 1 - PlotConstants.Y_DIFF

        if total_min > 0:
            total_min -= (total_max - total_min) * PlotConstants.Y_DIFF
        elif total_min == 0:
            total_min = - PlotConstants.Y_DIFF
        else:  # total_min < 0
            total_min *= 1 + PlotConstants.Y_DIFF

        return total_min, total_max

    ##############################################

    @staticmethod
    def create_plots(coders_array, panda_utils_0, panda_utils_3, col_index, options={}):
        plots_obj = {}
        total_min, total_max = sys.maxint, -sys.maxint
        for coder_name in coders_array:
            values0, _, _ = CompressionRatioPlot.get_values(coder_name, col_index, panda_utils_0)
            values3, _, _ = CompressionRatioPlot.get_values(coder_name, col_index, panda_utils_3)
            assert(len(values0) == len(values3))

            plot_instance = RelativeDifferencePlot(coder_name, True, options)
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

    def plot2(self, ax, options):
        self.plot(ax, self.ymin, self.ymax, options)

    ##############################################

import sys
sys.path.append('.')

from scripts.compress.experiments_utils import ExperimentsUtils
from scripts.informe.plot.plot_constants import PlotConstants
from scripts.informe.plot.plot_utils import PlotUtils
from scripts.informe.plots.common_plot import CommonPlot
from scripts.informe.plots.compression_ratio_plot import CompressionRatioPlot


class RelativeDifferencePlot(CommonPlot):
    def __init__(self, information, options={}):
        self.algorithm = information.get('algorithm')
        self.filename = information.get('filename')
        self.options = options
        self.values = []
        super(RelativeDifferencePlot, self).__init__()

    def add_value(self, value0, value3):
        plot_value = 100*CommonPlot.plot_value(value0, value3)
        self.values.append(plot_value)

    def close(self):
        assert(len(self.values) == len(ExperimentsUtils.THRESHOLDS))

    def min_max(self):
        return [min(self.values), max(self.values)]

    def plot(self, ax, ymin, ymax, extra_options={}):
        # self.print_values2()  # TODO: uncomment to print the window stats
        extra_options.update(self.options); self.options = extra_options

        self._check_values()

        # scatter plot
        x_axis = list(range(len(self.values)))
        colors = [self.get_color_code(_) for _ in self.values]
        ax.scatter(x=x_axis, y=self.values, c=colors, marker='x')
        ax.set_xticks(x_axis)
        ax.grid(b=True, color=PlotConstants.COLOR_SILVER, linestyle='dotted')
        ax.set_axisbelow(True)
        # ax.legend()

        if self.options.get('add_min_max_circles'):
            action = self.options['pdf_instance'].check_min_max(self.algorithm, self.values) # "PlotMax"/"PlotMin"/None
            CommonPlot.add_min_max_circles(ax, x_axis, self.values, action)
        if self.options.get('add_max_circle'):
            CommonPlot.add_max_circle(self.algorithm, self.options, ax, x_axis, self.values)

        CommonPlot.set_lim(ax, ymin, ymax)
        self._labels(ax, self.options)

    def _check_values(self):
        minimum = min(self.values)
        if minimum < 0 and self.options.get('check_never_negative'):
            raise(StandardError, "The values must be >= 0.")
            assert(minimum >= 0)

    def _labels(self, ax, options):
        CommonPlot.label_title(ax, options, self.algorithm)
        CommonPlot.label_y(ax, options, PlotConstants.RELATIVE_DIFF)
        CommonPlot.label_x(ax, options, PlotConstants.ERROR_THRE, ExperimentsUtils.THRESHOLDS)
        PlotUtils.hide_ticks(ax)

    @staticmethod
    def get_color_code(_):
        return PlotConstants.COLOR_BLACK

    def print_values(self):
        print(self.algorithm + " Relative Difference")
        # print "self.values = " + str(self.values)
        min_value, max_value = min(self.values), max(self.values)
        if min_value < 0:
            print("min_value = " + str(min_value))
        if max_value > 0:
            print("max_value = " + str(max_value))

    def print_values2(self):
        if max(self.values) == 0:
            return

        if self.filename == "vwc_1202.dat.csv" and self.algorithm == "CoderPCA":
            print("Filename,Algorithm,Threshold,Value,,>1,>2,>5")
        for i, value in enumerate(self.values):
            if value == 0:
                continue
            threshold = ExperimentsUtils.THRESHOLDS[i]
            str_value = str(value)
            if value > 5:
                extra_row = ['', '', str_value]
            elif value > 2:
                extra_row = ['', str_value, '']
            elif value > 1:
                extra_row = [str_value, '', '']
            else:
                extra_row = ['', '', '']
            extra_row_str = ",".join(extra_row)
            print(self.filename + "," + self.algorithm + "," + str(threshold) + "," + str_value + ",," + extra_row_str)

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
    def create_plots(coders_array, filename, panda_utils_NM, panda_utils_M, col_index, options={}):
        plots_obj = {}
        total_min, total_max = sys.maxsize, -sys.maxsize
        for coder_name in coders_array:
            values0, _, _ = CompressionRatioPlot.get_values(coder_name, col_index, panda_utils_NM)
            values3, _, _ = CompressionRatioPlot.get_values(coder_name, col_index, panda_utils_M)
            assert(len(values0) == len(values3))

            plot_instance = RelativeDifferencePlot({'algorithm': coder_name, 'filename': filename}, options)
            plot_instance.set_values(values0, values3)
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

    def set_values(self, values0, values3):
        for index, value0 in enumerate(values0):
            self.add_value(value0, values3[index])
        # TODO: uncomment to show stats for Table of Section 3.2 "Comparison of Masking and Non-Masking Variants"
        # self.show_stats()
        self.close()

    def show_stats(self):
        pos_count = len(list(filter(lambda x: (x > 0), self.values)))
        neg_count = len(list(filter(lambda x: (x < 0), self.values)))
        zero_count = len(list(filter(lambda x: (x == 0), self.values)))
        if zero_count > 0:
            print("ERROR: RDs do not match in our experiments")
            exit(1)
        if neg_count == 0:
            print("+++++++++++++++++++++++++++")
        elif pos_count == 0:
            print("---------------------------")
        else:
            print("RD > 0 => " + str(pos_count))
            print("RD < 0 => " + str(neg_count))
        print("===========================")

    def set_ymin_ymax(self, ymin, ymax):
        self.ymin = ymin
        self.ymax = ymax

    def plot2(self, ax, options):
        self.plot(ax, self.ymin, self.ymax, options)

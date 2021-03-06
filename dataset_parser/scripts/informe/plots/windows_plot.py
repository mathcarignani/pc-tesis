import sys
sys.path.append('.')

from scripts.compress.experiments_utils import ExperimentsUtils
from scripts.informe.plot.plot_constants import PlotConstants
from scripts.informe.plot.plot_utils import PlotUtils
from scripts.informe.plots.common_plot import CommonPlot


class WindowsPlot(CommonPlot):
    def __init__(self, information, options={}):
        self.algorithm = information.get('algorithm')
        self.filename = information.get('filename')
        self.options = options
        self.values0 = []
        self.values3 = []
        super(WindowsPlot, self).__init__()

    def close(self):
        total_thresholds = len(ExperimentsUtils.THRESHOLDS)
        if len(self.values0) > 0:
            assert(len(self.values0) == total_thresholds)
        assert(len(self.values3) == total_thresholds)
        self.__check_sorted()

    def plot(self, ax, extra_options={}):
        # self.print_values()
        extra_options.update(self.options); self.options = extra_options

        x_axis_0, y_axis_0, x_axis_3, y_axis_3 = [], [], [], []
        local_color, global_color = 'red', 'forestgreen'

        assert(len(self.values3) > 0)
        two_sets = len(self.values0) > 0

        if two_sets:
            for i, values in enumerate(zip(self.values0, self.values3)):
                value0, value3 = values
                pos_value0 = self.__position(value0)
                x_axis_0.append(i); y_axis_0.append(pos_value0)
                pos_value3 = self.__position(value3)
                x_axis_3.append(i); y_axis_3.append(pos_value3)
            label0, label3 = self.options.get('labels')
            ax.scatter(x=x_axis_3, y=y_axis_3, c=local_color, zorder=2, marker='.', label=label3, s=20)
            ax.scatter(x=x_axis_0, y=y_axis_0, c=global_color, zorder=1, marker='x', label=label0, s=36)
            # legend
            bbox_to_anchor = (0.45, 0.26, 0.55, 0.75) # (x0, y0, width, height)
            ax.legend(loc='upper right', bbox_to_anchor=bbox_to_anchor, fontsize='small', scatterpoints=1,
                      handlelength=0.3, ncol=2, edgecolor='black')
        else:
            for i, value3 in enumerate(self.values3):
                pos_value3 = self.__position(value3)
                x_axis_3.append(i); y_axis_3.append(pos_value3)

            x_axis = x_axis_3.copy()
            y_axis = y_axis_3.copy()
            size = len(x_axis)
            opt = self.options['pdf_instance'].add_data('window', self.algorithm, y_axis)
            CommonPlot.scatter_plot(ax, x_axis, y_axis, size, global_color, opt)

        ax.set_xticks(x_axis_3)
        ax.grid(b=True, color=PlotConstants.COLOR_SILVER, linestyle='dotted')
        ax.set_axisbelow(True)
        ax.set_yticks(list(range(len(y_axis_3))))
        top = len(ExperimentsUtils.WINDOWS)
        top = top + 1 if two_sets else top # +1 so that there's space for the legend
        ax.set_ylim(top=top, bottom=-1)
        self._labels(ax, self.options)

    def _labels(self, ax, options):
        CommonPlot.label_title(ax, options, self.algorithm)
        CommonPlot.label_y(ax, options, PlotConstants.WINDOW_SIZE, ExperimentsUtils.WINDOWS)
        CommonPlot.label_x(ax, options, PlotConstants.ERROR_THRE, ExperimentsUtils.THRESHOLDS)
        PlotUtils.hide_ticks(ax)

    def print_values(self):
        print(self.algorithm + " Windows")
        print("self.values0 = " + str(self.values0))
        print("self.values3 = " + str(self.values3))

    def __check_sorted(self):
        if self.additional_checks and self.algorithm != "CoderPCA":
            assert(PlotUtils.sorted(self.values0))
            assert(PlotUtils.sorted(self.values3))

    @classmethod
    def __position(cls, window):
        return ExperimentsUtils.WINDOWS.index(window)

    ##############################################

    @staticmethod
    def create_plots(coders_array, filename, panda_utils_NM, panda_utils_M, col_index, options={}):
        plots_obj = {}
        for coder_name in coders_array:
            values3 = WindowsPlot.get_values(coder_name, col_index, panda_utils_M)
            if panda_utils_NM is None:
                values0 = []
            else:
                values0 = WindowsPlot.get_values(coder_name, col_index, panda_utils_NM)
                assert(len(values0) == len(values3))

            plot_instance = WindowsPlot({'algorithm': coder_name, 'filename': filename}, options)
            plot_instance.set_values(values0, values3)
            plots_obj[coder_name] = plot_instance

        return plots_obj

    @staticmethod
    def get_values(coder_name, col_index, panda_utils):
        df = panda_utils.min_value_for_each_threshold(coder_name, col_index)
        values = df['window'].values
        return values

    def set_values(self, values0, values3):
        self.values0 = values0
        self.values3 = values3
        self.close()

    def plot2(self, ax, options):
        self.plot(ax, options)

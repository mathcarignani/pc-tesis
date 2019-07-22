import sys
sys.path.append('.')

from scripts.compress.experiments_utils import ExperimentsUtils
from scripts.informe.plot.plot_constants import PlotConstants
from scripts.informe.plot.plot_utils import PlotUtils
from scripts.avances.avances15.common_plot import CommonPlot
from scripts.avances.avances15.plotter2_constants import Plotter2Constants


class WindowsPlot(CommonPlot):
    def __init__(self, algorithm):
        self.algorithm = algorithm
        self.values0 = []
        self.values3 = []
        super(WindowsPlot, self).__init__()

    def add_values(self, window0, window3):
        self.values0.append(window0)
        self.values3.append(window3)

    def close(self):
        total_thresholds = len(ExperimentsUtils.THRESHOLDS)
        assert(len(self.values0) == total_thresholds)
        assert(len(self.values3) == total_thresholds)
        self.__check_sorted()

    def plot(self, ax, extra):
        # self.print_values()

        x_axis_0, y_axis_0, x_axis_3, y_axis_3, x_axis_same, y_axis_same = [], [], [], [], [], []
        for i, values in enumerate(zip(self.values0, self.values3)):
            value0, value3 = values
            pos_value0 = self.__position(value0)
            if value0 == value3:
                x_axis_same.append(i); y_axis_same.append(pos_value0)
            else:
                x_axis_0.append(i); y_axis_0.append(pos_value0)
                pos_value3 = self.__position(value3)
                x_axis_3.append(i); y_axis_3.append(pos_value3)

        ax.scatter(x=x_axis_0, y=y_axis_0, c=self.value0_color)
        ax.scatter(x=x_axis_3, y=y_axis_3, c=self.value3_color)
        ax.scatter(x=x_axis_same, y=y_axis_same, c=Plotter2Constants.VALUE_SAME)
        ax.grid(b=True, color=PlotConstants.COLOR_SILVER)
        ax.set_axisbelow(True)
        ax.set_ylim(top=len(ExperimentsUtils.WINDOWS), bottom=-1)

        if extra.get('first_column') or extra.get('show_ylabel'):
            ax.set_ylabel(PlotConstants.WINDOW_SIZE)
            ax.set_yticklabels([''] + ExperimentsUtils.WINDOWS)
        else:
            ax.set_yticklabels([])

        ax.set_xticklabels([''] + ExperimentsUtils.THRESHOLDS)
        ax.set_xlabel(PlotConstants.ERROR_THRE)
        PlotUtils.hide_ticks(ax)

    def print_values(self):
        print self.algorithm + " Windows"
        print "self.values0 = " + str(self.values0)
        print "self.values3 = " + str(self.values3)

    def __check_sorted(self):
        if self.additional_checks and self.algorithm != "CoderPCA":
            assert(PlotUtils.sorted(self.values0))
            assert(PlotUtils.sorted(self.values3))

    @classmethod
    def __position(cls, window):
        return ExperimentsUtils.WINDOWS.index(window)

    ##############################################

    @staticmethod
    def create_plots(coders_array, panda_utils_0, panda_utils_3, col_index):
        plots_obj = {}
        for coder_name in coders_array:
            values0 = WindowsPlot.get_values(coder_name, col_index, panda_utils_0)
            values3 = WindowsPlot.get_values(coder_name, col_index, panda_utils_3)
            assert(len(values0) == len(values3))

            plot_instance = WindowsPlot(coder_name)
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

    def plot2(self, ax, extra):
        self.plot(ax, extra)

    ##############################################

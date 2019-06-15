import sys
sys.path.append('.')

from scripts.avances14.constants import Constants
from scripts.avances14.plot_utils import PlotUtils
from scripts.avances15.common_plot import CommonPlot
from scripts.avances15.plotter2_constants import Plotter2Constants


class WindowsPlot(CommonPlot):
    def __init__(self, algorithm):
        self.algorithm = algorithm
        self.windows0 = []
        self.windows3 = []
        super(WindowsPlot, self).__init__()

    def add_values(self, window0, window3):
        self.windows0.append(window0)
        self.windows3.append(window3)

    def close(self):
        total_thresholds = len(Constants.THRESHOLDS)
        assert(len(self.windows0) == total_thresholds)
        assert(len(self.windows3) == total_thresholds)
        self.__check_sorted()

    def plot(self, ax, extra):
        # self.print_values()

        x_axis_0, y_axis_0, x_axis_3, y_axis_3, x_axis_same, y_axis_same = [], [], [], [], [], []
        for i, values in enumerate(zip(self.windows0, self.windows3)):
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
        ax.grid(b=True, color=Constants.COLOR_SILVER)
        ax.set_axisbelow(True)
        ax.set_xticklabels([''] + Constants.THRESHOLDS)

        ax.set_ylim(top=len(Constants.WINDOWS), bottom=-1)

        if extra['last_row']:
            ax.set_xlabel('Error Threshold (%)')
        if extra['first_column']:
            ax.set_ylabel('Window Size')
            ax.set_yticklabels([''] + Constants.WINDOWS)
        else:
            ax.set_yticklabels([])
        PlotUtils.hide_ticks(ax)

    def print_values(self):
        print self.algorithm + " Windows"
        print "self.windows0 = " + str(self.windows0)
        print "self.windows3 = " + str(self.windows3)

    def __check_sorted(self):
        if self.additional_checks and self.algorithm != "CoderPCA":
            assert(PlotUtils.sorted(self.windows0))
            assert(PlotUtils.sorted(self.windows3))

    @classmethod
    def __position(cls, window):
        return Constants.WINDOWS.index(window)

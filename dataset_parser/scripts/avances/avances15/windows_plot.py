import sys
sys.path.append('.')

from scripts.compress.experiments_utils import ExperimentsUtils
from scripts.informe.plot.plot_constants import PlotConstants
from scripts.informe.plot.plot_utils import PlotUtils
from scripts.avances.avances15.common_plot import CommonPlot
from scripts.avances.avances15.plotter2_constants import Plotter2Constants


class WindowsPlot(CommonPlot):
    def __init__(self, algorithm, options={}):
        self.algorithm = algorithm
        self.options = options
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

    def plot(self, ax, extra_options={}):
        # self.print_values()
        extra_options.update(self.options); self.options = extra_options

        print self.values0
        print self.values3
        print 'chau'
        x_axis_0, y_axis_0, x_axis_3, y_axis_3, x_axis_same, y_axis_same = [], [], [], [], [], []

        if len(self.values0) > 0:
            for i, values in enumerate(zip(self.values0, self.values3)):
                value0, value3 = values
                pos_value0 = self.__position(value0)
                # if value0 == value3:
                #     x_axis_same.append(i); y_axis_same.append(pos_value0)
                # else:
                x_axis_0.append(i); y_axis_0.append(pos_value0)
                pos_value3 = self.__position(value3)
                x_axis_3.append(i); y_axis_3.append(pos_value3)
        else:
            for i, value3 in enumerate(self.values3):
                pos_value3 = self.__position(value3)
                x_axis_3.append(i); y_axis_3.append(pos_value3)

        label0, label3 = self.options.get('labels')
        ax.scatter(x=x_axis_0, y=y_axis_0, c=self.value0_color, zorder=2, label=label0)  # global
        ax.scatter(x=x_axis_3, y=y_axis_3, c=self.value3_color, zorder=1, label=label3)
        # ax.scatter(x=x_axis_same, y=y_axis_same, c=Plotter2Constants.VALUE_SAME)

        ax.legend(loc='lower right', bbox_to_anchor=(0.5, 0., 0.48, 0.95), fontsize='small', scatterpoints=1,
                  handlelength=0.5)  # labelspacing=0.5, borderpad=0.7

        ax.grid(b=True, color=PlotConstants.COLOR_SILVER)
        ax.set_axisbelow(True)
        ax.set_ylim(top=len(ExperimentsUtils.WINDOWS), bottom=-1)

        self._labels(ax, self.options)

        # ax.set_xticklabels([''] + ExperimentsUtils.THRESHOLDS)
        # ax.set_xlabel(PlotConstants.ERROR_THRE)
        PlotUtils.hide_ticks(ax)

    def _labels(self, ax, options):
        if options['title']:
            ax.title.set_text(self.algorithm)
        if self.options.get('first_column') or self.options.get('show_ylabel'):
            ax.set_ylabel(PlotConstants.WINDOW_SIZE)
            ax.set_yticklabels([''] + ExperimentsUtils.WINDOWS)
        else:
            ax.set_yticklabels([])
        if not options.get('last_row'):
            ax.set_xticklabels([])

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
    def create_plots(coders_array, panda_utils_0, panda_utils_3, col_index, options={}):
        plots_obj = {}
        for coder_name in coders_array:
            values3 = WindowsPlot.get_values(coder_name, col_index, panda_utils_3)
            if panda_utils_0 is None:
                values0 = []
            else:
                values0 = WindowsPlot.get_values(coder_name, col_index, panda_utils_0)
                assert(len(values0) == len(values3))

            plot_instance = WindowsPlot(coder_name, options)
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
        if len(values0) > 0:
            self.close()

    def plot2(self, ax, options):
        self.plot(ax, options)

    ##############################################

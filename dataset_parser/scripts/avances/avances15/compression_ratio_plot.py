#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.append('.')

from scripts.compress.experiments_utils import ExperimentsUtils
from scripts.informe.math_utils import MathUtils
from scripts.informe.plot.plot_constants import PlotConstants
from scripts.informe.plot.plot_utils import PlotUtils
from scripts.avances.avances15.common_plot import CommonPlot
from scripts.avances.avances15.plotter2_constants import Plotter2Constants
from scripts.informe.results_parsing.results_to_dataframe import ResultsToDataframe

# To make the latex math text look like the other text
# https://stackoverflow.com/a/27697390/4547232
import matplotlib
matplotlib.rcParams['mathtext.fontset'] = 'custom'
matplotlib.rcParams['mathtext.rm'] = 'Bitstream Vera Sans'
matplotlib.rcParams['mathtext.it'] = 'Bitstream Vera Sans'  # 'Bitstream Vera Sans:italic'
matplotlib.rcParams['mathtext.bf'] = 'Bitstream Vera Sans'  # 'Bitstream Vera Sans:bold'


class CompressionRatioPlot(CommonPlot):
    def __init__(self, algorithm):
        self.algorithm = algorithm
        self.values0 = []
        self.values3 = []
        self.basic_value0 = None
        super(CompressionRatioPlot, self).__init__()

    def add_values(self, value0, value3, basic_value0):
        self.basic_value0 = basic_value0 if self.basic_value0 is None else self.basic_value0
        assert(self.basic_value0 == basic_value0)  # check that basic_value0 never changes

        value0 = MathUtils.calculate_percentage(basic_value0, value0, 5)
        value3 = MathUtils.calculate_percentage(basic_value0, value3, 5)
        self.values0.append(value0)
        self.values3.append(value3)

    def close(self):
        assert(len(self.values0) == len(ExperimentsUtils.THRESHOLDS))
        assert(len(self.values3) == len(ExperimentsUtils.THRESHOLDS))
        self.__check_sorted()

    def min_max(self):
        return [min([min(self.values0), min(self.values3)]), max([max(self.values0), max(self.values3)])]

    def plot(self, ax, ymin, ymax, extra):
        # self.print_values()

        # scatter plot
        x_axis = list(xrange(len(self.values3)))
        if len(self.values0) > 0:
            colors0, colors3 = self.generate_colors()
            zorders0, zorders3 = self.__generate_zorders()
            ax.scatter(x=x_axis, y=self.values0, c=colors0, zorder=zorders0)
            ax.scatter(x=x_axis, y=self.values3, c=colors3, zorder=zorders3)
        else:
            ax.scatter(x=x_axis, y=self.values3, c=self.value3_color)

        ax.grid(b=True, color=PlotConstants.COLOR_SILVER)
        ax.set_axisbelow(True)

        if ymax >= 100:
            PlotUtils.horizontal_line(ax, 100, PlotConstants.COLOR_SILVER)

        CommonPlot.set_lim(ax, ymin, ymax)

        # TODO: improve
        if True:
            ax.title.set_text(self.algorithm)
        if not extra.get('last_row'):
            ax.set_xticklabels([])
        if extra.get('first_column') or extra.get('show_ylabel'):
            ax.set_ylabel(PlotConstants.COMPRESSION_RATIO)
            self.format_x_ticks(ax)
        else:
            ax.set_yticklabels([])
        PlotUtils.hide_ticks(ax)

    def print_values(self):
        print self.algorithm + " Compression Ratio"
        print "self.values0 = " + str(self.values0)
        print "self.values3 = " + str(self.values3)

    def __generate_zorders(self):
        zorders0 = []
        for index, value0 in enumerate(self.values0):
            zorder0 = 1 if value0 > self.values3[index] else -1
            zorders0.append(zorder0)
        zorders3 = [-val for val in zorders0]
        return zorders0, zorders3

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
        total_min = 0 if total_min > 0 else total_min - diff * Plotter2Constants.Y_DIFF
        return total_min, total_max + diff * Plotter2Constants.Y_DIFF

    ##############################################

    @staticmethod
    def create_plots(coders_array, panda_utils_0, panda_utils_3, col_index):
        plots_obj = {}
        total_min, total_max = sys.maxint, -sys.maxint
        for coder_name in coders_array:
            values3, min3, max3 = CompressionRatioPlot.get_values(coder_name, col_index, panda_utils_3)

            if panda_utils_0 is None:
                values0, min0, max0 = [], min3, max3
            else:
                values0, min0, max0 = CompressionRatioPlot.get_values(coder_name, col_index, panda_utils_0)
                assert(len(values0) == len(values3))

            min03, max03 = min([min0, min3]), max([max0, max3])
            total_min = min03 if min03 < total_min else total_min
            total_max = max03 if max03 > total_max else total_max

            plot_instance = CompressionRatioPlot(coder_name)
            plot_instance.set_values(values0, values3)
            plots_obj[coder_name] = plot_instance

        # calculate and set ymin and ymax
        ymin, ymax = CompressionRatioPlot.ylims(total_min, total_max)
        for coder in coders_array:
            plots_obj[coder].set_ymin_ymax(ymin, ymax)

        return plots_obj

    @staticmethod
    def get_values(coder_name, col_index, panda_utils):
        percentage_column_key = ResultsToDataframe.percentage_column_key(col_index)
        df = panda_utils.min_value_for_each_threshold(coder_name, col_index)
        values = df[percentage_column_key].values
        df_min = df[percentage_column_key].min()
        df_max = df[percentage_column_key].max()
        return values, df_min, df_max

    def set_values(self, values0, values3):
        self.values0 = values0
        self.values3 = values3
        if len(values0) > 0:
            self.close()

    def set_ymin_ymax(self, ymin, ymax):
        self.ymin = ymin
        self.ymax = ymax

    def plot2(self, ax, extra):
        self.plot(ax, self.ymin, self.ymax, extra)

    ##############################################

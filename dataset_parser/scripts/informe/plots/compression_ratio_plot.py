#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.append('.')

from scripts.compress.experiments_utils import ExperimentsUtils
from scripts.informe.plot.plot_constants import PlotConstants
from scripts.informe.plot.plot_utils import PlotUtils
from scripts.informe.plots.common_plot import CommonPlot
from scripts.informe.results_parsing.results_to_dataframe import ResultsToDataframe

# To make the latex math text look like the other text
# https://stackoverflow.com/a/27697390/4547232
import matplotlib
matplotlib.rcParams['mathtext.fontset'] = 'custom'
matplotlib.rcParams['mathtext.rm'] = 'Bitstream Vera Sans'
matplotlib.rcParams['mathtext.it'] = 'Bitstream Vera Sans'  # 'Bitstream Vera Sans:italic'
matplotlib.rcParams['mathtext.bf'] = 'Bitstream Vera Sans'  # 'Bitstream Vera Sans:bold'


class CompressionRatioPlot(CommonPlot):
    def __init__(self, information, options={}):
        self.algorithm = information.get('algorithm')
        self.filename = information.get('filename')
        self.options = options
        self.values0 = []
        self.values3 = []
        self.base_value0 = None
        super(CompressionRatioPlot, self).__init__()

    def close(self):
        total_thresholds = len(ExperimentsUtils.THRESHOLDS)
        if len(self.values0) > 0:
            assert(len(self.values0) == total_thresholds)
        assert(len(self.values3) == total_thresholds)
        self.__check_sorted()

    def min_max(self):
        return [min([min(self.values0), min(self.values3)]), max([max(self.values0), max(self.values3)])]

    def plot(self, ax, ymin, ymax, extra_options={}):
        # self.print_values()
        extra_options.update(self.options); self.options = extra_options

        assert(len(self.values3) > 0)
        two_sets = len(self.values0) > 0

        # scatter plot
        x_axis = list(range(len(self.values3)))
        if two_sets:
            colors0, colors3 = self.generate_colors(False)
            label0, label3 = self.options.get('labels')
            ax.scatter(x=x_axis, y=self.values0, c=colors0, zorder=1, marker='x', label=label0, s=36)
            ax.scatter(x=x_axis, y=self.values3, c=colors3, zorder=2, marker='.', label=label3, s=10)
            ax.legend(loc='upper right', bbox_to_anchor=(0.5, 0., 0.48, 0.95), fontsize='small', edgecolor='black',
                      scatterpoints=1, handlelength=1)
        else:
            y_axis = self.values3
            size = len(y_axis)
            x_axis = list(range(size))
            opt = self.options['pdf_instance'].add_data('compression', self.algorithm, y_axis)
            CommonPlot.scatter_plot(ax, x_axis, y_axis, size, PlotConstants.COLOR_BLACK, opt)

        ax.set_xticks(x_axis)
        ax.grid(b=True, color=PlotConstants.COLOR_SILVER, linestyle='dotted', zorder=0)
        ax.set_axisbelow(True)

        if ymax >= 100:
            PlotUtils.horizontal_line(ax, 100, PlotConstants.COLOR_SILVER)

        CommonPlot.set_lim(ax, ymin, ymax)
        self._labels(ax, self.options)

    def _labels(self, ax, options):
        CommonPlot.label_title(ax, options, self.algorithm)
        tick_labels = self.ytick_labels(ax)
        CommonPlot.label_y(ax, options, PlotConstants.COMPRESSION_RATIO, tick_labels)
        CommonPlot.label_x(ax, options, PlotConstants.ERROR_THRE, ExperimentsUtils.THRESHOLDS)
        PlotUtils.hide_ticks(ax)

    @classmethod
    def ytick_labels(cls, ax):
        tick_labels = [format(label, ',.0f') for label in ax.get_yticks()]
        new_tick_labels = []
        for tick_label in tick_labels:
            if tick_label == '0':
                new_tick_label = '0'
            else:
                tick_label = tick_label.replace(",", "")
                new_tick_label = str(float(tick_label) / 100) # '20' => '0.2'
            new_tick_labels.append(new_tick_label)
        return new_tick_labels

    # def print_values(self):
    #     print(self.algorithm + " Compression Ratio")
    #     print("self.values0 = " + str(self.values0))
    #     print("self.values3 = " + str(self.values3))

    def __check_sorted(self):
        if not self.additional_checks:
            return
        assert(PlotUtils.sorted_dec(self.values0))
        assert(PlotUtils.sorted_dec(self.values3))

    @classmethod
    def ylims(cls, total_min, total_max):
        assert(total_min > 0)
        assert(total_max > 0)

        diff = total_max - total_min
        total_min = 0 if total_min > 0 else total_min - diff * PlotConstants.Y_DIFF
        return total_min, total_max + diff * PlotConstants.Y_DIFF

    ##############################################

    @staticmethod
    def create_plots(coders_array, filename, panda_utils_NM, panda_utils_M, col_index, options={}):
        plots_obj = {}
        total_min, total_max = sys.maxsize, -sys.maxsize
        for coder_name in coders_array:
            values3, min3, max3 = CompressionRatioPlot.get_values(coder_name, col_index, panda_utils_M)

            if panda_utils_NM is None:
                values0, min0, max0 = [], min3, max3
            else:
                values0, min0, max0 = CompressionRatioPlot.get_values(coder_name, col_index, panda_utils_NM)
                assert(len(values0) == len(values3))

            min03, max03 = min([min0, min3]), max([max0, max3])
            total_min = min03 if min03 < total_min else total_min
            total_max = max03 if max03 > total_max else total_max

            plot_instance = CompressionRatioPlot({'algorithm': coder_name, 'filename': filename}, options)
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
        # print panda_utils.df
        df = panda_utils.min_value_for_each_threshold(coder_name, col_index)
        values = df[percentage_column_key].values
        df_min = df[percentage_column_key].min()
        df_max = df[percentage_column_key].max()
        return values, df_min, df_max

    def set_values(self, values0, values3):
        self.values0 = values0
        self.values3 = values3
        self.close()

    def set_ymin_ymax(self, ymin, ymax):
        self.ymin = ymin
        self.ymax = ymax

    def plot2(self, ax, options):
        self.plot(ax, self.ymin, self.ymax, options)

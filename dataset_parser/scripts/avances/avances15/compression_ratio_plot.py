#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.append('.')

from scripts.compress.experiments_utils import ExperimentsUtils
from scripts.informe.math_utils import MathUtils
from scripts.informe.plot.plot_constants import PlotConstants
from scripts.informe.plot.plot_utils import PlotUtils
from scripts.avances.avances15.common_plot import CommonPlot
from scripts.avances.avances15 import Plotter2Constants
from scripts.avances.avances15 import RelativeDifferencePlot

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
        x_axis = list(xrange(len(self.values0)))
        colors0, colors3 = self.generate_colors()
        ax.scatter(x=x_axis, y=self.values0, c=colors0, zorder=self.values0)
        ax.scatter(x=x_axis, y=self.values3, c=colors3, zorder=self.values3)
        ax.grid(b=True, color=PlotConstants.COLOR_SILVER)
        ax.set_axisbelow(True)

        if ymax >= 100:
            PlotUtils.horizontal_line(ax, 100, PlotConstants.COLOR_SILVER)

        RelativeDifferencePlot.set_lim(ax, ymin, ymax)

        if extra['first_row']:
            ax.title.set_text(self.algorithm)
        if not extra['last_row']:
            ax.set_xticklabels([])
        if extra['first_column']:
            ax.set_ylabel(PlotConstants.COMPRESSION_RATIO)
            self.format_x_ticks(ax)
        else:
            ax.set_yticklabels([])
        PlotUtils.hide_ticks(ax)

    def print_values(self):
        print self.algorithm + " Compression Ratio"
        print "self.values0 = " + str(self.values0)
        print "self.values3 = " + str(self.values3)

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

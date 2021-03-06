import sys
sys.path.append('.')

import numpy as n
import matplotlib.pyplot as plt
import matplotlib.markers as mmarkers
from scripts.informe.plot.plot_constants import PlotConstants


class CommonPlot(object):
    def __init__(self):
        # TODO: the following two values are exchanged
        self.value0_color = PlotConstants.VALUE3_COLOR
        self.value3_color = PlotConstants.VALUE0_COLOR
        self.additional_checks = False

    def set_colors(self, value0_color, value3_color):
        self.value0_color = value0_color or self.value0_color
        self.value3_color = value3_color or self.value3_color

    def color_code(self, value, value3_smaller=True):
        if value > 0:
            return self.value3_color if value3_smaller else self.value0_color
        elif value < 0:
            return self.value0_color if value3_smaller else self.value3_color
        else:  # value == 0
            return PlotConstants.VALUE_SAME

    def generate_colors(self, can_be_equal=True):
        colors0, colors3 = [], []
        for value0, value3 in zip(self.values0, self.values3):
            if can_be_equal and value0 == value3:
                colors0.append(PlotConstants.VALUE_SAME)
                colors3.append(PlotConstants.VALUE_SAME)
            else:
                colors0.append(self.value0_color)
                colors3.append(self.value3_color)
        return colors0, colors3

    @classmethod
    def plot_value(cls, value0, value3):
        dividend = value0 - value3
        value = float(dividend) / float(value0) if dividend != 0 else 0
        return value

    @classmethod
    def set_lim(cls, ax, ymin, ymax):
        ax.set_ylim(bottom=ymin, top=ymax)

    @classmethod
    def label_title(cls, ax, options, title):
        title_options = options.get('title')
        if title_options:
            fontsize = 15 if isinstance(title_options, bool) else title_options
            title = title.replace("Coder", "")  # "CoderABC" => "ABC"
            title = title.replace("GAMPSLimit", "GAMPS")
            ax.set_title(title, fontsize=fontsize)

    @classmethod
    def label_y(cls, ax, options, label, tick_labels=None):
        if not options.get('show_ylabel'):
            ax.set_yticklabels([])
            return
        ax.set_ylabel(label)
        if tick_labels is not None:
            ax.set_yticklabels(tick_labels)

    @classmethod
    def label_x(cls, ax, options, label, tick_labels=None):
        if not options.get('show_xlabel'):
            ax.set_xticklabels([])
            return
        ax.set_xlabel(label)
        if tick_labels is not None:
            ax.set_xticklabels(tick_labels)

    ####################################################################################################################

    #
    # SOURCE: https://stackoverflow.com/a/52303895/4547232
    #
    @classmethod
    def change_scatter_markers(cls, sc, markers):
        paths = []
        for marker in markers:
            if isinstance(marker, mmarkers.MarkerStyle):
                marker_obj = marker
            else:
                marker_obj = mmarkers.MarkerStyle(marker)
            path = marker_obj.get_path().transformed(marker_obj.get_transform())
            paths.append(path)
        sc.set_paths(paths)

    @classmethod
    def scatter_plot(cls, ax, x_axis, y_axis, size, color, opt=None):
        x_axis = list(x_axis)
        y_axis = list(y_axis)
        colors = [color] * size
        facecolors, edgecolors = colors.copy(), colors.copy()
        sizes = [plt.rcParams['lines.markersize'] ** 2] * size
        markers = ['x'] * size

        if opt and len(opt.keys()) > 0:
            for idx, key in enumerate(opt['keys']):
                # shift the index a number of times equal to the number of values previously inserted
                index = opt['indexes'][idx] + idx
                value_color = opt.get('color')
                colors = colors[:index] + ['none'] + colors[index:]
                facecolors.insert(index, 'none')
                sizes = sizes[:index] + [200] + sizes[index:]
                markers = markers[:index] + ['o'] + markers[index:]
                edgecolors = edgecolors[:index] + [value_color] + edgecolors[index:]
                x_axis = x_axis[:index] + [x_axis[index]] + x_axis[index:]
                y_axis = y_axis[:index] + [y_axis[index]] + y_axis[index:]

        sc = ax.scatter(x=x_axis, y=y_axis, c=colors, facecolors=facecolors, sizes=sizes, edgecolors=edgecolors)
        CommonPlot.change_scatter_markers(sc, markers)

import sys
sys.path.append('.')

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
    def set_lim(cls, ax, ymin, ymax):
        ax.set_xlim(left=-1, right=8)  # 8 thresholds
        ax.set_ylim(bottom=ymin, top=ymax)

    @classmethod
    def label_title(cls, ax, options, title):
        if options.get('title'):
            ax.title.set_text(title)

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

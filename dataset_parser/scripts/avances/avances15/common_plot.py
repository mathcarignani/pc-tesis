import sys
sys.path.append('.')

from scripts.avances.avances15.plotter2_constants import Plotter2Constants


class CommonPlot(object):
    def __init__(self):
        self.value0_color = Plotter2Constants.VALUE0_COLOR
        self.value3_color = Plotter2Constants.VALUE3_COLOR
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
            return Plotter2Constants.VALUE_SAME

    def generate_colors(self):
        colors0, colors3 = [], []
        for value0, value3 in zip(self.values0, self.values3):
            if value0 == value3:
                colors0.append(Plotter2Constants.VALUE_SAME)
                colors3.append(Plotter2Constants.VALUE_SAME)
            else:
                colors0.append(self.value0_color)
                colors3.append(self.value3_color)
        return colors0, colors3

    @classmethod
    def set_lim(cls, ax, ymin, ymax):
        ax.set_xlim(left=-1, right=8)  # 8 thresholds
        ax.set_ylim(bottom=ymin, top=ymax)

import sys
sys.path.append('.')

# import matplotlib
import numpy as np
import matplotlib.pyplot as plt
from scripts.informe.plot.plot_constants import PlotConstants
import math

plt.rcParams["mathtext.fontset"] = "cm"

class PWLHExample(object):
    LABEL_ORIG = 'original value'
    LABEL_DECO = 'encoded value'
    COLOR_ORIG = 'navy'
    COLOR_DECO = 'orange'
    COLOR_LINE = 'seagreen'
    YLABEL = 'value'
    XLABEL = 'time'
    PATH = '/Users/pablocerve/Documents/FING/Proyecto/pc-tesis/dataset_parser/scripts/informe/examples/pwlh/'
    SMAX_MAR = 0.06
    SMIN_MAR = 0.1
    LOW_ALPHA = 0.3
    LOWER_ALPHA = 0.2

    def __init__(self):
        self.original = [1, 1, 1, 1, 1, 2, 3, 3, 4, 2, 1, 1]
        self.decoded =  [0, 1, 1, 1, 2, 2, 3, 3, 3, 2, 1, 1]
        self.copy_decoded = list.copy(self.decoded)
        self.plot_values = []
        self.plot_values_alpha = []
        self.xs, self.ys, self.words = [], [], []
        self.convex_hull = []
        self.convex_hull_lines = []
        self.convex_hull_width = []

        self.index = 0
        self.pwlh1("pwlh1.pdf", 1)
        self.index = 1
        self.pwlh2("pwlh2.pdf", 2)
        self.index = 4
        self.pwlh3("pwlh3.pdf", 5)
        self.index = 5
        self.pwlh4("pwlh4.pdf", 6)
        self.index = 6
        self.pwlh5("pwlh5.pdf", 7)
        self.index = 7
        self.pwlh6("pwlh6.pdf", 8)
        self.index = 8
        self.pwlh7("pwlh7.pdf", 9)
        self.index = 9
        self.pwlh8("pwlh8.pdf", 10)
        self.index = 9
        self.pwlh9("pwlh9.pdf", 11)


    def pwlh1(self, filename, step):
        self.decoded = []
        self.convex_hull = [(0,1)]
        self.convex_hull_lines = []
        self.common(filename, step)

    def pwlh2(self, filename, step):
        self.convex_hull = [(0,1), (1,1)]
        self.convex_hull_lines = [{'x_values': [0,1], 'y_values': [1,1]}]
        self.xs = [0]
        self.ys = [0.65]
        self.words = [r"width$=0$"]
        self.common(filename, step)

    def pwlh3(self, filename, step):
        self.convex_hull = [(0,1), (4,1)]
        self.convex_hull_lines = [{'x_values': [0,4], 'y_values': [1,1]}]
        self.xs = [1.5]
        self.ys = [0.65]
        self.words = [r"width$=0$"]
        self.common(filename, step)

    def pwlh4(self, filename, step):
        self.convex_hull = [(0,1), (5,2), (4,1)]
        self.convex_hull_lines = [
            {'x_values': [0,4], 'y_values': [1,1]},
            {'x_values': [0,5], 'y_values': [1,2]},
            {'x_values': [4,5], 'y_values': [1,2]}
        ]
        # intersection
        _, _, real_distance = PWLHExample.calculate_intersection([(0,1), (5*60,2)], (4*60,1))
        assert(round(real_distance, 1) == 0.8)
        x, y, distance = PWLHExample.calculate_intersection([(0,1), (5,2)], (4,1))
        self.convex_hull_width = [{'x_values': [x,4], 'y_values': [y, 1]}]
        self.xs = [x - 0.7]
        self.ys = [y + 0.15]
        self.words = [r"width$\approx" + str(round(real_distance, 1)) + r"$"]
        self.common(filename, step)

    def pwlh5(self, filename, step):
        self.convex_hull = [(0,1), (6,3), (4,1)]
        self.convex_hull_lines = [
            {'x_values': [0,4], 'y_values': [1,1]},
            {'x_values': [0,6], 'y_values': [1,3]},
            {'x_values': [4,6], 'y_values': [1,3]}
        ]
        # intersection
        _, _, real_distance = PWLHExample.calculate_intersection([(0,1), (6*60,3)], (4*60,1))
        assert(round(real_distance, 2) == 1.33)
        x, y, distance = PWLHExample.calculate_intersection([(0,1), (6,3)], (4,1))
        self.convex_hull_width = [{'x_values': [x,4], 'y_values': [y, 1]}]
        self.xs = [x - 1.05]
        self.ys = [y + 0.15]
        self.words = [r"width$\approx" + str(round(real_distance, 1)) + r"$"]
        self.common(filename, step)

    def pwlh6(self, filename, step):
        self.convex_hull = [(0,1), (6,3), (7,3), (4,1)]
        self.convex_hull_lines = [
            {'x_values': [0,4], 'y_values': [1,1]},
            {'x_values': [0,6], 'y_values': [1,3]},
            {'x_values': [4,7], 'y_values': [1,3]},
            {'x_values': [6,7], 'y_values': [3,3]}
        ]
        self.common(filename, step)

    def pwlh7(self, filename, step):
        self.convex_hull = [(0,1), (8,4), (7,3), (4,1)]
        self.convex_hull_lines = [
            {'x_values': [0,4], 'y_values': [1,1]},
            {'x_values': [0,8], 'y_values': [1,4]},
            {'x_values': [4,7], 'y_values': [1,3]},
            {'x_values': [7,8], 'y_values': [3,4]}
        ]
        # intersection
        _, _, real_distance = PWLHExample.calculate_intersection([(0,1), (8*60,4)], (4*60,1))
        assert(round(real_distance, 1) == 1.5)
        x, y, distance = PWLHExample.calculate_intersection([(0,1), (8,4)], (4,1))
        self.convex_hull_width = [{'x_values': [x,4], 'y_values': [y, 1]}]
        self.xs = [x - 1]
        self.ys = [y + 0.15]
        self.words = [r"width$\approx" + str(round(real_distance, 1)) + r"$"]
        self.common(filename, step)

    def pwlh8(self, filename, step):
        self.convex_hull = [(0,1), (8,4), (9,2), (4,1)]

        self.convex_hull_lines = [
            {'x_values': [0,4], 'y_values': [1,1]},
            {'x_values': [0,8], 'y_values': [1,4]},
            {'x_values': [8,10],'y_values': [4,10*(3/8)+1], 'alpha': self.LOW_ALPHA}, # continue line
            {'x_values': [4,9], 'y_values': [1,2]},
            {'x_values': [9,8], 'y_values': [2,4]},
            {'x_values': [9,7], 'y_values': [2,-7*(2/1)+20], 'alpha': self.LOW_ALPHA}, # continue line
        ]
        # intersections
        _, _, real_distance = PWLHExample.calculate_intersection([(0,1), (8*60,4)], (9*60,2))
        assert(round(real_distance, 3) == 2.375)
        x, y, distance = PWLHExample.calculate_intersection([(0,1), (8,4)], (9,2))
        self.convex_hull_width = [{'x_values': [x,9], 'y_values': [y, 2]}]
        self.xs = [x + 0.2]
        self.ys = [y - 0.3]
        self.words = [r"width$\approx" + str(round(real_distance, 1)) + r"$"]

        _, _, real_distance = PWLHExample.calculate_intersection([(8*60,4), (9*60,2)], (0,1))
        assert(round(real_distance, 1) == 19)
        x, y, distance = PWLHExample.calculate_intersection([(8,4), (9,2)], (0,1))
        self.convex_hull_width.append({'x_values': [x,0], 'y_values': [y, 1]})
        self.xs.append(6.5)
        self.ys.append(4.05)
        self.words.append(r"width$\approx" + str(int(round(real_distance))) + r"$")

        _, _, real_distance = PWLHExample.calculate_intersection([(9*60,2), (4*60,1)], (8*60,4))
        assert(round(real_distance, 1) == 2.2)
        x, y, distance = PWLHExample.calculate_intersection([(9,2), (4,1)], (8,4))
        self.convex_hull_width.append({'x_values': [x,8], 'y_values': [y, 4]})
        self.xs.append(x - 0.35)
        self.ys.append(y - 0.35)
        self.words.append(r"width$\approx" + str(round(real_distance, 1)) + r"$")

        self.common(filename, step)

    def pwlh9(self, filename, step):
        self.convex_hull = [(9,2)]
        self.decoded = self.copy_decoded[0:9]
        self.plot_values = [{'x_values': [0,8], 'y_values': [0.25,3.25], 'linestyle': '-'}]

        self.plot_values_alpha = []
        self.xs, self.ys, self.words = [], [], []

        self.convex_hull_lines = []
        self.convex_hull_width = []

        self.common(filename, step)

    def plot_texts(self, ax, x, y, s):
        color = 'black'
        fontsize = 13
        if 'width' in s:
            fontsize = 10
            color = self.COLOR_LINE
        alpha = 1
        ax.text(x, y, s, fontsize=fontsize, alpha=alpha, c=color)

    def plot_original_values(self, ax):
        scatter_x_alpha = range(self.index, len(self.original))
        original_alpha = self.original[self.index:len(self.original) + 1]
        ax.scatter(scatter_x_alpha, original_alpha, c=self.COLOR_ORIG, marker='x', zorder=3, alpha=self.LOWER_ALPHA)

        scatter_x_black = range(self.index+1)
        original_black = self.original[0:self.index+1]
        ax.scatter(scatter_x_black, original_black, c=self.COLOR_ORIG, marker='x', zorder=3, label=self.LABEL_ORIG)

    def plot_convex_hull(self, ax):
        x, y = [], []
        for point in self.convex_hull:
            point_x, point_y = point
            x.append(point_x)
            y.append(point_y)
        ax.scatter(x, y, c=self.COLOR_LINE, marker='o', zorder=3, label='convex hull', s=10)

        for line in self.convex_hull_lines:
            alpha = line.get('alpha') or 1
            ax.plot(line['x_values'], line['y_values'], c=self.COLOR_LINE, zorder=3, linestyle='-', alpha=alpha)

        for line in self.convex_hull_width:
            ax.plot(line['x_values'], line['y_values'], c=self.COLOR_LINE, zorder=3, linestyle=':', alpha=1)

    def common(self, filename, step):
        # print(plt.rcParams["figure.figsize"]) # [6.4, 4.8]
        plt.rcParams["figure.figsize"] = [8, 3.48]
        scatter_x = range(len(self.original))
        fig, ax = plt.subplots()

        self.plot_original_values(ax)

        self.plot_convex_hull(ax)

        # decoded values
        x_decoded = scatter_x[0:len(self.decoded)]
        ax.scatter(x_decoded, self.decoded, c=self.COLOR_DECO, marker='o', zorder=2, label=self.encoded_label())

        # decoded lines
        for p in self.plot_values:
            alpha = p.get('alpha') or 1
            linestyle = p.get('linestyle') or ':'
            color = self.COLOR_DECO if linestyle == '-' else self.COLOR_LINE
            ax.plot(p['x_values'], p['y_values'], c=color, zorder=1, linestyle=linestyle, alpha=alpha)

        for index, x in enumerate(self.xs):
            y = self.ys[index]
            s = self.words[index]
            self.plot_texts(ax, x, y, s)

        ax.set(xlabel=self.XLABEL, ylabel=self.YLABEL, title=self.title("PWLH", 1, 256, step))
        ax.grid(color=PlotConstants.COLOR_SILVER, linestyle='dotted')
        ax.set_axisbelow(True)
        ax.set_ylim(bottom=0, top=4.5)
        ax.set_xlim(left=-1, right=12)
        ax.set_xticks(range(0,13))
        ax.set_yticks(range(0,5))

        labels = ['t' + str(index) for index in range(1, len(ax.get_xticklabels()))]
        ax.set_xticklabels(labels)
        ax.legend(loc='upper left')
        plt.tight_layout()
        fig.savefig(self.PATH + filename)

    def encoded_label(self):
        return self.LABEL_DECO

    def title(self, algorithm, epsilon, window, step):
        epsilon = r"$\epsilon = {}$".format(epsilon)
        window = r"$w = {}$".format(window)
        text = "Algorithm " + algorithm + " with " + epsilon + " and " + window + " - STEP " + str(step)
        return text

    @staticmethod
    def calculate_intersection(line, point):
        point1, point2 = line
        # line equation: a*x + b*y = c
        a, b, c = PWLHExample.line_from_points(point1, point2)
        distance = PWLHExample.shortest_distance(point[0], point[1], a, b, -c)

        # perpendicular line equation: a_p*x + b_p*y = c_p
        a_p, b_p, c_p = PWLHExample.perpendicular_by_point(a, b, point[0], point[1])

        if b_p == 0: # x = c_p/a_p
            other_point = (point[0], point[1] + 1) # same x as point, different y

        else: # y = (1/b_p)*(-a_p*x + c_p)
            other_point_x = point[0] + 1
            other_point_y = PWLHExample.get_y(a_p, b_p, c_p, other_point_x)
            other_point = (other_point_x, other_point_y)

        perpendicular_line = [point, other_point]

        x, y = PWLHExample.line_intersection(line, perpendicular_line)
        return [x, y, distance]

    @staticmethod
    def shortest_distance(x1, y1, a, b, c):
        d = abs((a * x1 + b * y1 + c)) / (math.sqrt(a * a + b * b))
        return d

    @staticmethod
    def get_y(a, b, c, x):
        # a*x + b*y = c
        if b == 0: # x = c_p/a_p
            return c/float(x)
        else: # y = (1/b)*(-a*x + c)
            return (1/float(b))*(-a*float(x) + c)

    @staticmethod
    def line_from_points(point1, point2):
        a = point2[1] - point1[1]
        b = point1[0] - point2[0]
        c = a*point1[0] + b*point1[1]
        # a*x + b*y = c
        return [a, b, c]

    # return the ax + by = c equation of a line that
    # - is perpendicular to a line with scope a
    # - passes through (x1, y1)
    @staticmethod
    def perpendicular_by_point(a, b, x1, y1):
        if a == 0:  # by = c
            return [1, 0, x1]  # x = x1
        else:
            # original line: a*x + b*y = c ====> original line slope: -(a/b)
            new_slope = b/float(a)

            # perpendicular line: y = new_slope*x + c
            # y1 = new_slope*x1 + c
            c = y1 - new_slope*x1

            # new_slope*x - y + c = 0
            # new_slope*x - y + c = -c
            return [new_slope, -1, -c]

    #
    # SOURCE: https://stackoverflow.com/a/20677983/4547232
    #
    @staticmethod
    def line_intersection(line1, line2):
        xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
        ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

        def det(a, b):
            return a[0] * b[1] - a[1] * b[0]

        div = det(xdiff, ydiff)
        if div == 0:
           raise Exception('lines do not intersect')

        d = (det(*line1), det(*line2))
        x = det(d, xdiff) / div
        y = det(d, ydiff) / div
        return x, y



PWLHExample()

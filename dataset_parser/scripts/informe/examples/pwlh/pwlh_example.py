import sys
sys.path.append('.')

import matplotlib.pyplot as plt
from scripts.informe.examples.examples_base import ExamplesBase
import math

plt.rcParams["mathtext.fontset"] = "cm"

class PWLHExample(ExamplesBase):
    SMAX_MAR = 0.06
    SMIN_MAR = 0.1

    def __init__(self):
        super(PWLHExample, self).__init__()
        self.path = "/Users/pablocerve/Documents/FING/Proyecto/pc-tesis/dataset_parser/scripts/informe/examples/pwlh/"
        self.algorithm = "PWLH"
        self.original = [1, 1, 1, 1, 1, 2, 3, 3, 4, 2, 1, 1]
        self.decoded =  [0, 1, 1, 1, 2, 2, 3, 3, 3, 2, 1, 1]
        self.copy_decoded = list.copy(self.decoded)
        self.plot_values = []
        self.plot_values_alpha = []
        self.xs, self.ys, self.words = [], [], []
        self.convex_hull = []
        self.convex_hull_lines = []
        self.convex_hull_width = []

        self.pwlh1("pwlh1.pdf", 1, 0)
        self.pwlh2("pwlh2.pdf", 2, 1)
        self.pwlh3("pwlh3.pdf", 5, 4)
        self.pwlh4("pwlh4.pdf", 6, 5)
        self.pwlh5("pwlh5.pdf", 7, 6)
        self.pwlh6("pwlh6.pdf", 8, 7)
        self.pwlh7("pwlh7.pdf", 9, 8)
        self.pwlh8("pwlh8.pdf", 10, 9)
        self.pwlh9("pwlh9.pdf", 11, 9)
        self.pwlh10("pwlh10.pdf", 12, 11)


    def pwlh1(self, filename, step, index):
        self.xs, self.ys, self.words = [0-0.2], [1+0.15], ['E1']
        self.decoded = []
        self.convex_hull = [(0,1)]
        self.convex_hull_lines = []
        self.common_pwlh(filename, step, index)

    def pwlh2(self, filename, step, index):
        self.xs, self.ys, self.words = [1-0.2], [1+0.15], ['E2']
        self.convex_hull = [(0,1), (1,1)]
        self.convex_hull_lines = [{'x_values': [0,1], 'y_values': [1,1]}]
        self.xs += [0]
        self.ys += [0.65]
        self.words += [r"distance$=0$"]
        self.common_pwlh(filename, step, index)

    def pwlh3(self, filename, step, index):
        self.xs, self.ys, self.words = [4-0.2], [1+0.15], ['E5']
        self.convex_hull = [(0,1), (4,1)]
        self.convex_hull_lines = [{'x_values': [0,4], 'y_values': [1,1]}]
        self.xs += [1.5]
        self.ys += [0.65]
        self.words += [r"distance$=0$"]
        self.common_pwlh(filename, step, index)

    def pwlh4(self, filename, step, index):
        self.xs, self.ys, self.words = [5-0.2], [2+0.15], ['E6']
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
        self.xs += [x - 0.7]
        self.ys += [y + 0.15]
        self.words += [self.width_text(str(round(real_distance, 1)))]
        self.common_pwlh(filename, step, index)

    def pwlh5(self, filename, step, index):
        self.xs, self.ys, self.words = [6-0.2], [3+0.15], ['E7']
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
        self.xs += [x - 1.05]
        self.ys += [y + 0.15]
        self.words += [self.width_text(str(round(real_distance, 1)))]
        self.common_pwlh(filename, step, index)

    def pwlh6(self, filename, step, index):
        del self.xs[0]
        del self.ys[0]
        del self.words[0]

        self.xs += [7-0.2]
        self.ys += [3+0.15]
        self.words += ['E8']
        self.convex_hull = [(0,1), (6,3), (7,3), (4,1)]
        self.convex_hull_lines = [
            {'x_values': [0,4], 'y_values': [1,1]},
            {'x_values': [0,6], 'y_values': [1,3]},
            {'x_values': [4,7], 'y_values': [1,3]},
            {'x_values': [6,7], 'y_values': [3,3]}
        ]
        self.common_pwlh(filename, step, index)

    def pwlh7(self, filename, step, index):
        self.xs, self.ys, self.words = [8-0.2], [4+0.15], ['E9']
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
        self.xs += [x - 1]
        self.ys += [y + 0.15]
        self.words += [self.width_text(str(round(real_distance, 1)))]
        self.common_pwlh(filename, step, index)

    def pwlh8(self, filename, step, index):
        self.xs, self.ys, self.words = [9+0.05], [2+0.15], ['E10']
        self.convex_hull = [(0,1), (8,4), (9,2), (4,1)]

        self.convex_hull_lines = [
            {'x_values': [0,4], 'y_values': [1,1]},
            {'x_values': [0,8], 'y_values': [1,4]},
            {'x_values': [8,10],'y_values': [4,10*(3/8)+1], 'alpha': ExamplesBase.ALPHA_LOW}, # continue line
            {'x_values': [4,9], 'y_values': [1,2]},
            {'x_values': [9,8], 'y_values': [2,4]},
            {'x_values': [9,7], 'y_values': [2,-7*(2/1)+20], 'alpha': ExamplesBase.ALPHA_LOW}, # continue line
            {'x_values': [4,9], 'y_values': [1,1], 'alpha': ExamplesBase.ALPHA_LOW}, # continue line
        ]
        # intersections
        _, _, real_distance = PWLHExample.calculate_intersection([(0,1), (8*60,4)], (9*60,2))
        assert(round(real_distance, 3) == 2.375)
        x, y, distance = PWLHExample.calculate_intersection([(0,1), (8,4)], (9,2))
        self.convex_hull_width = [{'x_values': [x,9], 'y_values': [y, 2]}]
        self.xs += [x + 0.2]
        self.ys += [y - 0.3]
        self.words += [self.width_text(str(round(real_distance, 1)))]

        _, _, real_distance = PWLHExample.calculate_intersection([(8*60,4), (9*60,2)], (0,1))
        assert(round(real_distance, 1) == 19)
        x, y, distance = PWLHExample.calculate_intersection([(8,4), (9,2)], (0,1))
        self.convex_hull_width.append({'x_values': [x,0], 'y_values': [y, 1]})
        self.xs.append(6.5)
        self.ys.append(4.05)
        self.words.append(self.width_text(str(int(round(real_distance)))))

        _, _, real_distance = PWLHExample.calculate_intersection([(9*60,2), (4*60,1)], (8*60,4))
        assert(round(real_distance, 1) == 2.2)
        x, y, distance = PWLHExample.calculate_intersection([(9,2), (4,1)], (8,4))
        self.convex_hull_width.append({'x_values': [x,8], 'y_values': [y, 4]})
        self.xs.append(x - 0.35)
        self.ys.append(y - 0.35)
        self.words.append(self.width_text(str(round(real_distance, 1))))

        _, _, real_distance = PWLHExample.calculate_intersection([(0,1),(4*60,1)],(8*60,4))
        assert(round(real_distance, 1) == 3)
        x, y, distance = PWLHExample.calculate_intersection([(0,1), (4,1)], (8,4))
        self.convex_hull_width.append({'x_values': [x,8], 'y_values': [y, 4]})
        self.xs.append(x - 0.6)
        self.ys.append(y - 0.35)
        self.words.append(r"dist.$=3$")

        self.common_pwlh(filename, step, index)

    def pwlh9(self, filename, step, index):
        self.xs, self.ys, self.words = [9+0.05], [2+0.15], ['E10'] # same as previous step
        self.encoded_points = [(0,0.25), (8,3.25)]
        self.convex_hull = [(9,2)]
        self.decoded = [] # self.copy_decoded[0:9]
        self.plot_values = [{'x_values': [0,8], 'y_values': [0.25,3.25], 'linestyle': '-'}]

        self.plot_values_alpha = []
        # self.xs, self.ys, self.words = [], [], []

        self.convex_hull_lines = []
        self.convex_hull_width = []

        self.common_pwlh(filename, step, index)

    def pwlh10(self, filename, step, index):
        self.encoded_points += [(9,1.75), (11,0.75)]
        self.convex_hull = []
        self.decoded = self.copy_decoded[0:12]
        self.plot_values += [{'x_values': [9,11], 'y_values': [1.75,0.75]}]

        self.plot_values_alpha = []
        self.xs, self.ys, self.words = [], [], []

        self.convex_hull_lines = []
        self.convex_hull_width = []

        self.common_pwlh(filename, step, index)

    def common_pwlh(self, filename, step, index):
        ax, fig = self.common_1(index)

        self.plot_convex_hull(self.convex_hull, self.convex_hull_lines, self.convex_hull_width, ax)
        for index, x in enumerate(self.xs):
            y = self.ys[index]
            s = self.words[index]
            self.plot_texts(ax, x, y, s)

        self.common_2(ax, fig, step, True, filename)

    @staticmethod
    def width_text(string):
        return r"dist.$\approx" + string + r"$"

    @staticmethod
    def plot_texts(ax, x, y, s):
        color = 'black'
        fontsize = 13
        if 'dist' in s:
            fontsize = 10
            color = ExamplesBase.COLOR_LINE
        alpha = 1
        ax.text(x, y, s, fontsize=fontsize, alpha=alpha, c=color)

    @staticmethod
    def plot_convex_hull(convex_hull, convex_hull_lines, convex_hull_width, ax):
        if len(convex_hull) == 0:
            return

        x, y = [], []
        for point in convex_hull:
            point_x, point_y = point
            x.append(point_x)
            y.append(point_y)
        ax.scatter(x, y, c=ExamplesBase.COLOR_LINE, marker='o', zorder=3, label='convex hull', s=10)

        for line in convex_hull_lines:
            alpha = line.get('alpha') or 1
            ax.plot(line['x_values'], line['y_values'], c=ExamplesBase.COLOR_LINE, zorder=3, linestyle='-', alpha=alpha)

        for line in convex_hull_width:
            ax.plot(line['x_values'], line['y_values'], c=ExamplesBase.COLOR_LINE, zorder=3, linestyle=':', alpha=1)

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




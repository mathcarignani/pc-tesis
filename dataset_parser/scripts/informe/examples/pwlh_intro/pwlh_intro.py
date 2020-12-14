import sys
sys.path.append('.')

# import matplotlib
import matplotlib.pyplot as plt
from scripts.informe.examples.examples_base import ExamplesBase
from scripts.informe.examples.pwlh.pwlh_example import PWLHExample

plt.rcParams["mathtext.fontset"] = "cm"

class PWLHIntro(ExamplesBase):
    def __init__(self):
        super(PWLHIntro, self).__init__()
        self.path = "/Users/pablocerve/Documents/FING/Proyecto/pc-tesis/dataset_parser/scripts/informe/examples/pwlh_intro/"
        self.xlim_right = 5
        self.figsize = [4.1, 3.48]
        self.window = None
        self.labels = range(1,6)

        self.algorithm = "PWLH"
        self.original = [2, 2, 2, 4, 1]
        self.plot_values = []
        self.plot_values_alpha = []
        self.arrows = []
        self.xs, self.ys, self.words = [], [], []
        self.xs_pwlh, self.ys_pwlh, self.words_pwlh = [], [], []

        self.pwlh1("pwlh1.pdf", 1, 3)
        self.pwlh2("pwlh2.pdf", 2, 4)

    def pwlh1(self, filename, step, index):
        self.encoded_points = [] #[(0,1)]
        self.decoded = []
        self.xs = [3+0.1]
        self.ys = [4+0.05]
        self.words = ['E4']
        self.convex_hull = [(0,2), (3,4), (2,2)]
        self.convex_hull_lines = [
            {'x_values': [0,3], 'y_values': [2,4]},
            {'x_values': [0,2], 'y_values': [2,2]},
            {'x_values': [2,3], 'y_values': [2,4]},
        ]
        x, y, real_distance = PWLHExample.calculate_intersection([(0,2), (3,4)], (2,2))
        # print(real_distance, x, y)
        assert(round(real_distance, 1) == 1.1)
        assert(round(x, 2) == 1.38)
        assert(round(y, 2) == 2.92)
        self.convex_hull_width = [{'x_values': [x,2], 'y_values': [y, 2]}]
        self.xs_pwlh = [x - 1]
        self.ys_pwlh = [y + 0.1]
        self.words_pwlh = [PWLHExample.width_text(str(round(real_distance, 1)))]
        self.common_ca(filename, step, index)

    def pwlh2(self, filename, step, index):
        self.xs = [4+0.1]
        self.ys = [1-0.3]
        self.words = ['E5']
        self.convex_hull = [(0,2), (3,4), (4,1)]
        self.convex_hull_lines = [
            {'x_values': [0,3], 'y_values': [2,4]},
            {'x_values': [0,4], 'y_values': [2,1]},
            {'x_values': [3,4], 'y_values': [4,1]},
        ]

        x, y, real_distance = PWLHExample.calculate_intersection([(0,2), (3,4)], (4,1))
        # print(real_distance, x, y)
        assert(round(real_distance, 1) == 3.1)
        assert(round(x, 2) == 2.31)
        assert(round(y, 2) == 3.54)
        self.convex_hull_width = [{'x_values': [x,4], 'y_values': [y, 1]}]
        self.xs_pwlh = [x - 0.88]
        self.ys_pwlh = [y + 0.18]
        self.words_pwlh = [PWLHExample.width_text(str(round(real_distance, 1)))]

        x, y, real_distance = PWLHExample.calculate_intersection([(0,2), (4,1)], (3,4))
        # print(real_distance, x, y)
        assert(round(real_distance, 1) == 2.7)
        assert(round(x, 2) == 2.35)
        assert(round(y, 2) == 1.41)
        self.convex_hull_width += [{'x_values': [x,3], 'y_values': [y, 4]}]
        self.xs_pwlh += [x - 0.88]
        self.ys_pwlh += [y - 0.3]
        self.words_pwlh += [PWLHExample.width_text(str(round(real_distance, 1)))]

        x, y, real_distance = PWLHExample.calculate_intersection([(4,1), (3,4)], (0,2))
        print(real_distance, x, y)
        assert(round(real_distance, 1) == 3.5)
        assert(round(x, 2) == 3.3)
        assert(round(y, 2) == 3.1)
        self.convex_hull_width += [{'x_values': [x,0], 'y_values': [y, 2]}]
        self.xs_pwlh += [x + 0.05]
        self.ys_pwlh += [y - 0]
        self.words_pwlh += [PWLHExample.width_text(str(round(real_distance, 1)))]

        self.common_ca(filename, step, index)
    
    def common_ca(self, filename, step, index):
        ax, fig = self.common_1(index)
        self.plot_texts(ax)
        PWLHExample.plot_convex_hull(self.convex_hull, self.convex_hull_lines, self.convex_hull_width, ax)
        for index, x in enumerate(self.xs_pwlh):
            y = self.ys_pwlh[index]
            s = self.words_pwlh[index]
            PWLHExample.plot_texts(ax, x, y, s)
        self.common_2(ax, fig, step, True, filename)
        
    def plot_texts(self, ax):
        for index, x in enumerate(self.xs):
            y = self.ys[index]
            s = self.words[index]
            color = 'black'
            if 'SM' in s or 'A,E' in s:
                color = self.COLOR_LINE
            if 'A,E' in s:
                x -= 0.05
            if s in ['A', 'S', 'E']:
                x -= 0.35
                y -= 0.06
            elif 'SMin' in s:
                if y == 0:
                    y += 0.05
            alpha = self.ALPHA_LOW if "Old" in s and "=" not in s else 1
            ax.text(x, y, s, fontsize=13, alpha=alpha, c=color)
            
PWLHIntro()

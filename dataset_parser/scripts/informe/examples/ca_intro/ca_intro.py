import sys
sys.path.append('.')

# import matplotlib
import matplotlib.pyplot as plt
from scripts.informe.examples.examples_base import ExamplesBase

plt.rcParams["mathtext.fontset"] = "cm"

class CAExample(ExamplesBase):
    def __init__(self):
        super(CAExample, self).__init__()
        self.path = "/Users/pablocerve/Documents/FING/Proyecto/pc-tesis/dataset_parser/scripts/informe/examples/ca_intro/"
        self.xlim_right = 5
        self.figsize = [4.1, 3.48]
        self.window = None

        self.algorithm = "CA"
        self.original = [2, 2, 2, 1, 1]
        self.plot_values = []
        self.plot_values_alpha = []
        self.arrows = []
        self.xs, self.ys, self.words = [], [], []

        self.ca1("ca1.pdf", 1, 2)
        self.ca2("ca2.pdf", 2, 2)

    def ca1(self, filename, step, index):
        self.encoded_points = [] #[(0,1)]
        self.decoded = [] # self.copy_decoded[0:1]
        self.plot_values1 = [
            {'x_values': [0,2], 'y_values': [2,4], 'color': self.COLOR_LINE, 'linestyle': ':'},
            {'x_values': [0,2], 'y_values': [2,0], 'color': self.COLOR_LINE, 'linestyle': ':'}
        ]
        self.plot_values = list.copy(self.plot_values1)
        self.plot_values.append({'x_values': [0,3], 'y_values': [2,2], 'color': self.COLOR_LINE, 'linestyle': '--'})
        self.xs = [0, 1.05, 2 + self.SMIN_MAR, 2 + self.SMAX_MAR, 2.05, 3 + self.SMAX_MAR]
        self.ys = [2, 2.1, 0, 4, 2.1, 2]
        self.words = ['A', 'S', 'SMin', 'SMax', 'E', '(A,E)']
        self.patches = [{'points': [(0,2), (2,4), (2,0)], 'polygon': True}]
        self.common_ca(filename, step, index)

    def ca2(self, filename, step, index):
        self.arrows = [{'x': 2, 'y': 2}]
        self.plot_values = self.plot_values1
        [a.update({'alpha': self.ALPHA_LOW}) for a in self.plot_values]
        self.plot_values += [
            {'x_values': [0,3], 'y_values': [2,3.5], 'color': self.COLOR_LINE, 'linestyle': ':'},
            {'x_values': [0,3], 'y_values': [2,0.5], 'color': self.COLOR_LINE, 'linestyle': ':'}
        ]
        self.xs = [0, 2 + self.SMIN_MAR, 2 + self.SMAX_MAR, 2.05, 3 + self.SMAX_MAR, 3 + self.SMAX_MAR]
        self.ys = [2, 0, 4, 2.1, 0.5-0.1, 3.5-0.1]
        self.words = ['A', 'SMinOld', 'SMaxOld', 'S', 'SMin', 'SMax']
        self.patches = [{'points': [(0,2), (2,3), (2,1)], 'polygon': True}]
        self.common_ca(filename, step, index)
    
    def common_ca(self, filename, step, index):
        ax, fig = self.common_1(index)
        self.plot_texts(ax)
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
            
CAExample()

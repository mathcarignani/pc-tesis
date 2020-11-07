import sys
sys.path.append('.')

# import matplotlib
import numpy as np
import matplotlib.pyplot as plt
from scripts.informe.plot.plot_constants import PlotConstants
from scripts.informe.examples.examples_base import ExamplesBase

plt.rcParams["mathtext.fontset"] = "cm"

class CAExample(ExamplesBase):
    def __init__(self):
        super(CAExample, self).__init__()
        self.path = "/Users/pablocerve/Documents/FING/Proyecto/pc-tesis/dataset_parser/scripts/informe/examples/ca/"
        self.algorithm = "CA"
        self.original = [1, 1, 1, 1, 1, 2, 3, 3, 4, 2, 1, 1]
        self.decoded =  [1, 1, 1, 2, 2, 2, 3, 4, 4, 2, 2, 1]
        self.copy_decoded = list.copy(self.decoded)
        self.plot_values = []
        self.plot_values_alpha = []
        self.arrows = []
        self.xs, self.ys, self.words = [], [], []

        self.ca1("ca1.pdf", 1, 1)
        self.ca2("ca2.pdf", 2, 2)
        self.ca3("ca3.pdf", 3, 2)
        self.ca4("ca4.pdf", 7, 4)
        self.ca5("ca5.pdf", 8, 5)
        self.ca6("ca6.pdf", 9, 5)
        self.ca7("ca7.pdf", 10, 6)
        self.ca8("ca8.pdf", 11, 7)
        self.ca9("ca9.pdf", 12, 11)

    def ca1(self, filename, step, index):
        self.encoded_points = [(0,1)]
        self.decoded = [] # self.copy_decoded[0:1]
        self.plot_values1 = [
            {'x_values': [0,2], 'y_values': [1,3], 'color': self.COLOR_LINE, 'linestyle': ':'},
            {'x_values': [0,2], 'y_values': [1,-1], 'color': self.COLOR_LINE, 'linestyle': ':'}
        ]
        self.arrows = [{'x': 1, 'y': 1}]
        self.plot_values = self.plot_values1
        self.xs = [0, 1, 1 + self.SMIN_MAR, 2 + self.SMAX_MAR]
        self.ys = [1, 1, 0, 3]
        self.words = ['A', 'S', 'SMin', 'SMax']
        self.patches = [{'points': [(0,1), (2,3), (2,0), (1,0)], 'polygon': True}]
        self.common_ca(filename, step, index)

    def ca2(self, filename, step, index):
        self.arrows = []
        self.plot_values = list.copy(self.plot_values1)
        self.plot_values.append({'x_values': [0,5], 'y_values': [1,1], 'color': self.COLOR_LINE, 'linestyle': '--'})
        self.xs += [2, 5 + self.SMAX_MAR]
        self.ys += [1, 1-0.1]
        self.words += ['E3', 'SE3']
        self.common_ca(filename, step, index)

    def ca3(self, filename, step, index):
        self.arrows = [{'x': 2, 'y': 1}]
        self.plot_values = list.copy(self.plot_values1)
        [a.update({'alpha': self.ALPHA_LOW}) for a in self.plot_values]
        m3 = (1/2.0)
        y_val3 = 3*m3+1
        self.plot_values3 = [
            {'x_values': [0,3], 'y_values': [1,y_val3], 'color': self.COLOR_LINE, 'linestyle': ':'},
            {'x_values': [0,3], 'y_values': [1,-3*m3+1], 'color': self.COLOR_LINE, 'linestyle': ':'}
        ]
        self.plot_values += self.plot_values3
        self.xs = [0, 2, -0.5, 2 + self.SMAX_MAR, 2 + self.SMAX_MAR, 3 + self.SMAX_MAR]
        self.ys = [1, 1, 0, 3, 0, y_val3]
        self.words = ['A', 'S', 'SMinOld', 'SMaxOld', 'SMin', 'SMax']
        self.patches = [{'points': [(0,1), (3,2.5), (3,0), (2,0)], 'polygon': True}]
        self.common_ca(filename, step, index)

    def ca4(self, filename, step, index):
        self.arrows = [{'x': 4, 'y': 1}]
        mprev = (1/3.0)
        m4 = (1/4.0)
        y_val4 = 7*m4+1
        plot_values_alpha = [
            {'x_values': [0,5], 'y_values': [1,5*mprev+1], 'alpha': self.ALPHA_LOW, 'color': self.COLOR_LINE, 'linestyle': ':'},
            {'x_values': [0,3], 'y_values': [1,-3*mprev+1], 'alpha': self.ALPHA_LOW, 'color': self.COLOR_LINE, 'linestyle': ':'}
        ]
        self.plot_values3 = [
            {'x_values': [0,7], 'y_values': [1,y_val4], 'color': self.COLOR_LINE, 'linestyle': ':'},
            {'x_values': [0,5], 'y_values': [1,-5*m4+1], 'color': self.COLOR_LINE, 'linestyle': ':'}
        ]
        self.plot_values = plot_values_alpha + self.plot_values3
        self.xs = [0, 4, 4 + self.SMIN_MAR, 7 + self.SMAX_MAR, 1, 3.5]
        self.ys = [1, 1, 0, y_val4-0.1, 0, 5*mprev+1]
        self.words = ['A', 'S', 'SMin', 'SMax', 'SMinOld', 'SMaxOld']
        self.patches = [{'points': [(0,1), (7,y_val4), (7,0), (4,0)], 'polygon': True}]
        self.common_ca(filename, step, index)

    def ca5(self, filename, step, index):
        self.arrows = []
        m4 = (1/4.0)
        m5 = (1/5.0)
        y_val4 = 7*m4+1
        y_val5 = 7*m5+1
        self.plot_values = list.copy(self.plot_values3)
        self.plot_values.append({'x_values': [0,7], 'y_values': [1,y_val5], 'color': self.COLOR_LINE, 'linestyle': '--'})
        self.xs = [0, 4, 4 + self.SMIN_MAR, 7 + self.SMAX_MAR, 5+0.1, 7 + self.SMAX_MAR]
        self.ys = [1, 1, 0,               y_val4-0.1,      2-0.3, y_val5-0.1]
        self.words = ['A', 'S', 'SMin', 'SMax', 'E6', 'SE6']
        self.common_ca(filename, step, index)

    def ca6(self, filename, step, index):
        self.arrows = [{'x': 5, 'y': 2}]
        m4 = (1/4.0)
        y_val4 = 7*m4+1
        self.plot_values = list.copy(self.plot_values3)
        self.plot_values[1].update({'alpha': self.ALPHA_LOW})
        self.plot_values += [
            {'x_values': [0,7], 'y_values': [1,1], 'color': self.COLOR_LINE, 'linestyle': ':'},
            {'x_values': [0,7], 'y_values': [1,7*(2/5.0)+1], 'alpha': self.ALPHA_LOW, 'color': self.COLOR_LINE, 'linestyle': ':'},
        ]
        self.xs = [0, 4 + self.SMIN_MAR, 7 + self.SMAX_MAR, 5, 7 + self.SMAX_MAR]
        self.ys = [1, 0, y_val4-0.1, 2-0.1, 1-0.2]
        self.words = ['A', 'SMinOld', 'SMax=SMaxOld', 'S', 'SMin']
        self.patches = [{'points': [(0,1), (7,y_val4), (7,1)], 'polygon': True}]
        self.common_ca(filename, step, index)

    def ca7(self, filename, step, index):
        self.arrows = []
        m4 = (1/4.0)
        y_val4 = 7*m4+1
        m7 = (2/6.0)
        yval = 7*m7+1
        del self.plot_values[-1]
        self.plot_values.append({'x_values': [0,7], 'y_values': [1,yval], 'color': self.COLOR_LINE, 'linestyle': '--'})
        self.xs = [0, 7 + self.SMAX_MAR, 5, 7 + self.SMAX_MAR, 6, 7 + self.SMAX_MAR]
        self.ys = [1, y_val4-0.1, 2-0.1, 1-0.2, 3+0.1, yval-0.1]
        self.words = ['A', 'SMax', 'S', 'SMin', 'E7', 'SE7']
        self.common_ca(filename, step, index)

    def ca8(self, filename, step, index):
        self.encoded_points += [(5,2), (6,3)]
        self.decoded = [] # self.copy_decoded[0:7]
        self.arrows = [{'x': 7, 'y': 3}]
        self.plot_values1 = [
            {'x_values': [0,5], 'y_values': [1,2]},
            {'x_values': [6,7], 'y_values': [3,4], 'linestyle': ':', 'color': self.COLOR_LINE},
            {'x_values': [6,7], 'y_values': [3,2], 'linestyle': ':', 'color': self.COLOR_LINE}
        ]
        self.plot_values = self.plot_values1
        self.xs = [6, 7, 7 + self.SMAX_MAR, 7 + self.SMAX_MAR]
        self.ys = [3, 3, 1.73, 4]
        self.words = ['A', 'S', 'SMin', 'SMax']
        self.patches = [{'points': [(6,3), (7,4), (7,2)], 'polygon': True}]
        self.common_ca(filename, step, index)

    def ca9(self, filename, step, index):
        self.encoded_points += [(8,4), (9,2), (11,1)]
        self.decoded = self.copy_decoded[0:12]
        self.arrows = []
        self.plot_values = [
            {'x_values': [0,5], 'y_values': [1,2]},
            {'x_values': [6,8], 'y_values': [3,4]},
            {'x_values': [9,11], 'y_values': [2,1]}
        ]
        self.xs = []
        self.patches = []
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
            if 'SM' in s or 'SE' in s:
                color = self.COLOR_LINE
            if s in ['A', 'S']:
                x -= 0.35
                y -= 0.06
            elif 'SMin' in s:
                if y == 0:
                    y += 0.05
            elif 'E' in s:
                if len(s) == 2:  # 'E1', 'E2', etc.
                    x -= 0.5
                    y -= 0.08
                else: # 'SE1', 'SE2', etc.
                    pass
            alpha = self.ALPHA_LOW if "Old" in s and "=" not in s else 1
            ax.text(x, y, s, fontsize=13, alpha=alpha, c=color)
            
CAExample()

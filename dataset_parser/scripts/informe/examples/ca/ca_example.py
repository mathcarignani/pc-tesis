import sys
sys.path.append('.')

# import matplotlib
import numpy as np
import matplotlib.pyplot as plt
from scripts.informe.plot.plot_constants import PlotConstants
from scripts.informe.examples.examples_base import ExamplesBase

plt.rcParams["mathtext.fontset"] = "cm"

class CAExample(ExamplesBase):
    PATH = '/Users/pablocerve/Documents/FING/Proyecto/pc-tesis/dataset_parser/scripts/informe/examples/ca/'
    SMAX_MAR = 0.06
    SMIN_MAR = 0.1
    LOW_ALPHA = 0.3
    LOWER_ALPHA = 0.2

    def __init__(self):
        self.original = [1, 1, 1, 1, 1, 2, 3, 3, 4, 2, 1, 1]
        self.decoded =  [1, 1, 1, 2, 2, 2, 3, 4, 4, 2, 2, 1]
        self.copy_decoded = list.copy(self.decoded)
        self.plot_values = []
        self.plot_values_alpha = []
        self.arrows = []
        self.xs, self.ys, self.words = [], [], []

        self.index = 1
        self.ca1("ca1.pdf", 1)
        self.index = 2
        self.ca2("ca2.pdf", 2)
        self.ca3("ca3.pdf", 3)
        self.index = 4
        self.ca4("ca4.pdf", 7)
        self.index = 5
        self.ca5("ca5.pdf", 8)
        self.ca6("ca6.pdf", 9)
        self.index = 6
        self.ca7("ca7.pdf", 10)
        self.index = 7
        self.ca8("ca8.pdf", 11)

    def ca1(self, filename, step):
        self.decoded = self.copy_decoded[0:1]
        self.plot_values1 = [
            {'x_values': [0,2], 'y_values': [1,3]},
            {'x_values': [0,2], 'y_values': [1,-1]}
        ]
        self.arrows = [{'x': 1, 'y': 1}]
        self.plot_values = self.plot_values1
        self.xs = [0, 1, 1 + self.SMIN_MAR, 2 + self.SMAX_MAR]
        self.ys = [1, 1, 0, 3]
        self.words = ['A', 'S', 'SMin', 'SMax']
        self.common(filename, step)

    def ca2(self, filename, step):
        self.arrows = []
        self.plot_values = list.copy(self.plot_values1)
        self.plot_values.append({'x_values': [0,5], 'y_values': [1,1], 'linestyle': '--'})
        self.xs += [2, 5 + self.SMAX_MAR]
        self.ys += [1, 1-0.1]
        self.words += ['E1', 'SE1']
        self.common(filename, step)

    def ca3(self, filename, step):
        self.arrows = [{'x': 2, 'y': 1}]
        self.plot_values = list.copy(self.plot_values1)
        [a.update({'alpha': self.LOW_ALPHA}) for a in self.plot_values]
        m3 = (1/2.0)
        y_val3 = 3*m3+1
        self.plot_values3 = [
            {'x_values': [0,3], 'y_values': [1,y_val3]},
            {'x_values': [0,3], 'y_values': [1,-3*m3+1]}
        ]
        self.plot_values += self.plot_values3
        self.xs = [0, 2, -0.5, 0.5, 2 + self.SMIN_MAR, 3 + self.SMAX_MAR]
        self.ys = [1, 1, 0, 3, 0, y_val3]
        self.words = ['A', 'S', 'SMinOld', 'SMaxOld', 'SMin', 'SMax']
        self.common(filename, step)

    def ca4(self, filename, step):
        self.arrows = [{'x': 4, 'y': 1}]
        mprev = (1/3.0)
        m4 = (1/4.0)
        y_val4 = 7*m4+1
        plot_values_alpha = [
            {'x_values': [0,5], 'y_values': [1,5*mprev+1], 'alpha': self.LOW_ALPHA},
            {'x_values': [0,3], 'y_values': [1,-3*mprev+1], 'alpha': self.LOW_ALPHA}
        ]
        self.plot_values3 = [
            {'x_values': [0,7], 'y_values': [1,y_val4]},
            {'x_values': [0,5], 'y_values': [1,-5*m4+1]}
        ]
        self.plot_values = plot_values_alpha + self.plot_values3
        self.xs = [0, 4, 4 + self.SMIN_MAR, 7 + self.SMAX_MAR, 1, 3.5]
        self.ys = [1, 1, 0, y_val4-0.1, 0, 5*mprev+1]
        self.words = ['A', 'S', 'SMin', 'SMax', 'SMinOld', 'SMaxOld']
        self.common(filename, step)

    def ca5(self, filename, step):
        self.arrows = []
        m4 = (1/4.0)
        m5 = (1/5.0)
        y_val4 = 7*m4+1
        y_val5 = 7*m5+1
        self.plot_values = list.copy(self.plot_values3)
        self.plot_values.append({'x_values': [0,7], 'y_values': [1,y_val5], 'linestyle': '--'})
        self.xs = [0, 4, 4 + self.SMIN_MAR, 7 + self.SMAX_MAR, 5+0.1, 7 + self.SMAX_MAR]
        self.ys = [1, 1, 0,               y_val4-0.1,      2-0.3, y_val5-0.1]
        self.words = ['A', 'S', 'SMin', 'SMax', 'E4', 'SE4']
        self.common(filename, step)

    def ca6(self, filename, step):
        self.arrows = [{'x': 5, 'y': 2}]
        m4 = (1/4.0)
        y_val4 = 7*m4+1
        self.plot_values = list.copy(self.plot_values3)
        self.plot_values[1].update({'alpha': self.LOW_ALPHA})
        self.plot_values += [
            {'x_values': [0,7], 'y_values': [1,1]},
            {'x_values': [0,7], 'y_values': [1,7*(2/5.0)+1], 'alpha': self.LOW_ALPHA},
        ]
        self.xs = [0, 4 + self.SMIN_MAR, 7 + self.SMAX_MAR, 5, 7 + self.SMAX_MAR]
        self.ys = [1, 0, y_val4-0.1, 2-0.1, 1-0.2]
        self.words = ['A', 'SMinOld', 'SMax=SMaxOld', 'S', 'SMin']
        self.common(filename, step)

    def ca7(self, filename, step):
        self.arrows = []
        m4 = (1/4.0)
        y_val4 = 7*m4+1
        m7 = (2/6.0)
        yval = 7*m7+1
        del self.plot_values[-1]
        self.plot_values.append({'x_values': [0,7], 'y_values': [1,yval], 'linestyle': '--'})
        self.xs = [0, 7 + self.SMAX_MAR, 5, 7 + self.SMAX_MAR, 6, 7 + self.SMAX_MAR]
        self.ys = [1, y_val4-0.1, 2-0.1, 1-0.2, 3+0.1, yval-0.1]
        self.words = ['A', 'SMax', 'S', 'SMin', 'E5', 'SE5']
        self.common(filename, step)

    def ca8(self, filename, step):
        self.decoded = self.copy_decoded[0:7]
        self.arrows = [{'x': 7, 'y': 3}]
        self.plot_values1 = [
            {'x_values': [0,5], 'y_values': [1,2], 'linestyle': '-'},
            {'x_values': [6,7], 'y_values': [3,4]},
            {'x_values': [6,7], 'y_values': [3,2]}
        ]
        self.plot_values = self.plot_values1
        self.xs = [6, 7, 7 + self.SMAX_MAR, 7 + self.SMAX_MAR]
        self.ys = [3, 3, 1.73, 4]
        self.words = ['A', 'S', 'SMin', 'SMax']
        self.common(filename, step)

    def plot_texts(self, ax, x, y, s):
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
        alpha = self.LOW_ALPHA if "Old" in s and "=" not in s else 1
        ax.text(x, y, s, fontsize=13, alpha=alpha, c=color)

    def plot_original_values(self, ax):
        scatter_x_alpha = range(self.index, len(self.original))
        original_alpha = self.original[self.index:len(self.original) + 1]
        ax.scatter(scatter_x_alpha, original_alpha, c=self.COLOR_ORIG, marker='x', zorder=3, alpha=self.LOWER_ALPHA)

        scatter_x_black = range(self.index+1)
        original_black = self.original[0:self.index+1]
        ax.scatter(scatter_x_black, original_black, c=self.COLOR_ORIG, marker='x', zorder=3, label=self.LABEL_ORIG)

    def common(self, filename, step):
        # print(plt.rcParams["figure.figsize"]) # [6.4, 4.8]
        plt.rcParams["figure.figsize"] = [8, 3.48]
        scatter_x = range(len(self.original))
        fig, ax = plt.subplots()

        self.plot_original_values(ax)

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

        for plot in self.arrows:
            ExamplesBase.plot_arrows(ax, plot, self.COLOR_LINE)

        ax.set(xlabel=self.XLABEL, ylabel=self.YLABEL, title=self.title("CA", 1, 256, step))
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


CAExample()

import sys
sys.path.append('.')

# import matplotlib
import numpy as np
import matplotlib.pyplot as plt
from scripts.informe.plot.plot_constants import PlotConstants

plt.rcParams["mathtext.fontset"] = "cm"

class CAExample(object):
    LABEL_ORIG = 'original value'
    LABEL_DECO = 'encoded value'
    COLOR_ORIG = 'navy'
    COLOR_DECO = 'orange'
    YLABEL = 'value'
    XLABEL = 'time'
    PATH = '/Users/pablocerve/Documents/FING/Proyecto/pc-tesis/dataset_parser/scripts/informe/examples/ca/'

    def __init__(self):
        self.original = [1, 1, 1, 1, 1, 2, 3, 3, 4, 2, 1, 1]
        self.decoded =  [1, 1, 1, 2, 2, 2, 3, 4, 4, 2, 2, 1]
        self.copy_decoded = list.copy(self.decoded)
        self.plot_values = []
        self.plot_values_alpha = []
        self.xs, self.ys, self.words = [], [], []
        self.ca1()
        self.ca2()
        self.ca3()
        self.ca4()
        self.ca5()
        self.ca6()
        self.ca7()
        self.ca8()

    def ca1(self):
        self.decoded = self.copy_decoded[0:1]
        self.plot_values1 = [
            {'x_values': [0,2], 'y_values': [1,3]},
            {'x_values': [0,2], 'y_values': [1,-1]}
        ]
        self.plot_values = self.plot_values1
        self.xs = [0, 1, 1, 2]
        self.ys = [1, 1, 0, 3]
        self.words = ['A', 'S', 'SMin', 'SMax']
        self.common("ca_1.pdf")

    def ca2(self):
        self.plot_values = list.copy(self.plot_values1)
        self.plot_values.append({'x_values': [0,5], 'y_values': [1,1], 'linestyle': '--'})
        self.xs += [2, 5]
        self.ys += [1, 1-0.1]
        self.words += ['E1', 'SE1']
        self.common("ca_2.pdf")

    def ca3(self):
        self.plot_values = list.copy(self.plot_values1)
        [a.update({'alpha': 0.3}) for a in self.plot_values]
        m = (1/2.0)
        y_val = 3*m+1
        self.plot_values3 = [
            {'x_values': [0,3], 'y_values': [1,y_val]},
            {'x_values': [0,3], 'y_values': [1,-3*m+1]}
        ]
        self.plot_values += self.plot_values3
        self.xs = [0, 2, -0.5, 0.5, 2, 3]
        self.ys = [1, 1, 0, 3, 0, y_val]
        self.words = ['A', 'S', 'SMinOld', 'SMaxOld', 'SMin', 'SMax']
        self.common("ca_3.pdf")

    def ca4(self):
        m4 = (1/4.0)
        y_val4 = 7*m4+1
        self.plot_values3 = [
            {'x_values': [0,7], 'y_values': [1,y_val4]},
            {'x_values': [0,5], 'y_values': [1,-5*m4+1]}
        ]
        self.plot_values = list.copy(self.plot_values3)
        self.xs = [0, 4, 4, 7]
        self.ys = [1, 1, 0, y_val4-0.1]
        self.words = ['A', 'S', 'SMin', 'SMax']
        self.common("ca_4.pdf")

    def ca5(self):
        m4 = (1/4.0)
        m5 = (1/5.0)
        y_val4 = 7*m4+1
        y_val5 = 7*m5+1
        self.plot_values.append({'x_values': [0,7], 'y_values': [1,y_val5], 'linestyle': '--'})
        self.xs = [0, 4, 4, 7,          5+0.1, 7]
        self.ys = [1, 1, 0, y_val4-0.1, 2-0.3, y_val5-0.1]
        self.words = ['A', 'S', 'SMin', 'SMax', 'E4', 'SE4']
        self.common("ca_5.pdf")

    def ca6(self):
        m4 = (1/4.0)
        y_val4 = 7*m4+1
        self.plot_values = list.copy(self.plot_values3)
        self.plot_values[1].update({'alpha': 0.3})
        self.plot_values.append({'x_values': [0,7], 'y_values': [1,1]})
        self.xs = [0, 4, 7, 5+0.1, 7]
        self.ys = [1, 0, y_val4-0.1, 2-0.3, 1-0.2]
        self.words = ['A', 'SMinOld', 'SMax', 'S', 'SMin']
        self.common("ca_6.pdf")

    def ca7(self):
        m4 = (1/4.0)
        y_val4 = 7*m4+1
        m7 = (2/6.0)
        yval = 7*m7+1
        del self.plot_values[1]
        self.plot_values.append({'x_values': [0,7], 'y_values': [1,yval], 'linestyle': '--'})
        self.xs = [0, 7, 5+0.1, 7, 6, 7]
        self.ys = [1, y_val4-0.1, 2-0.3, 1-0.2, 3, yval-0.1]
        self.words = ['A', 'SMax', 'S', 'SMin', 'E5', 'SE5']
        self.common("ca_7.pdf")

    def ca8(self):
        self.decoded = self.copy_decoded[0:7]
        self.plot_values1 = [
            {'x_values': [0,5], 'y_values': [1,2], 'linestyle': '-'},
            {'x_values': [6,7], 'y_values': [3,4]},
            {'x_values': [6,7], 'y_values': [3,2]}
        ]
        self.plot_values = self.plot_values1
        self.xs = [6, 7, 7, 7]
        self.ys = [3, 3, 2, 4]
        self.words = ['A', 'S', 'SMin', 'SMax']
        self.common("ca_8.pdf")


    def texts(self, ax, x, y, s):
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
        alpha = 0.3 if "Old" in s else 1
        ax.text(x, y, s, fontsize=13, alpha=alpha)

    def common(self, filename):
        # print(plt.rcParams["figure.figsize"]) # [6.4, 4.8]
        plt.rcParams["figure.figsize"] = [8, 3.48]
        scatter_x = range(len(self.original))
        fig, ax = plt.subplots()

        # original values
        ax.scatter(scatter_x, self.original, c=self.COLOR_ORIG, marker='x', zorder=2, label=self.LABEL_ORIG)

        # decoded values
        x_decoded = scatter_x[0:len(self.decoded)]
        ax.scatter(x_decoded, self.decoded, c=self.COLOR_DECO, marker='o', zorder=1, label=self.encoded_label())

        # decoded lines
        for p in self.plot_values:
            alpha = p.get('alpha') or 1
            linestyle = p.get('linestyle') or ':'
            ax.plot(p['x_values'], p['y_values'], c=self.COLOR_DECO, zorder=1, linestyle=linestyle, alpha=alpha)

        for index, x in enumerate(self.xs):
            y = self.ys[index]
            s = self.words[index]
            self.texts(ax, x, y, s)

        ax.set(xlabel=self.XLABEL, ylabel=self.YLABEL, title=self.title("APCA", 1, 256))
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

    def title(self, algorithm, epsilon, window):
        epsilon = r"$\epsilon = {}$".format(epsilon)
        window = r"$w = {}$".format(window)
        text = "Algorithm " + algorithm + " with " + epsilon
        if window:
            text += " and " + window
        return text



CAExample()

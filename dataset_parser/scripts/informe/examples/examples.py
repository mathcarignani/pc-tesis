import sys
sys.path.append('.')

# import matplotlib
# import numpy as np
import matplotlib.pyplot as plt
from scripts.informe.plot.plot_constants import PlotConstants
from scripts.informe.examples.examples_base import ExamplesBase

plt.rcParams["mathtext.fontset"] = "cm"

class Examples(ExamplesBase):
    PATH = '/Users/pablocerve/Documents/FING/Proyecto/pc-tesis/dataset_parser/scripts/informe/examples/all/'

    def __init__(self):
        self.original = [1, 1, 1, 1, 1, 2, 3, 3, 4, 2, 1, 1]
        self.decoded = []
        self.plot_values = []
        self.arrows = []

    def common(self, filename, algorithm, epsilon=1, window=None):
        # print(plt.rcParams["figure.figsize"]) # [6.4, 4.8]
        plt.rcParams["figure.figsize"] = [8, 3.48]
        scatter_x = range(len(self.original))
        fig, ax = plt.subplots()

        # original values
        ax.scatter(scatter_x, self.original, c=self.COLOR_ORIG, marker='x', zorder=2, label=self.LABEL_ORIG)

        # decoded values
        ax.scatter(scatter_x, self.decoded, c=self.COLOR_DECO, marker='o', zorder=1, label=self.encoded_label(algorithm))

        # decoded lines
        for p in self.plot_values:
            ax.plot(p['x_values'], p['y_values'], c=self.COLOR_DECO, zorder=1)

        for plot in self.arrows:
            ExamplesBase.plot_arrows(ax, plot, self.COLOR_LINE, 0.3, 0.6)

        ax.set(xlabel=self.XLABEL, ylabel=self.YLABEL, title=self.title(algorithm, epsilon, window))
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
        # plt.show()

    def encoded_label(self, algorithm):
        return self.LABEL_DECO # + " (" + algorithm + ")"

    def title(self, algorithm, epsilon, window):
        epsilon = r"$\epsilon = {}$".format(epsilon)
        text = "Algorithm " + algorithm + " with " + epsilon
        if window:
            window = r"$w = {}$".format(window)
            text += " and " + window
        return text

    def pwlh_int(self):
        self.decoded =  [1, 1, 1, 1, 1, 2, 3, 3, 4, 2, 1, 1]
        self.plot_values = []
        self.common("pwlh_int.pdf", 'PWLHInt', 1, 256)

    def sf(self):
        self.decoded =  [0, 1, 1, 2, 2, 2, 3, 3, 4, 3, 2, 0]
        self.plot_values = [
             {'x_values': [0,8], 'y_values': [0.27,3.72]},
             {'x_values': [8,11], 'y_values': [3.72,0.386]},
        ]
        self.common("sf.pdf", 'SF', 1, None)


Examples().pwlh_int()
Examples().sf()

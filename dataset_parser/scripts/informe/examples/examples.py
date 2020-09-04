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
        window = r"$w = {}$".format(window)
        text = "Algorithm " + algorithm + " with " + epsilon
        if window:
            text += " and " + window
        return text

    def pca(self):
        self.decoded =  [1, 1, 1, 1, 2, 2, 2, 2, 4, 2, 1, 1]
        self.plot_values = [
            {'x_values': [0,3], 'y_values': [1,1]},
            {'x_values': [4,7], 'y_values': [2,2]}
        ]
        self.arrows = [
            {'x': 0, 'y': 1, 'touch_above': True, 'touch_below': True},
            {'x': 4, 'y': 2, 'touch_above': True}
        ]
        self.common("pca.pdf", 'PCA', 1, 4)

    def apca(self):
        self.decoded =  [2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 1, 1]
        self.plot_values = [
            {'x_values': [0,7], 'y_values': [2,2]},
            {'x_values': [8,9], 'y_values': [3,3]},
            {'x_values': [10,11], 'y_values': [1,1]}
        ]
        self.arrows = [
            {'x': 0, 'y': 2, 'touch_above': True},
            {'x': 8, 'y': 3, 'touch_below': True},
            {'x': 10, 'y': 1, 'touch_above': True, 'touch_below': True}
        ]
        self.common("apca.pdf", 'APCA', 1, 256)

    def ca(self):
        self.decoded =  [1, 1, 1, 2, 2, 2, 3, 4, 4, 2, 2, 1]
        self.plot_values = [
            {'x_values': [0,5], 'y_values': [1,2]},
            {'x_values': [6,8], 'y_values': [3,4]},
            {'x_values': [9,11], 'y_values': [2,1]}
        ]
        self.common("ca.pdf", 'CA', 1, 256)

    def pwlh(self):
        self.decoded =  [0, 1, 1, 1, 2, 2, 3, 3, 3, 2, 1, 1]
        self.plot_values = [
            {'x_values': [0,8], 'y_values': [0.25,3.25]},
            {'x_values': [9,11], 'y_values': [1.75,0.75]}
        ]
        self.common("pwlh.pdf", 'PWLH', 1, 256)

    def pwlh_int(self):
        self.decoded =  [1, 1, 1, 1, 1, 2, 3, 3, 4, 2, 1, 1]
        self.plot_values = []
        self.common("pwlh_int.pdf", 'PWLHInt', 1, 256)

    def sf(self):
        self.decoded =  [0, 1, 1, 2, 2, 2, 3, 3, 4, 3, 2, 0]
        self.plot_values = []
        self.common("sf.pdf", 'SF', 1, 256)

    def fr(self):
        self.decoded =  [1, 1, 1, 2, 2, 2, 3, 3, 4, 3, 2, 1]
        self.plot_values = []
        self.common("fr.pdf", 'FR', 1, None)




Examples().pca()
Examples().apca()
Examples().ca()
Examples().pwlh()
Examples().pwlh_int()
Examples().sf()
Examples().fr()

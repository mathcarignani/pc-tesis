import sys
sys.path.append('.')

# import matplotlib
import numpy as np
import matplotlib.pyplot as plt
from scripts.informe.plot.plot_constants import PlotConstants
from scripts.informe.examples.examples_base import ExamplesBase

plt.rcParams["mathtext.fontset"] = "cm"

class PCAExample(ExamplesBase):
    PATH = '/Users/pablocerve/Documents/FING/Proyecto/pc-tesis/dataset_parser/scripts/informe/examples/pca/'
    LOW_ALPHA = 0.3
    LOWER_ALPHA = 0.2

    def __init__(self):
        self.algorithm = "PCA"
        self.original = [1, 1, 1, 1, 1, 2, 3, 3, 4, 2, 1, 1]
        self.decoded =  [1, 1, 1, 1, 2, 2, 2, 2, 4, 2, 1, 1]
        self.copy_decoded = list.copy(self.decoded)
        self.plot_values = []
        self.arrows = []

        self.pca1("pca1.pdf", 0, 11)
        self.pca2("pca2.pdf", 1, 3)
        self.pca3("pca3.pdf", 2, 7)
        self.pca4("pca4.pdf", 3, 11)

    def pca1(self, filename, step, index):
        self.decoded = []
        self.common(filename, step, index)

    def pca2(self, filename, step, index):
        self.decoded = self.copy_decoded[0:4]
        self.plot_values = [{'x_values': [0,3], 'y_values': [1,1]}]
        self.arrows = [{'x': 0, 'y': 1, 'touch_above': True, 'touch_below': True}]
        self.common(filename, step, index)

    def pca3(self, filename, step, index):
        self.decoded = self.copy_decoded[0:8]
        self.plot_values.append({'x_values': [4,7], 'y_values': [2,2]})
        self.arrows = [{'x': 4, 'y': 2, 'touch_above': True}]
        self.common(filename, step, index)

    def pca4(self, filename, step, index):
        self.decoded = self.copy_decoded[0:12]
        self.arrows = []
        self.common(filename, step, index)

    def plot_original_values(self, ax, index):
        scatter_x_alpha = range(index, len(self.original))
        original_alpha = self.original[index:len(self.original) + 1]
        ax.scatter(scatter_x_alpha, original_alpha, c=self.COLOR_ORIG, marker='x', zorder=3, alpha=self.LOWER_ALPHA)

        scatter_x_black = range(index+1)
        original_black = self.original[0:index+1]
        ax.scatter(scatter_x_black, original_black, c=self.COLOR_ORIG, marker='x', zorder=3, label=self.LABEL_ORIG)

    def common(self, filename, step, index):
        # print(plt.rcParams["figure.figsize"]) # [6.4, 4.8]
        plt.rcParams["figure.figsize"] = [8, 3.48]
        scatter_x = range(len(self.original))
        fig, ax = plt.subplots()

        self.plot_original_values(ax, index)

        # decoded values
        x_decoded = scatter_x[0:len(self.decoded)]
        ax.scatter(x_decoded, self.decoded, c=self.COLOR_DECO, marker='o', zorder=2, label=self.encoded_label())

        # decoded lines
        for p in self.plot_values:
            ax.plot(p['x_values'], p['y_values'], c=self.COLOR_DECO, zorder=1)

        for plot in self.arrows:
            ExamplesBase.plot_arrows(ax, plot, self.COLOR_LINE)

        ax.set(xlabel=self.XLABEL, ylabel=self.YLABEL, title=self.title(self.algorithm, 1, 256, step))
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


PCAExample()

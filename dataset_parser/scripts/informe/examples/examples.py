import sys
sys.path.append('.')

# import matplotlib
# import numpy as np
import matplotlib.pyplot as plt
from scripts.informe.plot.plot_constants import PlotConstants

plt.rcParams["mathtext.fontset"] = "cm"

class Examples(object):
    LABEL_ORIG = 'original value'
    LABEL_DECO = 'encoded value'
    COLOR_ORIG = 'navy'
    COLOR_DECO = 'orange'
    YLABEL = 'value'
    XLABEL = 'time'
    PATH = '/Users/pablocerve/Documents/FING/Proyecto/pc-tesis/dataset_parser/scripts/informe/examples/'

    def __init__(self):
        pass

    def common_pca_apca(self, original, plot_values, scatter_values, filename, algorithm):
        print(plt.rcParams["figure.figsize"]) # [6.4, 4.8]
        plt.rcParams["figure.figsize"] = [8, 3.48]
        scatter_x = range(len(original))
        fig, ax = plt.subplots()

        # original values
        ax.scatter(scatter_x, original, c=self.COLOR_ORIG, marker='x', zorder=2, label=self.LABEL_ORIG)

        # decoded values
        for index, s in enumerate(scatter_values):
            x_values = scatter_x[s['begin']:s['end'] + 1]
            label = self.encoded_label(algorithm) if index == 0 else None
            ax.scatter(x_values, s['y_values'], c=self.COLOR_DECO, marker='o', zorder=1, label=label)

        # decoded lines
        for p in plot_values:
            ax.plot(p['x_values'], p['y_values'], c=self.COLOR_DECO, zorder=1)

        ax.set(xlabel=self.XLABEL, ylabel=self.YLABEL, title=self.title(algorithm))
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

    def pca(self):
        original = [1, 1, 1, 1, 1, 2, 3, 3, 4, 2, 1, 1]
        plot_values = [
            {'x_values': [0,3], 'y_values': [1,1]},
            {'x_values': [4,7], 'y_values': [2,2]}
        ]
        scatter_values = [
            {'begin': 0, 'end': 3, 'y_values': [1] * 4},
            {'begin': 4, 'end': 7, 'y_values': [2] * 4},
            {'begin': 8, 'end': 11, 'y_values': original[8:12]},
        ]
        self.common_pca_apca(original, plot_values, scatter_values, "1.pca.pdf", 'PCA')


    def apca(self):
        original = [1, 1, 1, 1, 1, 2, 3, 3, 4, 2, 1, 1]
        plot_values = [
            {'x_values': [0,7], 'y_values': [2,2]},
            {'x_values': [8,9], 'y_values': [3,3]},
            {'x_values': [10,11], 'y_values': [1,1]}
        ]
        scatter_values = [
            {'begin': 0, 'end': 7, 'y_values': [2] * 8},
            {'begin': 8, 'end': 9, 'y_values': [3] * 2},
            {'begin': 10, 'end': 11, 'y_values': [1] * 2},
        ]
        self.common_pca_apca(original, plot_values, scatter_values, "2.apca.pdf", 'APCA')

    def encoded_label(self, algorithm):
        return self.LABEL_DECO # + " (" + algorithm + ")"

    def title(self, algorithm, epsilon=1, window=4):
        text = "Algorithm " + algorithm + " with " + r"$\epsilon = 1$" + " and " + r"$w = 4$"
        return text


Examples().pca()
Examples().apca()

import sys
sys.path.append('.')

import numpy as np
import matplotlib.pyplot as plt


class SinglePlot(object):
    WINDOWS = [4, 8, 16, 32, 64, 128, 256]

    def __init__(self, algorithm):
        self.algorithm = algorithm
        self.values0 = []
        self.values3 = []
        self.current_plot = []

        self.windows = []
        self.expected_window = 4

    @classmethod
    def plot_value(cls, value0, value3):
        if value0 == value3:
            return 0
        elif value0 > value3:  # map to positive
            return float(value0) / float(value3) - 1
        else:  # value3 > value0  # map to negative
            return (- float(value3) / float(value0)) + 1

    def check_window(self, window):
        if window != self.expected_window:
            print(self.expected_window)
            print(window)
            raise Exception("ERROR: check_window")
        self.windows.append(window)
        self.expected_window *= 2

    def add_values(self, window, value0, value3):
        self.check_window(window)
        self.values0.append(value0)
        self.values3.append(value3)
        value = self.plot_value(value0, value3)
        self.current_plot.append(value)

    def ylim(self):
        max_value = max([abs(value) for value in self.current_plot])  # 1.27
        max_value_int = int(max_value)  # 1
        max_value_decimal = max_value - max_value_int  # 0.27
        most_significant = int(max_value_decimal*10)  # 2
        result = max_value_int + float(most_significant + 1) / 10  # 1.3
        return result

    def check_windows(self):
        if self.windows != self.WINDOWS:
            print self.windows
            raise Exception("ERROR: plot 1")

    @classmethod
    def xticklabels(cls):
        xticklabels = ['']
        for index, value in enumerate(cls.WINDOWS):
            power = index + 2
            label = r"$2^{}$".format(power)  # 2^power
            xticklabels.append(label)
        return xticklabels

    def plot(self, ax, first_graph, ylim):


        # plot
        color = ['lightgreen' if item > 0 else 'red' for item in self.current_plot]
        x_axis = list(xrange(len(self.current_plot)))
        ax.scatter(x=x_axis, y=self.current_plot, c=color)
        ax.grid(True)

        ax.set_xticklabels(self.xticklabels())

        ax.title.set_text(self.algorithm)
        ax.set_xlabel('Window Size')
        if first_graph:
            ax.set_ylabel('Relative Difference')
        else:
            ax.set_yticklabels([])

        ax.set_xlim(left=-1, right=7)
        ax.set_ylim(top=ylim, bottom=-ylim)

        # horizontal line on 0
        ax.axhline(y=0, color='blue', linestyle='-')


class Plotter(object):
    def __init__(self, filename, column_index):
        self.filename = filename
        self.column_index = column_index
        self.plots = []
        self.single_plot = None

    def begin_algorithm(self, algorithm):
        self.single_plot = SinglePlot(algorithm)

    def end_algorithm(self):
        self.single_plot.check_windows()
        self.plots.append(self.single_plot)

    def add_values(self, window, value0, value3):
        self.single_plot.add_values(window, value0, value3)

    def y_lim(self):
        max_y_lim = 0
        for single_plot in self.plots:
            ylim = single_plot.ylim()
            if ylim > max_y_lim:
                max_y_lim = ylim
        return max_y_lim

    def plot(self):
        y_lim = self.y_lim()
        subplot_begin = 100 + 10*len(self.plots)

        white_background = (1, 1, 1)
        fig = plt.figure(figsize=(15, 8), facecolor=white_background)
        fig.suptitle(self.filename + ' - col = ' + str(self.column_index), fontsize=20)
        for index, single_plot in enumerate(self.plots):
            ax = fig.add_subplot(subplot_begin+1+index)
            single_plot.plot(ax, index == 0, y_lim)
        fig.subplots_adjust(wspace=0.05)
        # fig.set_tight_layout(True)
        fig.subplots_adjust(left=0.06, right=0.98, top=0.88)
        plt.show()


plotter = Plotter('filename.csv', 1)
for x in xrange(6):
    coder = 'Coder ' + str(x + 1)
    plotter.begin_algorithm(coder)
    plotter.add_values(4, 779670, 759969)
    plotter.add_values(8, 988620, 838923)
    plotter.add_values(16, 1053306, 1054779)
    plotter.add_values(32, 1054368, 1053153)
    plotter.add_values(64, 1052724, 1051509)
    plotter.add_values(128, 1051908, 1050693)
    plotter.add_values(256, 1051500, 1050285)
    plotter.end_algorithm()
plotter.plot()

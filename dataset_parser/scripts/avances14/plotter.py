import sys
sys.path.append('.')

import numpy as np
import matplotlib.pyplot as plt


class SinglePlot(object):
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
        if self.windows != [4, 8, 16, 32, 64, 128, 256]:
            print self.windows
            raise Exception("ERROR: plot 1")

    def plot(self, plt, first_graph, ylim):
        # add ticks with the window values
        x = list(xrange(len(self.current_plot)))
        plt.xticks(x, [0] + self.windows)

        color = ['lightgreen' if item > 0 else 'red' for item in self.current_plot]
        plt.scatter(x=x, y=self.current_plot, c=color)
        plt.grid(True)

        plt.title(self.algorithm)
        plt.xlabel('Window Size')
        if first_graph:
            plt.ylabel('Relative Difference')
        else:
            pass

        plt.xlim(left=-1, right=7)
        plt.ylim(top=ylim, bottom=-ylim)

        # horizontal line on 0
        plt.axhline(y=0, color='blue', linestyle='-')


class Plotter(object):
    def __init__(self):
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
        for index, single_plot in enumerate(self.plots):
            subplot_index = subplot_begin+index+1
            plt.subplot(subplot_index)
            single_plot.plot(plt, index == 0, y_lim)

        plt.show()


plotter = Plotter()
plotter.begin_algorithm('PCA1')
plotter.add_values(4, 779670, 759969)
plotter.add_values(8, 988620, 838923)
plotter.add_values(16, 1053306, 1054779)
plotter.add_values(32, 1054368, 1053153)
plotter.add_values(64, 1052724, 1051509)
plotter.add_values(128, 1051908, 1050693)
plotter.add_values(256, 1051500, 1050285)
plotter.end_algorithm()
plotter.begin_algorithm('PCA2')
plotter.add_values(4, 779670, 759969)
plotter.add_values(8, 988620, 838923)
plotter.add_values(16, 1053306, 1054779)
plotter.add_values(32, 1054368, 1053153)
plotter.add_values(64, 1052724, 1051509)
plotter.add_values(128, 1051908, 1050693)
plotter.add_values(256, 1051500, 1050285)
plotter.end_algorithm()
plotter.begin_algorithm('PCA3')
plotter.add_values(4, 779670, 759969)
plotter.add_values(8, 988620, 838923)
plotter.add_values(16, 1053306, 1054779)
plotter.add_values(32, 1054368, 1053153)
plotter.add_values(64, 1052724, 1051509)
plotter.add_values(128, 1051908, 1050693)
plotter.add_values(256, 1051500, 1050285)
plotter.end_algorithm()


plotter.plot()

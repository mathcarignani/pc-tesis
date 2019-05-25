import sys
sys.path.append('.')

import numpy as np
import matplotlib.pyplot as plt


class Plotter(object):
    def __init__(self):
        self.current_plot = []
        self.windows = [0]
        self.current_window = 4

    @classmethod
    def plot_value(cls, value0, value3):
        if value0 == value3:
            return 0
        elif value0 > value3:  # map to positive
            return float(value0) / float(value3) - 1
        else:  # value3 > value0  # map to negative
            return (- float(value3) / float(value0)) + 1

    def check_window(self, window):
        if window != self.current_window:
            print(self.current_window)
            print(window)
            raise "ERROR: check_window"
        self.windows.append(window)
        self.current_window *= 2

    def add_values(self, window, value0, value1):
        self.check_window(window)
        value = self.plot_value(value0, value1)
        self.current_plot.append(value)

    def print_current_plot(self):
        print self.current_plot

    def plot(self):

        fig, ax = plt.subplots()
        fig.canvas.draw()

        ax.set_xticklabels(self.windows)
        color = ['lightgreen' if item > 0 else 'red' for item in self.current_plot]
        plt.scatter(x=list(xrange(len(self.current_plot))), y=self.current_plot, c=color)
        plt.grid(True)

        plt.xlabel('Window Size')
        plt.ylabel('Relative Difference')

        plt.xlim(left=-1, right=7)
        plt.ylim(top=0.2, bottom=-0.2)

        # horizontal line on 0
        plt.axhline(y=0, color='blue', linestyle='-')
        plt.show()

plotter = Plotter()
plotter.add_values(4, 779670, 759969)
plotter.add_values(8, 988620, 838923)
plotter.add_values(16, 1053306, 1054779)
plotter.add_values(32, 1054368, 1053153)
plotter.add_values(64, 1052724, 1051509)
plotter.add_values(128, 1051908, 1050693)
plotter.add_values(256, 1051500, 1050285)
plotter.print_current_plot()

plotter.plot()

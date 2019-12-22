import sys
sys.path.append('.')

import matplotlib.pyplot as plt


class PlotUtils(object):
    @classmethod
    def horizontal_line(cls, ax, y, color):
        # https://stackoverflow.com/a/33382750/4547232
        ax.axhline(y=y, color=color, linestyle='-', zorder=0)

    @classmethod
    def hide_ticks(cls, ax):
        # https://stackoverflow.com/a/29988431/4547232
        ax.tick_params(axis=u'both', which=u'both', length=0)

    @classmethod
    def create_figure(cls, figsize_h, figsize_v, fig_title):
        white_background = (1, 1, 1)
        figure = plt.figure(figsize=(figsize_h, figsize_v), facecolor=white_background)
        figure.suptitle(fig_title, fontsize=20)
        return figure

    @classmethod
    def sorted(cls, array):
        return all(array[i] <= array[i+1] for i in range(len(array)-1))

    @classmethod
    def sorted_dec(cls, array):
        return all(array[i] >= array[i+1] for i in range(len(array)-1))
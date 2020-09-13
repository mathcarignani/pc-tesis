import sys
sys.path.append('.')


import matplotlib as mpl
import matplotlib.pyplot as plt
plt.rcParams["mathtext.fontset"] = "cm"
from scripts.informe.plot.plot_constants import PlotConstants

class ExamplesBase(object):
    FONT_SIZE = 15
    EPSILON = r"$\epsilon$"
    YLABEL = 'data'
    XLABEL = 'timestamp'
    LABEL_ORIG = 'original value'
    LABEL_DECO = 'encoded value'
    COLOR_ORIG = 'navy'
    COLOR_DECO = 'orange'
    COLOR_LINE = 'seagreen'
    LOW_ALPHA = 0.3
    LOWER_ALPHA = 0.2
    INVISIBLE_ALPHA = 0.1

    def __init__(self):
        self.window = 256

    @classmethod
    def plot_patch(cls, ax, patch):
        patch = mpl.patches.Rectangle(patch['point'], patch['w'], patch['h'],
                                      color=cls.COLOR_LINE, zorder=0, alpha=cls.INVISIBLE_ALPHA)
        ax.add_patch(patch)

    @classmethod
    def plot_arrows(cls, ax, plot, color, alpha=1, epsilon_alpha=1):
        c, a = color, alpha

        x, y = plot['x'], plot['y']
        dx, dy = 0, 1
        hw, hl = 0.1, 0.1

        # epsilon text
        ax.text(x + 0.1, y + 0.4, cls.EPSILON, fontsize=cls.FONT_SIZE, c=c, alpha=epsilon_alpha)
        ax.text(x + 0.1, y - 0.55, cls.EPSILON, fontsize=cls.FONT_SIZE, c=c, alpha=epsilon_alpha)

        m = 0 if plot.get('touch_all') else 0.08

        # arrows above the point
        diff = 0 if plot.get('touch_above') else m
        ax.arrow(x, y+m, dx, dy-m-diff, head_width=hw, head_length=hl, color=c, length_includes_head=True, alpha=a)
        ax.arrow(x, y+dy-diff, dx, -(dy-m-diff), head_width=hw, head_length=hl, color=c, length_includes_head=True, alpha=a)

        # arrows below the point
        diff = 0 if plot.get('touch_below') else m
        ax.arrow(x, y-m, dx, -(dy-m-diff), head_width=hw, head_length=hl, color=c, length_includes_head=True, alpha=a)
        ax.arrow(x, y-dy+diff, dx, dy-m-diff, head_width=hw, head_length=hl, color=c, length_includes_head=True, alpha=a)

    def plot_original_values(self, ax, index):
        scatter_x_alpha = range(index, len(self.original))
        original_alpha = self.original[index:len(self.original) + 1]
        ax.scatter(scatter_x_alpha, original_alpha, c=self.COLOR_ORIG, marker='x', zorder=3, alpha=self.LOWER_ALPHA)

        scatter_x_black = range(index+1)
        original_black = self.original[0:index+1]
        ax.scatter(scatter_x_black, original_black, c=self.COLOR_ORIG, marker='x', zorder=3, label=self.LABEL_ORIG)

    def common(self, filename, step, index, title=True):
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

        for patch in self.patches:
            ExamplesBase.plot_patch(ax, patch)

        ax.set(xlabel=self.XLABEL, ylabel=self.YLABEL) #, title=title_str)
        title_obj = plt.title(self.title(self.algorithm, 1, step))
        plt.setp(title_obj, color='black' if title else 'white')

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
        fig.savefig(self.path + filename)

    def encoded_label(self):
        return self.LABEL_DECO

    def title(self, algorithm, epsilon, step):
        epsilon = r"$\epsilon = {}$".format(epsilon)
        window = r"$w = {}$".format(self.window)
        text = "Algorithm " + algorithm + " with " + epsilon + " and " + window + " - STEP " + str(step)
        return text

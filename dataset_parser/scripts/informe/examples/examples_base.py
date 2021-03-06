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
    LABEL_ENCO_DECO = 'encoded/decoded sample'
    COLOR_ORIG = 'navy'
    COLOR_DECO = 'orange'
    COLOR_ENCO = 'red'
    COLOR_LINE = 'seagreen'
    ALPHA_HIGH = 1
    ALPHA_MED = 0.5
    ALPHA_LOW = 0.3
    ALPHA_LOWER = 0.2
    ALPHA_INV = 0.1
    SMAX_MAR = 0.06
    SMIN_MAR = 0.1

    def __init__(self):
        self.labels = None
        self.window = 256
        self.encoded_points = []
        self.patches = []
        self.arrows = []
        self.plot_original = True
        self.xlim_right = 12
        self.figsize = [8, 3.48]
        self.first_timestamp = 1
        self.label_orig = 'sample'
        self.label_enco = 'encoded point'
        self.label_deco = 'decoded sample'
        self.xs, self.yx, self.words = [], [], []
        self.epsilon = 1

    @classmethod
    def plot_patch(cls, ax, patch):
        if patch.get('polygon'):
            patch = mpl.patches.Polygon(patch['points'],
                                        color=cls.COLOR_LINE, zorder=0, alpha=cls.ALPHA_INV)
        else:
            patch = mpl.patches.Rectangle(patch['point'], patch['w'], patch['h'],
                                          color=cls.COLOR_LINE, zorder=0, alpha=cls.ALPHA_INV)
        ax.add_patch(patch)

    @classmethod
    def plot_arrows(cls, ax, plot, color, alpha=1, epsilon_alpha=1):
        c, a = color, alpha

        x, y = plot['x'], plot['y']
        dx, dy = 0, 1
        hw, hl = 0.1, 0.1

        # epsilon text
        left = -0.35 if plot.get('left') else 0
        x_coord = x + 0.1 + left
        if not plot.get('no_legend_above') and not plot.get('only_below') :
            ax.text(x_coord, y + 0.4, cls.EPSILON, fontsize=cls.FONT_SIZE, c=c, alpha=epsilon_alpha)
        if not plot.get('only_above'):
            ax.text(x_coord, y - 0.55, cls.EPSILON, fontsize=cls.FONT_SIZE, c=c, alpha=epsilon_alpha)

        m = 0 if plot.get('touch_all') else 0.08

        # arrows above the point
        if not plot.get('only_below'):
            diff = 0 if plot.get('touch_above') else m
            ax.arrow(x, y+m, dx, dy-m-diff, head_width=hw, head_length=hl, color=c, length_includes_head=True, alpha=a)
            ax.arrow(x, y+dy-diff, dx, -(dy-m-diff), head_width=hw, head_length=hl, color=c, length_includes_head=True, alpha=a)

        # arrows below the point
        if not plot.get('only_above'):
            diff = 0 if plot.get('touch_below') else m
            ax.arrow(x, y-m, dx, -(dy-m-diff), head_width=hw, head_length=hl, color=c, length_includes_head=True, alpha=a)
            ax.arrow(x, y-dy+diff, dx, dy-m-diff, head_width=hw, head_length=hl, color=c, length_includes_head=True, alpha=a)

    def plot_original_values(self, ax, index):
        if not self.plot_original:
            return
        scatter_x_alpha = range(index, len(self.original))
        original_alpha = self.original[index:len(self.original) + 1]
        ax.scatter(scatter_x_alpha, original_alpha, c=self.COLOR_ORIG, marker='x', zorder=3, alpha=self.ALPHA_LOWER, s=25)

        scatter_x_black = range(index+1)
        original_black = self.original[0:index+1]
        ax.scatter(scatter_x_black, original_black, c=self.COLOR_ORIG, marker='x', zorder=3, label=self.label_orig, s=25)

    def plot_encoded_points(self, ax):
        if len(self.encoded_points) == 0:
            return
        x, y = [], []
        for point in self.encoded_points:
            point_x, point_y = point
            x.append(point_x)
            y.append(point_y)
        ax.scatter(x, y, zorder=3, alpha=1, label=self.label_enco, facecolors='none', edgecolors=self.COLOR_ENCO, s=60)

    def plot_decoded_values(self, ax):
        scatter_x = range(len(self.original))
        x_decoded = scatter_x[0:len(self.decoded)]
        label = self.label_deco if len(self.encoded_points) > 0 else self.LABEL_ENCO_DECO
        ax.scatter(x_decoded, self.decoded, c=self.COLOR_DECO, marker='o', zorder=2, label=label)

    def plot_decoded_lines(self, ax, p):
        alpha = p.get('alpha') or self.ALPHA_HIGH
        linestyle = p.get('linestyle') or '-'
        color = p.get('color') or self.COLOR_DECO
        if len(self.encoded_points) > 0 and not p.get('color'):
            color = self.COLOR_ENCO
        ax.plot(p['x_values'], p['y_values'], c=color, zorder=1, linestyle=linestyle, alpha=alpha)

    def common(self, filename, step, index, title=True):
        ax, fig = self.common_1(index)
        self.common_2(ax, fig, step, title, filename)

    def common_1(self, index):
        plt.rcParams["figure.figsize"] = self.figsize
        fig, ax = plt.subplots()
        self.plot_original_values(ax, index)

        return ax, fig

    def common_2(self, ax, fig, step, title, filename):
        self.plot_encoded_points(ax)

        # decoded values
        if len(self.decoded) > 0:
            self.plot_decoded_values(ax)

        # decoded lines
        for p in self.plot_values:
            self.plot_decoded_lines(ax, p)

        for plot in self.arrows:
            ExamplesBase.plot_arrows(ax, plot, self.COLOR_LINE)

        for patch in self.patches:
            ExamplesBase.plot_patch(ax, patch)

        ax.set(xlabel=self.XLABEL, ylabel=self.YLABEL)

        title_obj = plt.title(self.title(step))
        plt.setp(title_obj, color='black' if title else 'white')

        ax.grid(color=PlotConstants.COLOR_SILVER, linestyle='dotted')
        ax.set_axisbelow(True)
        ax.set_ylim(bottom=0, top=4.5)
        ax.set_xlim(left=-1, right=self.xlim_right)
        ax.set_xticks(range(0,self.xlim_right + 1))
        ax.set_yticks(range(0,5))

        ft = self.first_timestamp
        labels = ['t' + str(index) for index in range(ft, len(ax.get_xticklabels()) + ft - 1)] if not self.labels else self.labels
        print(labels)
        ax.set_xticklabels(labels)
        ax.legend(loc='upper left')
        plt.tight_layout()
        fig.savefig(self.path + filename)

    def title(self, step):
        epsilon = r"$\epsilon = {}$".format(self.epsilon)
        window = " and " + r"$w = {}$".format(self.window) if self.window else ""

        text = "Algorithm " + self.algorithm + " with " + epsilon + window + " - STEP " + str(step)
        return text

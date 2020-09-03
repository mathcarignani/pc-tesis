import sys
sys.path.append('.')


class ExamplesCommon(object):
    FONT_SIZE = 15
    EPSILON = r"$\epsilon$"

    @classmethod
    def plot_arrows(cls, ax, plot, color, alpha=1, epsilon_alpha=1):
        c, a = color, alpha
        fontsize = cls.FONT_SIZE
        epsilon = cls.EPSILON

        x, y = plot['x'], plot['y']
        dx, dy = 0, 1
        hw, hl = 0.1, 0.1

        # epsilon text
        ax.text(x + 0.1, y + 0.4, epsilon, fontsize=fontsize, c=c, alpha=epsilon_alpha)
        ax.text(x + 0.1, y - 0.55, epsilon, fontsize=fontsize, c=c, alpha=epsilon_alpha)

        # touch_above, touch_below = plot.get('touch_above'), plot.get('touch_below')

        m = 0.08 # don't touch the point
        # arrows above the point
        diff = 0 if plot.get('touch_above') else m
        ax.arrow(x, y+m, dx, dy-m-diff, head_width=hw, head_length=hl, color=c, length_includes_head=True, alpha=a)
        ax.arrow(x, y+dy-diff, dx, -(dy-m-diff), head_width=hw, head_length=hl, color=c, length_includes_head=True, alpha=a)

        # arrows below the point
        diff = 0 if plot.get('touch_below') else m
        ax.arrow(x, y-m, dx, -(dy-m-diff), head_width=hw, head_length=hl, color=c, length_includes_head=True, alpha=a)
        ax.arrow(x, y-dy+diff, dx, dy-m-diff, head_width=hw, head_length=hl, color=c, length_includes_head=True, alpha=a)

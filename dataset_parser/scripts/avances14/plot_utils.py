
class PlotUtils(object):
    @classmethod
    def horizontal_line(cls, ax, y, color):
        # https://stackoverflow.com/a/33382750/4547232
        ax.axhline(y=y, color=color, linestyle='-', zorder=0)

    @classmethod
    def hide_ticks(cls, ax):
        # https://stackoverflow.com/a/29988431/4547232
        ax.tick_params(axis=u'both', which=u'both', length=0)

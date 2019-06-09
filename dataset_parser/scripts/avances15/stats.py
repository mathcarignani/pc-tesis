import sys
sys.path.append('.')

from scripts.avances14.constants import Constants
from scripts.avances15.plotter2_constants import Plotter2Constants


class RelativeDifferenceStats(object):
    def __init__(self):
        self.total_results = 0
        self.best0_results = 0
        self.best3_results = 0
        self.same_results = 0

    def add_values(self, value0, value3):
        self.total_results += 1
        if value0 == value3:
            self.same_results += 1
        elif value0 < value3:
            self.best0_results += 1
        else:  # value3 < value0
            self.best3_results += 1

    def close(self):
        assert(self.total_results == self.best0_results + self.best3_results + self.same_results)
        assert(self.total_results == 6 * 8)

    def plot(self, ax):
        col_labels = ['BEST', '#', '%']
        row_labels = ['MM=0', 'SAME', 'MM=3']
        results = [self.best0_results, self.same_results, self.best3_results]
        colors = [Plotter2Constants.VALUE0_COLOR, Plotter2Constants.VALUE_SAME, Plotter2Constants.VALUE3_COLOR]
        self.plot_aux(ax, col_labels, zip(results, row_labels, colors))

    def plot_aux(self, ax, col_labels, zipped_values):
        table_values, table_colors = [], []
        for total, label, color in zipped_values:
            percentage = self.percentage(self.total_results, total)
            table_values.append([label, total, percentage])
            cell_color = Constants.COLOR_WHITE if total == 0 else color
            table_colors.append([cell_color, Constants.COLOR_WHITE, Constants.COLOR_WHITE])

        # Draw table
        the_table = ax.table(cellText=table_values, colWidths=[0.12, 0.1, 0.12], cellColours=table_colors,
                             colLabels=col_labels,
                             loc='center right')
        # the_table.auto_set_font_size(True)
        the_table.set_fontsize(14)
        the_table.scale(3, 2)

        # Removing ticks and spines enables you to get the figure only with table
        ax.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
        ax.tick_params(axis='y', which='both', right=False, left=False, labelleft=False)

        for pos in ['right', 'top', 'bottom', 'left']:
            ax.spines[pos].set_visible(False)

    @classmethod
    def percentage(cls, total, value):
        return round((float(100) / float(total)) * value, 2)


class WindowsStats(RelativeDifferenceStats):
    def plot(self, ax):
        col_labels = ['BIG', '#', '%']
        row_labels = ['MM=0', 'SAME', 'MM=3']
        results = [self.best3_results, self.same_results, self.best0_results]
        colors = [Plotter2Constants.VALUE0_COLOR, Plotter2Constants.VALUE_SAME, Plotter2Constants.VALUE3_COLOR]
        self.plot_aux(ax, col_labels, zip(results, row_labels, colors))

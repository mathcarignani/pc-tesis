import sys
sys.path.append('.')

from scripts.avances14.constants import Constants
from scripts.avances15.common_plot import CommonPlot
from scripts.avances15.plotter2_constants import Plotter2Constants


class RelativeDifferenceStats(CommonPlot):
    def __init__(self):
        self.total_results = 0
        self.best0_results = 0
        self.best3_results = 0
        self.same_results = 0
        self.col_labels = ['BEST', '#', '%']
        self.row_labels = ['MM=0', 'SAME', 'MM=3']
        super(RelativeDifferenceStats, self).__init__()

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

    def set_colors_and_labels(self, value0_color, value3_color, label0, label3):
        super(RelativeDifferenceStats, self).set_colors(value0_color, value3_color)
        self.row_labels[0] = label0 or self.row_labels[0]
        self.row_labels[2] = label3 or self.row_labels[2]

    def set_labels(self, col_labels, row_labels):
        self.col_labels = col_labels
        self.row_labels = row_labels

    def plot(self, ax):
        results = [self.best0_results, self.same_results, self.best3_results]
        colors = [self.value0_color, Plotter2Constants.VALUE_SAME, self.value3_color]
        self.plot_aux(ax, self.col_labels, zip(results, self.row_labels, colors))

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
    def __init__(self):
        super(WindowsStats, self).__init__()
        self.set_labels(['BIG', '#', '%'], ['MM=0', 'SAME', 'MM=3'])

    def plot(self, ax):
        results = [self.best3_results, self.same_results, self.best0_results]
        colors = [self.value0_color, Plotter2Constants.VALUE_SAME, self.value3_color]
        self.plot_aux(ax, self.col_labels, zip(results, self.row_labels, colors))

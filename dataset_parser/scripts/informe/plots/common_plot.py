import sys
sys.path.append('.')

from scripts.informe.plot.plot_constants import PlotConstants


class CommonPlot(object):
    def __init__(self):
        # TODO: the following two values are exchanged
        self.value0_color = PlotConstants.VALUE3_COLOR
        self.value3_color = PlotConstants.VALUE0_COLOR
        self.additional_checks = False

    def set_colors(self, value0_color, value3_color):
        self.value0_color = value0_color or self.value0_color
        self.value3_color = value3_color or self.value3_color

    def color_code(self, value, value3_smaller=True):
        if value > 0:
            return self.value3_color if value3_smaller else self.value0_color
        elif value < 0:
            return self.value0_color if value3_smaller else self.value3_color
        else:  # value == 0
            return PlotConstants.VALUE_SAME

    def generate_colors(self, can_be_equal=True):
        colors0, colors3 = [], []
        for value0, value3 in zip(self.values0, self.values3):
            if can_be_equal and value0 == value3:
                colors0.append(PlotConstants.VALUE_SAME)
                colors3.append(PlotConstants.VALUE_SAME)
            else:
                colors0.append(self.value0_color)
                colors3.append(self.value3_color)
        return colors0, colors3

    @classmethod
    def set_lim(cls, ax, ymin, ymax):
        ax.set_ylim(bottom=ymin, top=ymax)

    @classmethod
    def label_title(cls, ax, options, title):
        title_options = options.get('title')
        if title_options:
            fontsize = 15 if isinstance(title_options, bool) else title_options
            title = title.replace("Coder", "")  # "CoderABC" => "ABC"
            ax.set_title(title, fontsize=fontsize)

    @classmethod
    def label_y(cls, ax, options, label, tick_labels=None):
        if not options.get('show_ylabel'):
            ax.set_yticklabels([])
            return
        ax.set_ylabel(label)
        if tick_labels is not None:
            ax.set_yticklabels(tick_labels)

    @classmethod
    def label_x(cls, ax, options, label, tick_labels=None):
        if not options.get('show_xlabel'):
            ax.set_xticklabels([])
            return
        ax.set_xlabel(label)
        if tick_labels is not None:
            ax.set_xticklabels(tick_labels)

    ####################################################################################################################

    @classmethod
    def add_min_max_circles(cls, algorithm, options, ax, x_axis, y_axis):
        dataset_name, col_index = options['pdf_instance'].dataset_name, options['pdf_instance'].col_index

        if dataset_name == "NOAA-SST" and col_index == 1 and algorithm == "CoderPCA":
            # 2-NOAA-SST-1.pdf
            color = PlotConstants.VALUE0_COLOR
        elif dataset_name == "NOAA-SPC-tornado" and col_index == 2 and algorithm == "CoderAPCA":
            # 7-NOAA-SPC-tornado-2.pdf
            color = PlotConstants.VALUE3_COLOR
        else:
            return
        new_x_axis, values = x_axis[-1:], y_axis[-1:]  # last value
        ax.scatter(x=new_x_axis, y=values, zorder=2, facecolors='none', edgecolors=color, s=200)

    @classmethod
    def add_max_circle(cls, algorithm, options, ax, x_axis, y_axis):
        dataset_name, col_index = options['pdf_instance'].dataset_name, options['pdf_instance'].col_index

        if not(dataset_name == "IRKIS" and col_index == 1 and algorithm == "CoderPCA"):
            return

        maximum = max(y_axis) # 10.6830419509284
        if not(10.68 < maximum < 10.69):
            return

        # 1-IRKIS-2-1.pdf
        new_x_axis, values = [x_axis[5]], [y_axis[5]]
        ax.scatter(x=new_x_axis, y=values, zorder=2, facecolors='none', edgecolors=PlotConstants.VALUE0_COLOR, s=200)

    @classmethod
    def circle_table_values(cls, algorithm, options, ax, x_axis, y_axis):
        dataset_name, col_index = options['pdf_instance'].dataset_name, options['pdf_instance'].col_index
        if not(dataset_name == "ElNino" and col_index == 7):
            return
        # 5-ElNino-7.pdf
        new_x_axis, values = x_axis[:], y_axis[:]  # copy lists by value
        if algorithm == "CoderPCA":
            new_x_axis, values = [new_x_axis[0]], [values[0]]  # first value
        elif algorithm == "CoderAPCA":
            new_x_axis, values = new_x_axis[1:], values[1:]  # every value except the first
        else:
            return
        ax.scatter(x=new_x_axis, y=values, zorder=2, facecolors='none', edgecolors='blue', s=200)

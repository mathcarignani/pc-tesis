import sys
sys.path.append('.')

from scripts.compress.experiments_utils import ExperimentsUtils
from scripts.avances.avances14.plotter import Plotter
from scripts.informe.plot.plot_constants import PlotConstants
from scripts.avances.avances15.column import Column
from scripts.avances.avances15.matrix import Matrix
from scripts.avances.avances15.plotter2 import Plotter2


class Plotter3(object):
    def __init__(self, dataset_name):
        self.dataset_name = dataset_name
        self.plotter2_array = []  # one entry for each <file, column_type> combination
        self.number_of_files = len(ExperimentsUtils.dataset_csv_filenames(self.dataset_name))
        self.number_of_column_types = ExperimentsUtils.get_dataset_data_columns_count(self.dataset_name)
        self.total_pages = self.number_of_files * self.number_of_column_types
        self.must_plot = self.number_of_files > 1
        self.plotter_array = []  # one entry for each column_type
        self.global_plotters_array = []  # one for each column_type

    def add_plotter2(self, plotter2):
        assert(isinstance(plotter2, Plotter2))
        self.plotter2_array.append(plotter2)

    def global_plotters(self):
        assert(self.total_pages == len(self.plotter2_array))
        assert self.must_plot
        self.__fill_plotter_array()
        self.global_plotters_array = [Plotter2(plotter) for plotter in self.plotter_array]
        return self.global_plotters_array

    def compare_plotters_0(self):
        return self.__compare_plotters("mode0")

    def compare_plotters_3(self):
        return self.__compare_plotters("mode3")

    def __compare_plotters(self, mode_str):
        result = []
        non_global_plotters = self.plotter2_array
        for plotter_index, plotter2 in enumerate(non_global_plotters):  # one for each <file, column_type> combination
            assert(isinstance(plotter2, Plotter2))
            file_index = plotter_index / self.number_of_column_types  # 0..(total_files-1)
            column_type_i = plotter_index % self.number_of_column_types  # 0..(self.number_of_column_types - 1)
            # print "(file_index, column_type_i) = " + str((file_index, column_type_i))
            new_matrix = Matrix()

            for algo_i, algorithm in enumerate(ExperimentsUtils.ALGORITHMS):
                # print "algorithm = " + algorithm
                new_column = Column(algorithm, mode_str == "mode3")
                column = plotter2.matrix.columns[algo_i]
                tb_plot, ws_plot = column.total_bits_plot, column.windows_plot

                for thre_i, threshold in enumerate(ExperimentsUtils.THRESHOLDS):  # threshold row
                    # print "threshold = " + str(threshold)
                    best_values = self.__generate_best_values(plotter2, ws_plot, tb_plot, column_type_i, algo_i, thre_i, mode_str)
                    # print "str(best_values)"
                    # print str(best_values)
                    new_column.add_values(best_values)
                    new_matrix.add_values(best_values)
                # print "new_column.print_values()"
                # new_column.print_values()
                new_column.close()
                new_matrix.add_column(new_column)
            new_matrix.close()
            # print "new_matrix.print_values()"
            # new_matrix.print_values()
            new_plotter2 = self.__create_plotter2(plotter2.plotter, new_matrix, mode_str)
            # print "new_plotter2.print_values()"
            # new_plotter2.print_values()
            result.append(new_plotter2)
        return result

    def __generate_best_values(self, plotter2, ws_plot, tb_plot, column_type_i, algo_i, thre_i, mode_str):
        window0, window3 = ws_plot.windows0[thre_i], ws_plot.windows3[thre_i]
        value0, value3 = tb_plot.values0[thre_i], tb_plot.values3[thre_i]
        basic_value0 = tb_plot.basic_value0

        best_global_window = self.__get_best_global_window(column_type_i, algo_i, thre_i, mode_str)
        window_value = self.__get_window_value(plotter2, algo_i, thre_i, best_global_window, mode_str)
        # print "best_global_window = " + str(best_global_window)
        # print "window_value = " + str(window_value)
        if mode_str == "mode0":  # value0 remains unchanged
            return {
                'value0': {'min': value0, 'window': window0},
                'value3': {'min': window_value, 'window': best_global_window},
                'basic_value0': basic_value0
            }
        else:  # value3 remains unchanged
            return {
                'value0': {'min': window_value, 'window': best_global_window},
                'value3': {'min': value3, 'window': window3},
                'basic_value0': basic_value0
            }

    @classmethod
    def __get_window_value(cls, plotter2, algo_i, thre_i, best_global_window, mode_str):
        plotter = plotter2.plotter
        assert(isinstance(plotter, Plotter))

        row_plots = plotter.row_plots
        row_plot = row_plots[thre_i]
        row_algorithm_plot = row_plot.plots[algo_i]

        if mode_str == "mode0":  # value0 remains unchanged
            values = row_algorithm_plot.values0
        else:  # value3 remains unchanged
            values = row_algorithm_plot.values3

        # print "values = " + str(values)
        best_global_window_index = ExperimentsUtils.WINDOWS.index(best_global_window)
        return values[best_global_window_index]

    def __get_best_global_window(self, column_type_index, algorithm_index, threshold_index, mode_str):
        assert(len(self.global_plotters_array) > column_type_index)
        plotter2 = self.global_plotters_array[column_type_index]
        columns = plotter2.matrix.columns
        assert(len(columns) > algorithm_index)
        column = columns[algorithm_index]
        windows_plot = column.windows_plot
        if mode_str == "mode0":
            windows = windows_plot.windows0
        else:
            windows = windows_plot.windows3
        assert(len(windows) > threshold_index)
        return windows[threshold_index]

    @classmethod
    def __create_plotter2(cls, plotter, matrix, mode_str):
        plotter2 = Plotter2(plotter)
        plotter2.set_matrix(matrix)
        value0_color = None if mode_str == 'mode0' else PlotConstants.COLOR_GREEN_F
        value3_color = None if mode_str == 'mode3' else PlotConstants.COLOR_GREEN_F
        label0 = None if mode_str == 'mode0' else 'BGW'
        label3 = None if mode_str == 'mode3' else 'BGW'
        plotter2.set_colors(value0_color, value3_color, label0, label3)
        return plotter2

    def __fill_plotter_array(self):
        for column_type_index in range(self.number_of_column_types):
            new_plotter = None
            column_index = column_type_index
            while column_index < self.total_pages:
                current_plotter = self.plotter2_array[column_index].plotter
                new_plotter = current_plotter if new_plotter is None else Plotter.sum(new_plotter, current_plotter)
                column_index += self.number_of_column_types
            self.plotter_array.append(new_plotter)

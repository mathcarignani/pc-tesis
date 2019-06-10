import sys
sys.path.append('.')

from scripts.compress.compress_aux import dataset_csv_filenames, get_dataset_info
from scripts.avances14.plotter import Plotter
from scripts.avances15.plotter2 import Plotter2


class Plotter3(object):
    def __init__(self, dataset_name):
        self.dataset_name = dataset_name
        self.plotter2_array = []  # one for each <file, column_type> combination
        self.number_of_files = len(dataset_csv_filenames(self.dataset_name))
        self.number_of_column_types = get_dataset_info(self.dataset_name)['cols']
        self.total_pages = self.number_of_files * self.number_of_column_types
        self.must_plot = self.number_of_files > 1
        self.plotter_array = []  # one for each column_type

    def add_plotter2(self, plotter2):
        assert(isinstance(plotter2, Plotter2))
        self.plotter2_array.append(plotter2)

    def plotters(self):
        assert(self.total_pages == len(self.plotter2_array))
        assert self.must_plot
        self.__fill_plotter_array()
        return [Plotter2(plotter) for plotter in self.plotter_array]

    def __fill_plotter_array(self):
        # fill self.plotter_array
        print "Plotter3 plot"
        for column_type_index in range(self.number_of_column_types):
            new_plotter = None
            column_index = column_type_index
            while column_index < self.total_pages:
                print "1"
                current_plotter = self.plotter2_array[column_index].plotter
                new_plotter = current_plotter if new_plotter is None else Plotter.sum(new_plotter, current_plotter)
                column_index += self.number_of_column_types

            print "OUTPUT"
            print new_plotter.filename
            print new_plotter.column_index
            print len(new_plotter.row_plots)
            self.plotter_array.append(new_plotter)

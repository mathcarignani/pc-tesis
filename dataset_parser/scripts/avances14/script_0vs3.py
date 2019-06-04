import sys
sys.path.append('.')

from matplotlib.backends.backend_pdf import PdfPages

from scripts.avances14.row_plot import RowPlot
from scripts.avances14.plotter import Plotter
from scripts.avances15.plotter2 import Plotter2
from file_utils.csv_utils.csv_reader import CSVReader
from scripts.compress.compress_aux import DATASETS_ARRAY, CSV_PATH
from scripts.utils import csv_files_filenames
from scripts.avances14.constants import Constants


class Script(object):
    def __init__(self, filename, column_index):
        path = "/Users/pablocerve/Documents/FING/Proyecto/results/avances-13/3-0vs3"
        self.input_file = CSVReader(path, "0vs3.csv")
        self.filename = filename
        self.column_index = column_index
        self.plotter = None
        self.row_plot = None
        self.__goto_file_start()

    def run(self):
        print "FILENAME = " + self.filename + " - COLUMN_INDEX = " + str(self.column_index)
        self.plotter = Plotter(self.filename, self.column_index)
        for threshold in Constants.THRESHOLDS:
            self.row_plot = RowPlot(threshold)

            for algorithm in Constants.ALGORITHMS:
                self.row_plot.begin_algorithm(algorithm)
                self.__find_combination(self.filename, algorithm, threshold)

                for window_size in Constants.WINDOWS:
                    self.__find_next_line(6, window_size, True)
                    window, value0, value3 = self.__parse_line_values()
                    self.row_plot.add_values(window, value0, value3)

                self.row_plot.end_algorithm()
                self.__goto_file_start()
            self.plotter.add_row_plot(self.row_plot)

    def plot1(self):
        return self.plotter.plot()

    def plot2(self):
        plotter2 = Plotter2(self.plotter)
        return plotter2.plot()

    def __find_combination(self, filename, algorithm, threshold):
        self.__find_next_line(Constants.INDEX_FILENAME, filename, False)
        self.__find_next_line(Constants.INDEX_ALGORITHM, algorithm, False)
        self.__find_next_line(Constants.INDEX_THRESHOLD, threshold, True)

    def __matching_line(self, index, value, is_integer):
        value_in_index = self.line[index]
        if len(value_in_index) == 0:
            return False
        value_to_compare = int(value_in_index) if is_integer else value_in_index
        return value == value_to_compare

    def __read_line(self):
        self.line = self.input_file.read_line()
        self.line_count += 1

    def __find_next_line(self, index, value, is_integer):
        if self.line_count > 0 and self.__matching_line(index, value, is_integer):
            return True

        while self.input_file.continue_reading:
            self.__read_line()
            if self.__matching_line(index, value, is_integer):
                return True
        raise Exception("ERROR: __find_next_line")

    def __parse_line_values(self):
        window = int(self.line[Constants.INDEX_WINDOW])
        value0_index = Constants.INDEX_WINDOW + self.column_index
        value0 = self.__get_int(self.line[value0_index])
        value3 = self.__get_int(self.line[value0_index + 7])
        return window, value0, value3

    @classmethod
    def __get_int(cls, string):
        # string = "1,285,310 - W - 1.36"
        return int(string.split()[0].replace(",", ""))

    def __goto_file_start(self):
        self.input_file.goto_row(0)
        self.line = None
        self.line_count = 0


def add_to_pdf(pdf, filename, column_index):
    script = Script(filename, column_index)
    script.run()
    # fig, plt = script.plot1()
    fig, plt = script.plot2()

    # plt.show(); exit(0)  # uncomment to generate a single graph
    pdf.savefig(fig)
    plt.close()


def create_pdf(dataset_id, dataset_dictionary):
    input_path = CSV_PATH + dataset_dictionary['folder']
    dataset_name = dataset_dictionary['name']
    cols = dataset_dictionary['cols']
    with PdfPages("scripts/avances14/graphs/" + str(dataset_id) + "-" + dataset_name + ".pdf") as pdf:
        for id1, input_filename in enumerate(csv_files_filenames(input_path)):
            if dataset_name in ["NOAA-SST", "NOAA-ADCP"] and id1 >= 3:
                continue
            for col_index in range(cols):
                add_to_pdf(pdf, input_filename, col_index + 1)


for ds_id, ds_dict in enumerate(DATASETS_ARRAY):
    create_pdf(ds_id + 1, ds_dict)

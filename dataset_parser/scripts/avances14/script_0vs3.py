import sys
sys.path.append('.')

from matplotlib.backends.backend_pdf import PdfPages

# import matplotlib.pyplot as plt
# import matplotlib
# matplotlib.rcParams['text.usetex']=True
# matplotlib.rcParams['text.latex.unicode']=True
#
# string = r'z=${value}^{upper}_{lower}$'.format(
#                 value='{' + str(0.27) + '}',
#                 upper='{+' + str(0.01) + '}',
#                 lower='{-' + str(0.01) + '}')
# string = r'z=${value}^{upper}_{lower}$'.format(
#                 value='{' + str(0.27) + '}',
#                 upper='{+' + str(0.01) + '}',
#                 lower='{-' + str(0.01) + '}')
# print(string)
#
# fig = plt.figure(figsize=(3,1))
# fig.text(0.1,0.5,string,size=24,va='center')
# fig.savefig('issue5076.pdf')
# fig.savefig('issue5076.png')
# exit(1)

from scripts.avances14.row_plot import RowPlot
from scripts.avances14.plotter import Plotter
from scripts.avances15.plotter2 import Plotter2
from scripts.avances16.plotter3 import Plotter3
from file_utils.csv_utils.csv_reader import CSVReader
from scripts.compress.compress_aux import DATASETS_ARRAY
from scripts.avances14.constants import Constants
from scripts.compress.compress_aux import dataset_csv_filenames


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
                basic_value0 = self.__find_combination(self.filename, algorithm, threshold)

                for window_size in Constants.WINDOWS:
                    self.__find_next_line(Constants.INDEX_WINDOW, window_size, True)
                    window, value0, value3 = self.__parse_line_values()
                    self.row_plot.add_values(window, value0, value3, basic_value0)

                self.row_plot.end_algorithm()
                self.__goto_file_start()
            self.plotter.add_row_plot(self.row_plot)

    def plotter1(self):
        return self.plotter

    def plotter2(self):
        return Plotter2(self.plotter)

    def __find_combination(self, filename, algorithm, threshold):
        self.__find_next_line(Constants.INDEX_FILENAME, filename, False)
        basic_value0_index = self.__get_value0_index()
        basic_value0 = self.__get_int(self.line[basic_value0_index])
        self.__find_next_line(Constants.INDEX_ALGORITHM, algorithm, False)
        self.__find_next_line(Constants.INDEX_THRESHOLD, threshold, True)
        return basic_value0

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
        value0_index = self.__get_value0_index()
        value0 = self.__get_int(self.line[value0_index])
        value3 = self.__get_int(self.line[value0_index + Constants.MAX_COLUMN_TYPES])
        return window, value0, value3

    def __get_value0_index(self):
        return Constants.INDEX_WINDOW + self.column_index

    @classmethod
    def __get_int(cls, string):
        # string = "1,285,310 - W - 1.36"
        return int(string.split()[0].replace(",", ""))

    def __goto_file_start(self):
        self.input_file.goto_row(0)
        self.line = None
        self.line_count = 0


class PDFScript(object):
    GRAPH_PATH = "scripts/avances14/graphs/"

    def __init__(self):
        for dataset_id, dataset_dictionary in enumerate(DATASETS_ARRAY):
            self.dataset_id = dataset_id + 1
            self.dataset_name, self.cols = dataset_dictionary['name'], dataset_dictionary['cols']
            self.__create_pdfs_for_dataset()

    def __create_pdfs_for_dataset(self):
        plotter3 = self.__create_pdf1()
        if plotter3.must_plot:
            self.__create_pdf2(plotter3)
            self.__create_pdf3(plotter3)
            self.__create_pdf4(plotter3)
        # exit()

    def __create_pdf1(self):
        print "pdf1"
        with PdfPages(self.__pdf_name("")) as pdf:
            plotter3 = self.__create_pdf1_iteration(pdf)
            return plotter3

    def __create_pdf2(self, plotter3):
        print "pdf2"
        with PdfPages(self.__pdf_name("Global-")) as pdf:
            for plotter in plotter3.global_plotters():
                self.__plot_and_save(pdf, plotter)

    def __create_pdf3(self, plotter3):
        print "pdf3"
        with PdfPages(self.__pdf_name("Globalvs0-")) as pdf:
            for plotter in plotter3.compare_plotters_0():
                self.__plot_and_save(pdf, plotter)

    def __create_pdf4(self, plotter3):
        print "pdf4"
        with PdfPages(self.__pdf_name("Globalvs3-")) as pdf:
            for plotter in plotter3.compare_plotters_3():
                self.__plot_and_save(pdf, plotter)

    def __pdf_name(self, extra):
        print extra
        return self.GRAPH_PATH + extra + str(self.dataset_id) + "-" + self.dataset_name + ".pdf"

    def __create_pdf1_iteration(self, pdf):
        plotter3 = Plotter3(self.dataset_name)
        for file_index, input_filename in enumerate(dataset_csv_filenames(self.dataset_name)):
            for col_index in range(self.cols):
                plotter2 = self.__add_page_to_pdf(pdf, input_filename, col_index + 1)
                plotter3.add_plotter2(plotter2)
        return plotter3

    @classmethod
    def __add_page_to_pdf(cls, pdf, filename, column_index):
        script = Script(filename, column_index)
        script.run()
        # plotter = script.plotter1()
        plotter = script.plotter2()
        cls.__plot_and_save(pdf, plotter)
        return plotter

    @classmethod
    def __plot_and_save(cls, pdf, plotter):
        fig, plt = plotter.plot()
        plt.subplots_adjust(wspace=0.1)
        # plt.show(); exit(0)  # uncomment to generate a single graph
        pdf.savefig(fig)
        plt.close()

PDFScript()

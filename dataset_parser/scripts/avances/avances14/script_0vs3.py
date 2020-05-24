import sys
sys.path.append('.')

from matplotlib.backends.backend_pdf import PdfPages

from scripts.avances.avances14.row_plot import RowPlot
from scripts.avances.avances14.plotter import Plotter
from scripts.avances.avances15.plotter2 import Plotter2
from scripts.avances.avances16.plotter3 import Plotter3
from file_utils.csv_utils.csv_reader import CSVReader
from scripts.informe.plot.csv_constants import CSVConstants
from scripts.compress.experiments_utils import ExperimentsUtils
from scripts.informe.results_parsing.results_constants import ResultsConstants
from scripts.informe.results_parsing.results_reader import ResultsReader


class Script(object):
    def __init__(self, filename, column_index):
        self.input_file = CSVReader(ResultsConstants.COMPARE_RESULTS_PATH, "0vs3.csv")
        self.filename = filename
        self.column_index = column_index
        self.plotter = None
        self.row_plot = None
        self.__goto_file_start()

    def run(self):
        print "FILENAME = " + self.filename + " - COLUMN_INDEX = " + str(self.column_index)
        self.plotter = Plotter(self.filename, self.column_index)
        for threshold in ExperimentsUtils.THRESHOLDS:
            self.row_plot = RowPlot(threshold)

            for algorithm in ExperimentsUtils.ALGORITHMS:
                self.row_plot.begin_algorithm(algorithm)
                base_value0 = self.__find_combination(self.filename, algorithm, threshold)

                for window_size in ExperimentsUtils.WINDOWS:
                    self.__find_next_line(CSVConstants.INDEX_WINDOW, window_size, True)
                    window, value0, value3 = self.__parse_line_values()
                    self.row_plot.add_values(window, value0, value3, base_value0)

                self.row_plot.end_algorithm()
                self.__goto_file_start()
            self.plotter.add_row_plot(self.row_plot)

    def plotter1(self):
        return self.plotter

    def plotter2(self):
        return Plotter2(self.plotter)

    def __find_combination(self, filename, algorithm, threshold):
        self.__find_next_line(CSVConstants.INDEX_FILENAME, filename, False)
        base_value0_index = self.__get_value0_index()
        base_value0 = self.__get_int(self.line[base_value0_index])
        self.__find_next_line(CSVConstants.INDEX_ALGORITHM, algorithm, False)
        self.__find_next_line(CSVConstants.INDEX_THRESHOLD, threshold, True)
        return base_value0

    def __read_line(self):
        self.line = self.input_file.read_line()
        self.line_count += 1

    def __find_next_line(self, index, value, is_integer):
        if self.line_count > 0 and ResultsReader.matching_line(self.line, index, value, is_integer):
            return True

        while self.input_file.continue_reading:
            self.__read_line()
            if ResultsReader.matching_line(self.line, index, value, is_integer):
                return True
        raise Exception("ERROR: __find_next_line")

    def __parse_line_values(self):
        window = int(self.line[CSVConstants.INDEX_WINDOW])
        value0_index = self.__get_value0_index()
        value0 = self.__get_int(self.line[value0_index])
        value3 = self.__get_int(self.line[value0_index + ExperimentsUtils.MAX_COLUMN_TYPES])
        return window, value0, value3

    def __get_value0_index(self):
        return CSVConstants.INDEX_WINDOW + self.column_index

    @classmethod
    def __get_int(cls, string):
        # string = "1,285,310 - W - 1.36"
        return int(string.split()[0].replace(",", ""))

    def __goto_file_start(self):
        self.input_file.goto_row(0)
        self.line = None
        self.line_count = 0


class PDFScript(object):
    GRAPH_PATH = "scripts/avances/avances14/graphs/"

    def __init__(self):
        for dataset_id, dataset_dictionary in enumerate(ExperimentsUtils.DATASETS_ARRAY):
            self.dataset_id = dataset_id + 1
            self.dataset_name, self.cols = dataset_dictionary['name'], dataset_dictionary['cols']
            self.__create_pdfs_for_dataset()

    def __create_pdfs_for_dataset(self):
        plotter3 = self.__create_pdf1()
        # if plotter3.must_plot:
        #     self.__create_pdf2(plotter3)
        #     self.__create_pdf3(plotter3)
        #     self.__create_pdf4(plotter3)
        exit(1)

    def __create_pdf1(self):
        print "pdf1"
        with PdfPages(self.__pdf_name("")) as pdf:
            plotter3 = self.__create_pdf1_iteration(pdf)
            return plotter3

    # def __create_pdf2(self, plotter3):
    #     print "pdf2"
    #     with PdfPages(self.__pdf_name("Global-")) as pdf:
    #         for plotter in plotter3.global_plotters():
    #             self.__plot_and_save(pdf, plotter)
    #
    # def __create_pdf3(self, plotter3):
    #     print "pdf3"
    #     with PdfPages(self.__pdf_name("Globalvs0-")) as pdf:
    #         for plotter in plotter3.compare_plotters_0():
    #             self.__plot_and_save(pdf, plotter)
    #
    # def __create_pdf4(self, plotter3):
    #     print "pdf4"
    #     with PdfPages(self.__pdf_name("Globalvs3-")) as pdf:
    #         for plotter in plotter3.compare_plotters_3():
    #             self.__plot_and_save(pdf, plotter)

    def __pdf_name(self, extra_options=None):
        print extra_options
        return self.GRAPH_PATH + extra_options + str(self.dataset_id) + "-" + self.dataset_name + ".pdf"

    def __create_pdf1_iteration(self, pdf):
        plotter3 = Plotter3(self.dataset_name)
        for file_index, input_filename in enumerate(ExperimentsUtils.dataset_csv_filenames(self.dataset_name)):
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

import sys
sys.path.append('.')

from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt

from scripts.compress.experiments_utils import ExperimentsUtils
from scripts.informe.plot.plot_utils import PlotUtils
from scripts.informe.results_parsing.results_reader import ResultsReader
from scripts.informe.results_parsing.results_to_pandas import ResultsToPandas
from scripts.informe.pandas_utils.pandas_utils import PandasUtils


class PDFS1(object):
    PATH = "/Users/pablocerve/Documents/FING/Proyecto/pc-tesis/dataset_parser/scripts/informe/pdfs/pdfs1/"

    # Para cada dataset:
    #   Se crea un pdf.
    #   Para cada archivo del dataset:
    #       Para cada tipo de datos:
    #           Se agrega al pdf una pagina con las siguientes graficas:
    #               + tasa de compresion
    #               + diferencia relativa
    #               + window size
    #               + stats
    def __init__(self, datasets_names=None):
        self.dataset_names = datasets_names or ExperimentsUtils.DATASET_NAMES
        self.results_reader_0 = ResultsReader('raw', 0)
        self.results_reader_3 = ResultsReader('raw', 3)

        self.dataset_name = None
        self.filename = None
        self.pdf = None
        self.col_index = None

    def create_pdfs(self):
        for dataset_id, self.dataset_name in enumerate(self.dataset_names):
            self.create_dataset_pdf(dataset_id)

    def create_dataset_pdf(self, dataset_id):
        pdf_name = self.PATH + str(dataset_id) + "-" + self.dataset_name + ".pdf"
        with PdfPages(pdf_name) as self.pdf:
            for self.filename in ExperimentsUtils.dataset_csv_filenames(self.dataset_name):
                self.create_file_pages()

    def create_file_pages(self):
        panda_utils_0, panda_utils_3 = self.create_panda_utils()
        for self.col_index in range(ExperimentsUtils.get_dataset_data_columns_count(self.dataset_name)):
            self.create_page(panda_utils_0, panda_utils_3)

    def create_panda_utils(self):
        df_0 = ResultsToPandas(self.results_reader_0).create_dataframe(self.dataset_name, self.filename)
        df_3 = ResultsToPandas(self.results_reader_3).create_dataframe(self.dataset_name, self.filename)
        panda_utils_0 = PandasUtils(self.dataset_name, df_0, 0)
        panda_utils_3 = PandasUtils(self.dataset_name, df_3, 3)
        return panda_utils_0, panda_utils_3

    def create_page(self, panda_utils_0, panda_utils_3):
        fig, plt_ = Plotter(panda_utils_0, panda_utils_3, self.filename, self.col_index)
        plt_.subplots_adjust(wspace=0.1)
        # plt_.show(); exit(0)  # uncomment to generate a single graph
        self.pdf.savefig(fig)
        plt_.close()


class Plotter(object):
    def __init__(self, panda_utils_0, panda_utils_3, filename, col_index):
        self.panda_utils_0 = panda_utils_0
        self.panda_utils_3 = panda_utils_3
        self.filename = filename
        self.col_index = col_index
        self.fig = PlotUtils.create_figure(20, 30, self.__column_title())
        self.total_rows = 7
        self.total_columns = 3
        self.current_subplot = 0
        self.__add_plots(['compression', 'relative', 'window'], ['CoderPCA', 'CoderAPCA', 'CoderCA'])
        self.__add_plots(['compression', 'relative', 'window'], ['CoderPWLH', 'CoderPWLHInt', 'CoderGAMPSLimit'])

    def create(self):
        self.fig.set_tight_layout(True)
        self.fig.subplots_adjust(hspace=0.1)
        return self.fig, plt

    def __column_title(self):
        return self.filename + ' - col = ' + str(self.col_index)

    def __add_plots(self, plot_types_array, coders_array):
        for plot_type in plot_types_array:
            for coder_name in coders_array:
                self.add_plot(self.current_subplot, plot_type, coder_name)
                self.current_subplot += 1

    def add_plot(self, current_subplot, plot_type, coder_name):
        print str(current_subplot) + " - " + plot_type + " - " + coder_name

        if plot_type == 'compression':
            self.add_compression_plot(coder_name)
        elif plot_type == 'relative':
            pass
        else:  # plot_type == 'window'
            pass
        # ax = self.fig.add_subplot(self.total_rows, self.total_columns, current_subplot)

    def add_compression_plot(self, coder_name):
        print self.panda_utils_0.best_values_for_threshold(coder_name, self.col_index + 1)






PDFS1(['IRKIS']).create_pdfs()


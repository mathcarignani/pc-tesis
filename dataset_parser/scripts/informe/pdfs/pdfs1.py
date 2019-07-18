import sys
sys.path.append('.')

from matplotlib.backends.backend_pdf import PdfPages

from scripts.compress.experiments_utils import ExperimentsUtils
from scripts.informe.results_parsing.results_reader import ResultsReader
from scripts.informe.results_parsing.results_to_pandas import ResultsToPandas
from scripts.informe.pandas_utils.pandas_utils import PandasUtils
from scripts.informe.pdfs.plotter import Plotter


class PDFS1(object):
    PATH = "/Users/pablocerve/Documents/FING/Proyecto/pc-tesis/dataset_parser/scripts/informe/pdfs/pdfs1/"

    # For each dataset:
    #   Create a pdf.
    #   For each file in the dataset:
    #       For each data type:
    #           Add a pdf page with the following graphs:
    #               + compression rate
    #               + relative difference
    #               + window size
    #               + stats
    def __init__(self, datasets_names=None):
        self.dataset_names = datasets_names or ExperimentsUtils.DATASET_NAMES
        self.results_reader_0 = ResultsReader('raw', 0)
        self.results_reader_3 = ResultsReader('raw_basic', 3)
        self.dataset_id = None
        self.dataset_name = None
        self.filename = None
        self.pdf = None
        self.col_index = None

    def create_pdfs(self):
        for dataset_id, self.dataset_name in enumerate(self.dataset_names):
            print self.dataset_name
            self.dataset_id = dataset_id + 1
            self.created_pdfs_for_dataset()

    def created_pdfs_for_dataset(self):
        pdf_name = self.PATH + str(self.dataset_id) + "-" + self.dataset_name + ".pdf"
        with PdfPages(pdf_name) as pdf:
            for self.filename in ExperimentsUtils.dataset_csv_filenames(self.dataset_name):
                print self.filename
                self.create_file_pages(pdf)

    def create_file_pages(self, pdf):
        panda_utils_0, panda_utils_3 = self.create_panda_utils()
        for col_index in range(ExperimentsUtils.get_dataset_data_columns_count(self.dataset_name)):
            self.col_index = col_index + 1
            self.create_page(pdf, panda_utils_0, panda_utils_3)
            return

    def create_panda_utils(self):
        df_0 = ResultsToPandas(self.results_reader_0).create_dataframe(self.dataset_name, self.filename)
        df_3 = ResultsToPandas(self.results_reader_3).create_dataframe(self.dataset_name, self.filename)
        panda_utils_0 = PandasUtils(self.dataset_name, df_0, 0)
        panda_utils_3 = PandasUtils(self.dataset_name, df_3, 3)
        return panda_utils_0, panda_utils_3

    def create_page(self, pdf, panda_utils_0, panda_utils_3):
        plotter = Plotter(panda_utils_0, panda_utils_3, self.filename, self.col_index)
        fig, plt = plotter.create()
        plt.subplots_adjust(wspace=0.1)
        # plt_.show(); exit(0)  # uncomment to generate a single graph
        pdf.savefig(fig)
        plt.close()

PDFS1(['NOAA-SPC-wind']).create_pdfs()
# PDFS1(None).create_pdfs()

import sys
sys.path.append('.')

from matplotlib.backends.backend_pdf import PdfPages

from scripts.compress.experiments_utils import ExperimentsUtils
from scripts.informe.results_parsing.results_reader import ResultsReader
from scripts.informe.results_parsing.results_to_dataframe import ResultsToDataframe
from scripts.informe.pandas_utils.pandas_utils import PandasUtils
from scripts.informe.pdfs.pdf_page import PdfPage


class PDFS1(object):
    PATH = "/Users/pablocerve/Documents/FING/Proyecto/pc-tesis/dataset_parser/scripts/informe/pdfs/pdfs1/"
    FIGSIZE_H = 10
    FIGSIZE_V = 25
    WSPACE = 0.1
    CODERS_ARRAY = ['CoderPCA', 'CoderAPCA', 'CoderCA', 'CoderPWLH', 'CoderPWLHInt', 'CoderGAMPSLimit']
    PLOTS_ARRAY = ['compression', 'relative', 'window', 'relative_stats', 'window_stats']
    PLOTS_MATRIX = [
        [['CoderPCA', 'compression'],  ['CoderAPCA', 'compression'],    ['CoderCA', 'compression']],
        [['CoderPCA', 'relative'],     ['CoderAPCA', 'relative'],       ['CoderCA', 'relative']],
        [['CoderPCA', 'window'],       ['CoderAPCA', 'window'],         ['CoderCA', 'window']],

        [['CoderPWLH', 'compression'], ['CoderPWLHInt', 'compression'], ['CoderGAMPSLimit', 'compression']],
        [['CoderPWLH', 'relative'],    ['CoderPWLHInt', 'relative'],    ['CoderGAMPSLimit', 'relative']],
        [['CoderPWLH', 'window'],      ['CoderPWLHInt', 'window'],      ['CoderGAMPSLimit', 'window']],

        [[None, 'relative_stats'],     [None, 'window_stats']]
    ]

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
        self.df_0 = ResultsToDataframe(ResultsReader('raw', 0)).create_full_df()
        self.df_3 = ResultsToDataframe(ResultsReader('raw_basic', 3)).create_full_df()

        # iteration variables
        self.dataset_id = None
        self.dataset_name = None
        self.filename = None
        self.pdf = None
        self.col_index = None

    def create_pdfs(self):
        for dataset_id, self.dataset_name in enumerate(self.dataset_names):
            print self.dataset_name
            self.dataset_id = dataset_id + 1
            self.created_pdf_for_dataset()

    def created_pdf_for_dataset(self):
        pdf_name = self.PATH + str(self.dataset_id) + "-" + self.dataset_name + ".pdf"
        with PdfPages(pdf_name) as self.pdf:
            dataset_filenames = ExperimentsUtils.dataset_csv_filenames(self.dataset_name)
            for self.filename in dataset_filenames:
                print self.filename
                self.create_pdf_pages()

    def create_pdf_pages(self):
        # create panda_utils
        panda_utils_0 = PandasUtils(self.dataset_name, self.filename, self.df_0, 0)
        panda_utils_3 = PandasUtils(self.dataset_name, self.filename, self.df_3, 3)

        for self.col_index in range(1, ExperimentsUtils.get_dataset_data_columns_count(self.dataset_name) + 1):
            self.create_pdf_page(panda_utils_0, panda_utils_3)
            return

    def create_pdf_page(self, panda_utils_0, panda_utils_3):
        pdf_page = PdfPage(panda_utils_0, panda_utils_3, self.filename, self.col_index, self.FIGSIZE_H, self.FIGSIZE_V)
        fig, plt = pdf_page.create(self.CODERS_ARRAY, self.PLOTS_ARRAY, self.PLOTS_MATRIX)
        plt.subplots_adjust(wspace=PDFS1.WSPACE)
        # plt.show(); exit(0) # uncomment to show first page
        self.pdf.savefig(fig)
        plt.close()

# PDFS1(['NOAA-SPC-wind']).create_pdfs()
# PDFS1(['IRKIS']).create_pdfs()
PDFS1(None).create_pdfs()

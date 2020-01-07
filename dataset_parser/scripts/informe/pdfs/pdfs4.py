import sys
sys.path.append('.')

from matplotlib.backends.backend_pdf import PdfPages

from scripts.compress.experiments_utils import ExperimentsUtils
from scripts.informe.results_parsing.results_reader import ResultsReader
from scripts.informe.results_parsing.results_to_dataframe import ResultsToDataframe
from scripts.informe.pandas_utils.pandas_methods import PandasMethods
from scripts.informe.pandas_utils.pandas_utils import PandasUtils
from scripts.informe.pdfs.pdf_page import PdfPage


class PDFS4(object):
    PATH = "/Users/pablocerve/Documents/FING/Proyecto/pc-tesis/dataset_parser/scripts/informe/pdfs/pdfs2/"
    FIGSIZE_H = 15
    FIGSIZE_V = 20
    WSPACE = 0.1
    CODERS_ARRAY = ['CoderPCA', 'CoderAPCA', 'CoderCA', 'CoderPWLH', 'CoderPWLHInt', 'CoderGAMPSLimit', 'CoderFR', 'CoderSF']
    PLOTS_ARRAY = ['compression', 'window']
    PLOTS_MATRIX = [
        [['CoderPCA', 'compression'],     ['CoderAPCA', 'compression'],       ['CoderCA', 'compression'], ['CoderPWLH', 'compression']],
        [['CoderPCA', 'window'],          ['CoderAPCA', 'window'],            ['CoderCA', 'window'],      ['CoderPWLH', 'window']],

        [['CoderPWLHInt', 'compression'], ['CoderGAMPSLimit', 'compression'], ['CoderFR', 'compression'], ['CoderSF', 'compression']],
        [['CoderPWLHInt', 'window'],      ['CoderGAMPSLimit', 'window'],      ['CoderFR', 'window']]
    ]

    def __init__(self, datasets_names=None):
        df_0 = ResultsToDataframe(ResultsReader('global', 0)).create_full_df()
        self.df_3 = ResultsToDataframe(ResultsReader('global', 3)).create_full_df()
        self.df_3 = PandasMethods.set_coder_basic(df_0, self.df_3)
        self.path = PDFS4.PATH
        self.dataset_names = datasets_names or ExperimentsUtils.DATASET_NAMES

        # iteration variables
        self.dataset_id = None
        self.dataset_name = None
        self.filename = None
        self.pdf = None
        self.col_index = None

    def create_pdfs(self):
        for dataset_id, self.dataset_name in enumerate(self.dataset_names):
            print(self.dataset_name)
            self.dataset_id = dataset_id + 1
            self.created_pdf_for_dataset()

    def created_pdf_for_dataset(self):
        pdf_name = self.path + str(self.dataset_id) + "-" + self.dataset_name + ".pdf"
        with PdfPages(pdf_name) as self.pdf:
            dataset_filenames = ExperimentsUtils.dataset_csv_filenames(self.dataset_name)
            if len(dataset_filenames) > 1:
                dataset_filenames = ['Global']

            for self.filename in dataset_filenames:
                print(self.filename)
                self.create_pdf_pages()

    def create_pdf_pages(self):
        # create panda_utils
        panda_utils_3 = PandasUtils(self.dataset_name, self.filename, self.df_3, 3)

        for self.col_index in range(1, ExperimentsUtils.get_dataset_data_columns_count(self.dataset_name) + 1):
            self.create_pdf_page(panda_utils_3)

    def create_pdf_page(self, panda_utils_3):
        pdf_page = PdfPage(None, panda_utils_3, self.filename, self.col_index, self.FIGSIZE_H, self.FIGSIZE_V)
        fig, plt = pdf_page.create(self.CODERS_ARRAY, self.PLOTS_ARRAY, self.PLOTS_MATRIX)
        plt.subplots_adjust(wspace=PDFS4.WSPACE)
        # plt.show(); exit(0) # uncomment to show first page
        self.pdf.savefig(fig)
        plt.close()

# PDFS2().create_pdfs()
# PDFS2(['NOAA-SPC-wind']).create_pdfs()

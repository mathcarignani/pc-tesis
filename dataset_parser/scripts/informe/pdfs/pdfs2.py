import sys
sys.path.append('.')

from matplotlib.backends.backend_pdf import PdfPages

from scripts.compress.experiments_utils import ExperimentsUtils
from scripts.informe.results_parsing.results_reader import ResultsReader
from scripts.informe.results_parsing.results_to_dataframe import ResultsToDataframe
from scripts.informe.pandas_utils.pandas_utils import PandasUtils
from scripts.informe.pdfs.pdf_page import PdfPage
from scripts.informe.pdfs.pdfs_common import PDFSCommon


class PDFS2(PDFSCommon):
    FIGSIZE_H = 10
    FIGSIZE_V = 15  # 25
    WSPACE = 0.1  # horizontal spacing between subplots
    HSPACE = 0.3  # vertical spacing between subplots
    CODERS_ARRAY = ['CoderPCA', 'CoderAPCA', 'CoderCA', 'CoderPWLH', 'CoderPWLHInt', 'CoderGAMPSLimit']
    PLOTS_ARRAY = ['compression', 'window', 'window_stats']
    PLOTS_MATRIX = [
        [['CoderPCA', 'compression'],  ['CoderAPCA', 'compression'],    ['CoderCA', 'compression']],
        [['CoderPCA', 'window'],       ['CoderAPCA', 'window'],         ['CoderCA', 'window']],
        [['CoderPWLH', 'compression'], ['CoderPWLHInt', 'compression'], ['CoderGAMPSLimit', 'compression']],
        [['CoderPWLH', 'window'],      ['CoderPWLHInt', 'window'],      ['CoderGAMPSLimit', 'window']],
        [[None, 'window_stats']]
    ]
    PLOT_OPTIONS = {
        'compression': {'title': True, 'labels': [r'$a_{NM}$', r'$a_M$']},
        'window': {'show_xlabel': True, 'labels': [r'$global$', r'$local$']},
    }

    def __init__(self, path, global_mode=True, datasets_names=None):
        if global_mode:
            self.df_3 = ResultsToDataframe(ResultsReader('global', 3)).create_full_df()
            path += 'global/'
        else:
            self.df_3 = ResultsToDataframe(ResultsReader('raw', 3)).create_full_df()
            path += 'local/'

        # self.df_3 = PandasMethods.set_coder_basic(self.df_0, self.df_3)

        self.col_index = None  # iteration variable
        super(PDFS2, self).__init__(path, global_mode, datasets_names)

    def create_pdf_pages(self, pdf, dataset_name, filename):
        # create panda_utils
        panda_utils_3 = PandasUtils(dataset_name, filename, self.df_3, 3)

        for self.col_index in range(1, ExperimentsUtils.get_dataset_data_columns_count(dataset_name) + 1):
            self.create_pdf_page(pdf, filename, panda_utils_3)

    def create_pdf_page(self, pdf, filename, panda_utils_3):
        pdf_page = PdfPage(None, panda_utils_3, filename, self.col_index, self.FIGSIZE_H, self.FIGSIZE_V, self.PLOT_OPTIONS)
        fig, plt = pdf_page.create(self.CODERS_ARRAY, self.PLOTS_ARRAY, self.PLOTS_MATRIX)
        plt.subplots_adjust(wspace=PDFS2.WSPACE, hspace=PDFS2.HSPACE)
        # plt.show(); exit(0) # uncomment to show first page
        pdf.savefig(fig)
        plt.close()

# PDFS2(False).create_pdfs()
# PDFS2(True).create_pdfs()
# PDFS2(True, ['NOAA-SPC-wind']).create_pdfs()

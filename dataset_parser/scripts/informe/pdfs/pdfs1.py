import sys
sys.path.append('.')

from scripts.compress.experiments_utils import ExperimentsUtils
from scripts.informe.results_parsing.results_reader import ResultsReader
from scripts.informe.results_parsing.results_to_dataframe import ResultsToDataframe
from scripts.informe.pandas_utils.pandas_methods import PandasMethods
from scripts.informe.pandas_utils.pandas_utils import PandasUtils
from scripts.informe.pdfs.pdf_page import PdfPage
from scripts.informe.pdfs.pdfs_common import PDFSCommon

# PLOTS_MATRIX = [
#     [['CoderPCA', 'compression'],  ['CoderAPCA', 'compression'],    ['CoderCA', 'compression']],
#     [['CoderPCA', 'relative'],     ['CoderAPCA', 'relative'],       ['CoderCA', 'relative']],
#     # [['CoderPCA', 'window'],       ['CoderAPCA', 'window'],         ['CoderCA', 'window']],
#
#     [['CoderPWLH', 'compression'], ['CoderPWLHInt', 'compression'], ['CoderGAMPSLimit', 'compression']],
#     [['CoderPWLH', 'relative'],    ['CoderPWLHInt', 'relative'],    ['CoderGAMPSLimit', 'relative']],
#     # [['CoderPWLH', 'window'],      ['CoderPWLHInt', 'window'],      ['CoderGAMPSLimit', 'window']],
#
#     # [[None, 'relative_stats'],     [None, 'window_stats']]
# ]


class PDFS1(PDFSCommon):
    FIGSIZE_H = 10
    FIGSIZE_V = 15  # 25
    WSPACE = 0.1  # horizontal spacing between subplots
    HSPACE = 0.3  # vertical spacing between subplots
    CODERS_ARRAY = ['CoderPCA', 'CoderAPCA', 'CoderCA', 'CoderPWLH', 'CoderPWLHInt', 'CoderGAMPSLimit']
    PLOTS_ARRAY = ['compression', 'relative']  # , 'window', 'relative_stats']  # , 'window_stats']
    PLOTS_MATRIX = [
        [['CoderPCA', 'compression'],  ['CoderAPCA', 'compression'],    ['CoderCA', 'compression']],
        [['CoderPCA', 'relative'],     ['CoderAPCA', 'relative'],       ['CoderCA', 'relative']],

        [['CoderPWLH', 'compression'], ['CoderPWLHInt', 'compression'], ['CoderGAMPSLimit', 'compression']],
        [['CoderPWLH', 'relative'],    ['CoderPWLHInt', 'relative'],    ['CoderGAMPSLimit', 'relative']]
    ]
    PLOT_OPTIONS = {
        'compression': {'title': True, 'labels': [r'$a_{NM}$', r'$a_M$']},
        'relative': {'add_min_max_circles': True, 'show_xlabel': True}
    }

    def __init__(self, path, global_mode=True, datasets_names=None):
        if global_mode:
            self.df_0 = ResultsToDataframe(ResultsReader('global', 0)).create_full_df()
            self.df_3 = ResultsToDataframe(ResultsReader('global', 3)).create_full_df()
            path += 'global/'
        else:
            self.df_0 = ResultsToDataframe(ResultsReader('raw', 0)).create_full_df()
            self.df_3 = ResultsToDataframe(ResultsReader('raw', 3)).create_full_df()
            path += 'local/'

        # Move this to a new class
        self.df_3 = PandasMethods.set_coder_basic(self.df_0, self.df_3)
        PandasMethods.check_coder_basic_matches(self.df_0, self.df_3)

        self.col_index = None  # iteration variable
        super(PDFS1, self).__init__(path, global_mode, datasets_names)

    def create_pdf_pages(self, pdf, dataset_name, filename):
        # create panda_utils
        panda_utils_0 = PandasUtils(dataset_name, filename, self.df_0, 0)
        panda_utils_3 = PandasUtils(dataset_name, filename, self.df_3, 3)

        for self.col_index in range(1, ExperimentsUtils.get_dataset_data_columns_count(dataset_name) + 1):
            self.create_pdf_page(pdf, filename, panda_utils_0, panda_utils_3)

    def create_pdf_page(self, pdf, filename, panda_utils_0, panda_utils_3):
        pdf_page = PdfPage(panda_utils_0, panda_utils_3, filename, self.col_index, self.FIGSIZE_H, self.FIGSIZE_V, self.PLOT_OPTIONS)
        fig, plt = pdf_page.create(self.CODERS_ARRAY, self.PLOTS_ARRAY, self.PLOTS_MATRIX)
        plt.subplots_adjust(wspace=PDFS1.WSPACE, hspace=PDFS1.HSPACE)
        # plt.show(); exit(0) # uncomment to show first page
        pdf.savefig(fig)
        plt.close()

# PDFS1(False).create_pdfs()
# PDFS1(True).create_pdfs()
# PDFS1(True, ['NOAA-SPC-wind']).create_pdfs()

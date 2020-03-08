import sys
sys.path.append('.')

from matplotlib.backends.backend_pdf import PdfPages

from scripts.compress.experiments_utils import ExperimentsUtils
from scripts.informe.results_parsing.results_reader import ResultsReader
from scripts.informe.results_parsing.results_to_dataframe import ResultsToDataframe
from scripts.informe.pandas_utils.pandas_methods import PandasMethods
from scripts.informe.pandas_utils.pandas_utils import PandasUtils
from scripts.informe.pdfs.pdf_page import PdfPage
from scripts.informe.pdfs.pdfs_common import PDFSCommon


class PDFS4(PDFSCommon):
    SUBPLOT_SPACING_W_H = (0.1, 0.05)
    FIG_SIZE_H_V = (10, 11)
    CODERS_ARRAY = ['CoderPCA', 'CoderAPCA', 'CoderCA', 'CoderPWLH', 'CoderPWLHInt', 'CoderGAMPSLimit',
                    'CoderFR', 'CoderSF']
    PLOTS_ARRAY = ['window', 'compression']
    PLOTS_MATRIX = [
        [['CoderPCA', 'window'],       ['CoderAPCA', 'window'],         ['CoderCA', 'window'],               ['CoderFR', 'window']],
        None,
        [['CoderPCA', 'compression'],  ['CoderAPCA', 'compression'],    ['CoderCA', 'compression'],          ['CoderFR', 'compression']],
        None,
        [['CoderPWLH', 'window'],      ['CoderPWLHInt', 'window'],      ['CoderGAMPSLimit', 'window'],       ['CoderSF', 'window']],
        None,
        [['CoderPWLH', 'compression'], ['CoderPWLHInt', 'compression'], ['CoderGAMPSLimit', 'compression'],  ['CoderSF', 'compression']]
    ]
    HEIGHT_RATIOS = [30, 0, 30, 15, 30, 0, 30]
    PLOT_OPTIONS = {
        'window': {'title': 12, 'labels': [r'$global$', r'$local$']},
        'compression': {'show_xlabel': True} # {'labels': [r'$global$', r'$local$']},
        # 'relative': {'check_never_negative': True, 'show_xlabel': True, 'add_max_circle': True}
    }

    def __init__(self, path, global_mode=True, datasets_names=None):
        assert(len(self.HEIGHT_RATIOS) == len(self.PLOTS_MATRIX))
        self.global_mode = global_mode

        df_0 = ResultsToDataframe(ResultsReader('global', 0)).create_full_df()
        self.df_3 = ResultsToDataframe(ResultsReader('global', 3)).create_full_df()
        self.df_3 = PandasMethods.set_coder_basic(df_0, self.df_3)

        # iteration variables
        self.col_index = None  # iteration variable
        super(PDFS4, self).__init__(path, global_mode, datasets_names)

    def create_pdf_pages(self, pdf, dataset_name, filename):
        # create panda_utils
        panda_utils_3 = PandasUtils(self.dataset_name, self.filename, self.df_3, 3)

        for self.col_index in self.column_indexes(dataset_name):
            self.create_pdf_page(pdf, filename, panda_utils_3)

    def create_pdf_page(self, pdf, filename, panda_utils_3):
        pdf_page = PdfPage(None, panda_utils_3, filename, self)

        # IMPORTANT: resize before setting the labels to avoid this issue: https://stackoverflow.com/q/50395392/4547232
        pdf_page.plt.subplots_adjust(wspace=PDFS4.SUBPLOT_SPACING_W_H[0], hspace=PDFS4.SUBPLOT_SPACING_W_H[1])

        fig, plt = pdf_page.create(self.CODERS_ARRAY, self.PLOTS_ARRAY, self.PLOTS_MATRIX)
        pdf.savefig(fig)
        if self.global_mode:
            plt.savefig(self.pdf_name.replace(".pdf", "-") + str(self.col_index) + ".png")
        plt.close()

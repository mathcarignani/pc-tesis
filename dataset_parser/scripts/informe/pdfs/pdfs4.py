import sys
sys.path.append('.')

from scripts.informe.results_parsing.results_reader import ResultsReader
from scripts.informe.results_parsing.results_to_dataframe import ResultsToDataframe
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
        [['CoderPCA', 'compression'],  ['CoderAPCA', 'compression'],    ['CoderCA', 'compression'],          ['CoderFR', 'compression']],
        None,
        [['CoderPCA', 'window'],       ['CoderAPCA', 'window'],         ['CoderCA', 'window'],               ['CoderFR', 'window']],
        None,
        [['CoderPWLH', 'compression'], ['CoderPWLHInt', 'compression'], ['CoderGAMPSLimit', 'compression'],  ['CoderSF', 'compression']],
        None,
        [['CoderPWLH', 'window'],      ['CoderPWLHInt', 'window'],      ['CoderGAMPSLimit', 'window'],       ['CoderSF', 'window']]
    ]
    HEIGHT_RATIOS = [30, 0, 30, 15, 30, 0, 30]
    PLOT_OPTIONS = {
        'compression': {'title': 12, 'add_data': True},
        'window': {'show_xlabel': True, 'add_data': True}
    }

    def __init__(self, path, mode='global', datasets_names=None):
        assert(len(self.HEIGHT_RATIOS) == len(self.PLOTS_MATRIX))
        PDFSCommon.check_valid_mode(mode)

        self.df_M = ResultsToDataframe(ResultsReader('global', "M")).create_full_df()

        # iteration variables
        self.col_index = None  # iteration variable
        super(PDFS4, self).__init__(path, mode, datasets_names)

    def create_pdf_pages(self, pdf, dataset_name, filename):
        # create panda_utils
        panda_utils_M = PandasUtils(self.dataset_name, self.filename, self.df_M, "M")

        for self.col_index in self.column_indexes(dataset_name):
            self.create_pdf_page(pdf, filename, panda_utils_M)

    def create_pdf_page(self, pdf, filename, panda_utils_M):
        pdf_page = PdfPage(None, panda_utils_M, filename, self)

        # IMPORTANT: resize before setting the labels to avoid this issue: https://stackoverflow.com/q/50395392/4547232
        pdf_page.plt.subplots_adjust(wspace=PDFS4.SUBPLOT_SPACING_W_H[0], hspace=PDFS4.SUBPLOT_SPACING_W_H[1])

        fig, plt = pdf_page.create(self.CODERS_ARRAY, self.PLOTS_ARRAY, self.PLOTS_MATRIX)
        pdf.savefig(fig)
        if self.mode == 'global':
            plt.savefig(self.create_image_name(self.pdf_name, self.col_index), format='pdf')
        plt.close()

    ####################################################################################################################
    ####################################################################################################################
    ####################################################################################################################

    def add_data(self, plot_name, algorithm, values):
        if not self.PLOT_OPTIONS[plot_name].get('add_data'):
            return {}

        if not(self.dataset_name == "ElNino" and self.col_index == 7):
            return {}

        if algorithm == "CoderPCA":
            return {'keys': ["PlotMax"], 'indexes': [0]}
        elif algorithm == "CoderAPCA":
            size = len(values)
            array = list(range(1, size)) # [1, 2, ..., size-1]
            result = {'keys': ["PlotMax"]*(size-1), 'indexes': array}
            return result
        else:
            return {}

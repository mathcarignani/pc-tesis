import sys
sys.path.append('.')

from scripts.informe.results_parsing.results_reader import ResultsReader
from scripts.informe.results_parsing.results_to_dataframe import ResultsToDataframe
from scripts.informe.pandas_utils.pandas_methods import PandasMethods
from scripts.informe.pandas_utils.pandas_utils import PandasUtils
from scripts.informe.pdfs.pdf_page import PdfPage
from scripts.informe.pdfs.pdfs_common import PDFSCommon
from scripts.informe.plot.plot_constants import PlotConstants


class PDFS2(PDFSCommon):
    SUBPLOT_SPACING_W_H = (0.1, 0.05)
    FIG_SIZE_H_V = (10, 14)
    CODERS_ARRAY = ['CoderPCA', 'CoderAPCA', 'CoderCA', 'CoderPWLH', 'CoderPWLHInt', 'CoderGAMPSLimit',
                    'CoderFR', 'CoderSF']
    PLOTS_ARRAY = ['compression', 'window', 'window_stats']
    PLOTS_MATRIX = [
        [['CoderPCA', 'compression'],  ['CoderAPCA', 'compression'],    ['CoderCA', 'compression'],         ['CoderFR', 'compression']],
        None,
        [['CoderPCA', 'window'],       ['CoderAPCA', 'window'],         ['CoderCA', 'window'],              ['CoderFR', 'window']],
        None,
        [['CoderPWLH', 'compression'], ['CoderPWLHInt', 'compression'], ['CoderGAMPSLimit', 'compression'], ['CoderSF', 'compression']],
        None,
        [['CoderPWLH', 'window'],      ['CoderPWLHInt', 'window'],      ['CoderGAMPSLimit', 'window'],      ['CoderSF', 'window']],
        None,
        [[None, 'window_stats']]
    ]
    HEIGHT_RATIOS = [30, 0, 30, 15, 30, 0, 30, 10, 20]
    PLOT_OPTIONS = {
        'compression': {'title': True, 'labels': [r'$a_{NM}$', r'$a_M$']},
        'window': {'show_xlabel': True},
    }

    def __init__(self, path, mode='global', datasets_names=None):
        assert(len(self.HEIGHT_RATIOS) == len(self.PLOTS_MATRIX))
        PDFSCommon.check_valid_mode(mode)

        self.df_0 = ResultsToDataframe(ResultsReader(mode, 0)).create_full_df()
        self.df_3 = ResultsToDataframe(ResultsReader(mode, 3)).create_full_df()

        self.col_index = None  # iteration variable
        super(PDFS2, self).__init__(path + mode + "/", mode, datasets_names)

    def plot_options(self):
        options = self.PLOT_OPTIONS
        color = PlotConstants.COLOR_LIGHT_BLUE if self.mode == 'global' else PlotConstants.COLOR_RED
        options['window']['color'] = color
        options['compression']['color'] = color
        return options

    def create_pdf_pages(self, pdf, dataset_name, filename):
        panda_utils_3 = PandasUtils(dataset_name, filename, self.df_3, 3)

        for self.col_index in self.column_indexes(dataset_name):
            self.create_pdf_page(pdf, filename, panda_utils_3)

    def create_pdf_page(self, pdf, filename, panda_utils_3):
        pdf_page = PdfPage(None, panda_utils_3, filename, self)

        # IMPORTANT: resize before setting the labels to avoid this issue: https://stackoverflow.com/q/50395392/4547232
        pdf_page.plt.subplots_adjust(wspace=PDFS2.SUBPLOT_SPACING_W_H[0], hspace=PDFS2.SUBPLOT_SPACING_W_H[1])

        fig, plt = pdf_page.create(self.CODERS_ARRAY, self.PLOTS_ARRAY, self.PLOTS_MATRIX)
        pdf.savefig(fig)
        if self.mode == 'global':
            plt.savefig(self.pdf_name.replace(".pdf", "-") + str(self.col_index) + ".png")
        plt.close()

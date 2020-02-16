import sys
sys.path.append('.')

from matplotlib.backends.backend_pdf import PdfPages

from scripts.compress.experiments_utils import ExperimentsUtils
from scripts.informe.results_parsing.results_reader import ResultsReader
from scripts.informe.results_parsing.results_to_dataframe import ResultsToDataframe
from scripts.informe.pandas_utils.pandas_utils import PandasUtils
from scripts.informe.pandas_utils.pandas_methods import PandasMethods
from scripts.informe.pdfs.pdf_page import PdfPage
from scripts.informe.pdfs.pdfs_common import PDFSCommon


class PDFS3(PDFSCommon):
    SUBPLOT_SPACING_W_H = (0.1, 0.05)
    FIG_SIZE_H_V = (10, 14)
    CODERS_ARRAY = ['CoderPCA', 'CoderAPCA', 'CoderCA', 'CoderPWLH', 'CoderPWLHInt', 'CoderGAMPSLimit',
                    'CoderFR', 'CoderSF']
    PLOTS_ARRAY = ['compression', 'relative', 'window', 'relative_stats', 'window_stats']
    PLOTS_MATRIX = [
        [['CoderPCA', 'window'],       ['CoderAPCA', 'window'],         ['CoderCA', 'window'],              ['CoderFR', 'window']],
        None,
        [['CoderPCA', 'compression'],  ['CoderAPCA', 'compression'],    ['CoderCA', 'compression'],         ['CoderFR', 'compression']],
        None,
        [['CoderPCA', 'relative'],     ['CoderAPCA', 'relative'],       ['CoderCA', 'relative'],            ['CoderFR', 'relative']],
        None,
        [['CoderPWLH', 'window'],      ['CoderPWLHInt', 'window'],      ['CoderGAMPSLimit', 'window'],      ['CoderSF', 'window']],
        None,
        [['CoderPWLH', 'compression'], ['CoderPWLHInt', 'compression'], ['CoderGAMPSLimit', 'compression'], ['CoderSF', 'compression']],
        None,
        [['CoderPWLH', 'relative'],    ['CoderPWLHInt', 'relative'],    ['CoderGAMPSLimit', 'relative'],    ['CoderSF', 'relative']],
        None,
        [[None, 'window_stats'], [None, 'relative_stats']]
    ]
    HEIGHT_RATIOS = [30, 0, 30, 0, 30, 20, 30, 0, 30, 0, 30, 20, 5]
    PLOT_OPTIONS = {
        'window': {'title': True, 'labels': [r'$global$', r'$local$']},
        'compression': {'labels': [r'$global$', r'$local$']},
        'relative': {'check_never_negative': True, 'show_xlabel': True},
        'relative_stats': {},
        'window_stats': {}
    }

    def __init__(self, path, datasets_names=None):
        self.df_3_local = ResultsToDataframe(ResultsReader('raw', 3)).create_full_df()
        self.df_3_global = ResultsToDataframe(ResultsReader('global', 3)).create_full_df()
        self.path = path

        self.dataset_names = datasets_names or ExperimentsUtils.datasets_with_multiple_files()
        self.global_mode = False

        # iteration variables
        self.dataset_id = None
        self.dataset_name = None
        self.filename = None
        self.pdf_name = None
        self.col_index = None
        self.pd_utils_3_global = None

    def create_pdfs(self):
        for dataset_id, self.dataset_name in enumerate(self.dataset_names):
            # print self.dataset_name
            self.dataset_id = dataset_id + 1
            self.created_dataset_pdf_file()

    def created_dataset_pdf_file(self):
        self.pdf_name = self.path + str(self.dataset_id) + "-" + self.dataset_name + ".pdf"
        with PdfPages(self.pdf_name) as pdf:
            self.pd_utils_3_global = PandasUtils(self.dataset_name, 'Global', self.df_3_global, 3)
            for self.filename in self.dataset_filenames():
                # print("  " + self.filename)
                self.create_pdf_pages(pdf, self.dataset_name, self.filename)

    def create_pdf_pages(self, pdf, dataset_name, filename):
        for self.col_index in self.column_indexes(dataset_name):
            # create panda_utils. Must do it inside this block to prevent issue with many datatypes in a single dataset
            df_3_local_copy_1 = PandasMethods.copy(self.df_3_local)
            df_3_local_copy_2 = PandasMethods.copy(self.df_3_local)
            pd_utils_3_local_1 = PandasUtils(dataset_name, filename, df_3_local_copy_1, 3)  # local with best LOCAL window
            pd_utils_3_local_2 = PandasUtils(dataset_name, filename, df_3_local_copy_2, 3)  # local with best GLOBAL window

            mod_pd_utils_3_local_2 = self.set_global_window(pd_utils_3_local_2)
            # TODO: change order to make Relative Difference <= 0
            self.create_pdf_page(pdf, filename, mod_pd_utils_3_local_2, pd_utils_3_local_1)
            # exit(1)

    #
    # In the local results, consider the best global window instead of the best local window
    #
    def set_global_window(self, pd_utils_3_local_2):
        new_df = pd_utils_3_local_2.df

        for coder_name in self.CODERS_ARRAY:
            # print "  " + coder_name
            for threshold in ExperimentsUtils.THRESHOLDS:
                # print threshold
                best_global_window = self.pd_utils_3_global.min_value_for_threshold(coder_name, self.col_index, threshold)['window']
                best_local_window = pd_utils_3_local_2.min_value_for_threshold(coder_name, self.col_index, threshold)['window']
                if best_global_window != best_local_window:
                    # print str(threshold) + " - GLOBAL = " + str(best_global_window) + " - LOCAL = " + str(best_local_window)
                    # remove every threshold value other than the one that uses the best global window
                    index_names = new_df[(new_df['coder'] == coder_name) & (new_df['threshold'] == threshold) & (new_df['window'] != best_global_window)].index
                    new_df.drop(index_names, inplace=True)
        mod_pd_utils_3_local_2 = PandasUtils(self.dataset_name, self.filename, new_df, 3, False)
        return mod_pd_utils_3_local_2

    def create_pdf_page(self, pdf, filename, pd_utils_3_local_1, pd_utils_3_local_2):
        pdf_page = PdfPage(pd_utils_3_local_1, pd_utils_3_local_2, filename, self)

        # IMPORTANT: resize before setting the labels to avoid this issue: https://stackoverflow.com/q/50395392/4547232
        pdf_page.plt.subplots_adjust(wspace=PDFS3.SUBPLOT_SPACING_W_H[0], hspace=PDFS3.SUBPLOT_SPACING_W_H[1])

        fig, plt = pdf_page.create(self.CODERS_ARRAY, self.PLOTS_ARRAY, self.PLOTS_MATRIX)
        pdf.savefig(fig)
        plt.close()

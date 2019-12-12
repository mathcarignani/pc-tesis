import sys
sys.path.append('.')

from matplotlib.backends.backend_pdf import PdfPages

from scripts.compress.experiments_utils import ExperimentsUtils
from scripts.informe.results_parsing.results_reader import ResultsReader
from scripts.informe.results_parsing.results_to_dataframe import ResultsToDataframe
from scripts.informe.pandas_utils.pandas_methods import PandasMethods
from scripts.informe.pandas_utils.pandas_utils import PandasUtils
from scripts.informe.pdfs.pdf_page import PdfPage


class PDFS3(object):
    FIGSIZE_H = 10
    FIGSIZE_V = 15  # 25
    WSPACE = 0.1  # horizontal spacing between subplots
    HSPACE = 0.3  # vertical spacing between subplots
    CODERS_ARRAY = ['CoderPCA', 'CoderAPCA', 'CoderCA', 'CoderPWLH', 'CoderPWLHInt', 'CoderGAMPSLimit']
    PLOTS_ARRAY = ['compression', 'relative', 'window', 'relative_stats', 'window_stats']
    PLOTS_MATRIX = [
        [['CoderPCA', 'window'],       ['CoderAPCA', 'window'],         ['CoderCA', 'window']],
        [['CoderPCA', 'compression'],  ['CoderAPCA', 'compression'],    ['CoderCA', 'compression']],
        [['CoderPCA', 'relative'],     ['CoderAPCA', 'relative'],       ['CoderCA', 'relative']],

        [['CoderPWLH', 'window'],      ['CoderPWLHInt', 'window'],      ['CoderGAMPSLimit', 'window']],
        [['CoderPWLH', 'compression'], ['CoderPWLHInt', 'compression'], ['CoderGAMPSLimit', 'compression']],
        [['CoderPWLH', 'relative'],    ['CoderPWLHInt', 'relative'],    ['CoderGAMPSLimit', 'relative']],

        # [[None, 'relative_stats'],     [None, 'window_stats']]  # TODO: comment after debugging
    ]
    PLOT_OPTIONS = {
        'window': {'title': True, 'labels': [r'$global$', r'$local$']},
        'compression': {'title': False, 'labels': [r'$global$', r'$local$']},
        'relative': {'title': False, 'check_never_negative': True},
        'relative_stats': {},
        'window_stats': {}
    }

    # For each dataset:
    #   Create a pdf.
    #   For each file in the dataset:
    #       For each data type:
    #           Add a pdf page with the following graphs:
    #               + compression rate
    #               + relative difference
    #               + window size
    #               + stats
    def __init__(self, path, datasets_names=None):
        self.df_3_local_1 = ResultsToDataframe(ResultsReader('raw', 3)).create_full_df()  # local with best local window
        self.df_3_local_2 = ResultsToDataframe(ResultsReader('raw', 3)).create_full_df()  # local with best global window
        self.df_3_global = ResultsToDataframe(ResultsReader('global', 3)).create_full_df()
        self.path = path + 'window/'

        self.dataset_names = datasets_names or ExperimentsUtils.datasets_with_multiple_files()

        # iteration variables
        self.dataset_id = None
        self.dataset_name = None
        self.filename = None
        self.pdf = None
        self.col_index = None
        self.pd_utils_3_global = None

    def create_pdfs(self):
        for dataset_id, self.dataset_name in enumerate(self.dataset_names):
            print self.dataset_name
            self.dataset_id = dataset_id + 1
            self.created_pdf_for_dataset()

    def created_pdf_for_dataset(self):
        pdf_name = self.path + str(self.dataset_id) + "-" + self.dataset_name + ".pdf"
        with PdfPages(pdf_name) as self.pdf:
            self.pd_utils_3_global = PandasUtils(self.dataset_name, 'Global', self.df_3_global, 3)

            dataset_filenames = ExperimentsUtils.dataset_csv_filenames(self.dataset_name)
            for self.filename in dataset_filenames:
                print self.filename
                self.create_pdf_pages()

    def create_pdf_pages(self):
        # create panda_utils
        pd_utils_3_local_1 = PandasUtils(self.dataset_name, self.filename, self.df_3_local_1, 3)
        pd_utils_3_local_2 = PandasUtils(self.dataset_name, self.filename, self.df_3_local_2, 3)

        for self.col_index in range(1, ExperimentsUtils.get_dataset_data_columns_count(self.dataset_name) + 1):
            mod_pd_utils_3_local_2 = self.set_global_window(pd_utils_3_local_2)
            # TODO: change order to make Relative Difference <= 0
            self.create_pdf_page(mod_pd_utils_3_local_2, pd_utils_3_local_1)
            # exit(1)

    #
    # In the local results, consider the best global window instead of the best local window
    #
    def set_global_window(self, pd_utils_3_local_2):
        new_df = pd_utils_3_local_2.df

        for coder_name in self.CODERS_ARRAY:
            print coder_name
            for threshold in ExperimentsUtils.THRESHOLDS:
                # print threshold
                best_global_window = self.pd_utils_3_global.min_value_for_threshold(coder_name, self.col_index, threshold)['window']
                best_local_window = pd_utils_3_local_2.min_value_for_threshold(coder_name, self.col_index, threshold)['window']
                if best_global_window != best_local_window:
                    print str(threshold) + " - GLOBAL = " + str(best_global_window) + " - LOCAL = " + str(best_local_window)
                    # remove every threshold value other than the one that uses the best global window
                    index_names = new_df[(new_df['coder'] == coder_name) & (new_df['threshold'] == threshold) & (new_df['window'] != best_global_window)].index
                    new_df.drop(index_names, inplace=True)
        mod_pd_utils_3_local_2 = PandasUtils(self.dataset_name, self.filename, new_df, 3, False)
        return mod_pd_utils_3_local_2

    def create_pdf_page(self, pd_utils_3_local_1, pd_utils_3_local_2):
        pdf_page = PdfPage(pd_utils_3_local_1, pd_utils_3_local_2, self.filename, self.col_index, self.FIGSIZE_H, self.FIGSIZE_V, self.PLOT_OPTIONS)
        fig, plt = pdf_page.create(self.CODERS_ARRAY, self.PLOTS_ARRAY, self.PLOTS_MATRIX)
        plt.subplots_adjust(wspace=PDFS3.WSPACE, hspace=PDFS3.HSPACE)
        # plt.show(); exit(0) # uncomment to show first page
        self.pdf.savefig(fig)
        plt.close()

# PDFS1(False).create_pdfs()
# PDFS1(True).create_pdfs()
# PDFS1(True, ['NOAA-SPC-wind']).create_pdfs()

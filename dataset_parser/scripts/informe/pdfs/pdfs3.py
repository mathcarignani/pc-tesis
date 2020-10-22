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
from scripts.informe.latex_tables.table_windows.table_windows import TableWindows


class PDFS3(PDFSCommon):
    SUBPLOT_SPACING_W_H = (0.1, 0.05)
    FIG_SIZE_H_V = (10, 11)
    CODERS_ARRAY = ['CoderPCA', 'CoderAPCA', 'CoderCA', 'CoderPWLH', 'CoderPWLHInt', 'CoderGAMPSLimit', 'CoderFR']
    PLOTS_ARRAY = ['window', 'relative']
    PLOTS_MATRIX = [
        [['CoderPCA', 'window'],       ['CoderAPCA', 'window'],         ['CoderCA', 'window'],              ['CoderFR', 'window']],
        None,
        [['CoderPCA', 'relative'],  ['CoderAPCA', 'relative'],    ['CoderCA', 'relative'],         ['CoderFR', 'relative']],
        None,
        [['CoderPWLH', 'window'],      ['CoderPWLHInt', 'window'],      ['CoderGAMPSLimit', 'window']],
        None,
        [['CoderPWLH', 'relative'], ['CoderPWLHInt', 'relative'], ['CoderGAMPSLimit', 'relative']],
    ]
    HEIGHT_RATIOS = [30, 0, 30, 15, 30, 0, 30]
    PLOT_OPTIONS = {
        'window': {'title': 12, 'labels': [r'$OWS$', r'$LOWS$']},
        'relative': {'check_pdf3': True, 'show_xlabel': True}
    }

    def __init__(self, path, datasets_names=None):
        assert(len(self.HEIGHT_RATIOS) == len(self.PLOTS_MATRIX))

        self.df_M_local = ResultsToDataframe(ResultsReader('local', "M")).create_full_df()
        self.df_M_global = ResultsToDataframe(ResultsReader('global', "M")).create_full_df()
        self.path = path

        self.dataset_names = datasets_names or ExperimentsUtils.datasets_with_multiple_files()
        self.mode = 'local'

        # iteration variables
        self.dataset_id = None
        self.dataset_name = None
        self.filename = None
        self.pdf_name = None
        self.col_index = None
        self.pd_utils_3_global = None
        self.latex_table_data = {}

    def create_pdfs(self):
        for dataset_id, self.dataset_name in enumerate(self.dataset_names):
            print(self.dataset_name)
            self.dataset_id = dataset_id + 1
            self.created_dataset_pdf_file()

    def created_dataset_pdf_file(self):
        self.pdf_name = self.create_pdf_name(self.path, self.dataset_id, self.dataset_name)
        with PdfPages(self.pdf_name) as pdf:
            self.pd_utils_3_global = PandasUtils(self.dataset_name, 'Global', self.df_M_global, "M")
            for self.filename_index, self.filename in enumerate(self.dataset_filenames()):
                print("  " + self.filename)
                self.create_pdf_pages(pdf, self.dataset_name, self.filename)

    def create_pdf_pages(self, pdf, dataset_name, filename):
        for self.col_index in self.column_indexes(dataset_name):
            # create panda_utils. Must do it inside this block to prevent issue with many datatypes in a single dataset
            df_M_local_copy_1 = PandasMethods.copy(self.df_M_local)
            df_M_local_copy_2 = PandasMethods.copy(self.df_M_local)
            pd_utils_3_local_1 = PandasUtils(dataset_name, filename, df_M_local_copy_1, "M")  # local with best LOCAL window
            pd_utils_3_local_2 = PandasUtils(dataset_name, filename, df_M_local_copy_2, "M")  # local with best GLOBAL window

            mod_pd_utils_3_local_2 = self.set_global_window(pd_utils_3_local_2)
            # TODO: change order to make Relative Difference <= 0
            self.create_pdf_page(pdf, filename, mod_pd_utils_3_local_2, pd_utils_3_local_1)

    #
    # In the local results, consider the best global window instead of the best local window
    #
    def set_global_window(self, pd_utils_3_local_2):
        new_df = pd_utils_3_local_2.df

        for coder_name in self.CODERS_ARRAY:
            # print("  " + coder_name)
            for threshold in ExperimentsUtils.THRESHOLDS:
                # print(threshold)
                best_global_window = self.pd_utils_3_global.min_value_for_threshold(coder_name, self.col_index, threshold)['window']
                best_local_window = pd_utils_3_local_2.min_value_for_threshold(coder_name, self.col_index, threshold)['window']
                if best_global_window != best_local_window:
                    # print str(threshold) + " - GLOBAL = " + str(best_global_window) + " - LOCAL = " + str(best_local_window)
                    # remove every threshold value other than the one that uses the best global window
                    index_names = new_df[(new_df['coder'] == coder_name) & (new_df['threshold'] == threshold) & (new_df['window'] != best_global_window)].index
                    new_df.drop(index_names, inplace=True)
        mod_pd_utils_3_local_2 = PandasUtils(self.dataset_name, self.filename, new_df, "M", False)
        return mod_pd_utils_3_local_2

    def create_pdf_page(self, pdf, filename, pd_utils_3_local_1, pd_utils_3_local_2):
        pdf_page = PdfPage(pd_utils_3_local_1, pd_utils_3_local_2, filename, self)

        # IMPORTANT: resize before setting the labels to avoid this issue: https://stackoverflow.com/q/50395392/4547232
        pdf_page.plt.subplots_adjust(wspace=PDFS3.SUBPLOT_SPACING_W_H[0], hspace=PDFS3.SUBPLOT_SPACING_W_H[1])

        fig, plt = pdf_page.create(self.CODERS_ARRAY, self.PLOTS_ARRAY, self.PLOTS_MATRIX)
        pdf.savefig(fig)
        plt.savefig(self.create_image_name_(), format='pdf')
        plt.close()

    def create_image_name_(self):
        filename = self.pdf_name.replace(".pdf", "-") + str(self.filename_index + 1) + "-" + str(self.col_index) + ".pdf"
        filename = filename.replace("PDF-", "")
        return filename


    ####################################################################################################################
    ####################################################################################################################
    ####################################################################################################################

    def add_data(self, algorithm, values):
        minimum, maximum = min(values), max(values)
        assert(minimum >= 0)
        # (1) Check that the maximum does not change and occurs in the expected dataset/coder
        expected_maximum = 10.598254581045069

        result = {}
        if self.dataset_name == "IRKIS" and algorithm == "CoderPCA" and self.filename == "vwc_1203.dat.csv":
            assert(maximum == expected_maximum)
            assert(str(round(maximum, 2)) == "10.6")
            result = {'keys': ["PlotMax"], 'values': [maximum]}
        else:
            assert(maximum < expected_maximum)

        # (2) Add information to the latex table structure
        if not self.latex_table_data.get(algorithm):
            self.latex_table_data[algorithm] = []
        self.latex_table_data[algorithm].append({'values': values})

        return result

    def create_latex_table(self, path):
        algorithms_data = {}
        total = [0, 0, 0, 0, 0]
        for algorithm, array in self.latex_table_data.items():
            range_1, range_2, range_3, range_4, range_5 = 0, 0, 0, 0, 0
            for dictionary in array:
                for value in dictionary['values']:
                    if value == 0:
                        range_1 += 1
                        total[0] += 1
                    elif 0 < value <= 1:
                        range_2 += 1
                        total[1] += 1
                    elif 1 < value <= 2:
                        range_3 += 1
                        total[2] += 1
                    elif 2 < value <= 5:
                        range_4 += 1
                        total[3] += 1
                    elif 5 < value <= 11:
                        range_5 += 1
                        total[4] += 1
                algorithms_data[algorithm] = [range_1, range_2, range_3, range_4, range_5]
        algorithms_data['Total'] = total
        TableWindows(algorithms_data, path).create_table()

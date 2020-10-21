import sys
sys.path.append('.')

from scripts.informe.results_parsing.results_reader import ResultsReader
from scripts.informe.results_parsing.results_to_dataframe import ResultsToDataframe
from scripts.informe.pandas_utils.pandas_utils import PandasUtils
from scripts.informe.pdfs.pdf_page import PdfPage
from scripts.informe.pdfs.pdfs_common import PDFSCommon
from scripts.compress.experiments_utils import ExperimentsUtils
from scripts.informe.latex_tables.table_relative.table_relative import TableRelative


class PDFS1(PDFSCommon):
    SUBPLOT_SPACING_W_H = (0.1, 0.05)
    FIG_SIZE_H_V = (10, 14)
    CODERS_ARRAY = ['CoderPCA', 'CoderAPCA', 'CoderCA', 'CoderPWLH', 'CoderPWLHInt', 'CoderGAMPSLimit']
    PLOTS_ARRAY = ['compression', 'relative']
    PLOTS_MATRIX = [
        [['CoderPCA', 'compression'],  ['CoderAPCA', 'compression'],    ['CoderCA', 'compression']],
        None,
        [['CoderPCA', 'relative'],     ['CoderAPCA', 'relative'],       ['CoderCA', 'relative']],
        None,
        [['CoderPWLH', 'compression'], ['CoderPWLHInt', 'compression'], ['CoderGAMPSLimit', 'compression']],
        None,
        [['CoderPWLH', 'relative'],    ['CoderPWLHInt', 'relative'],    ['CoderGAMPSLimit', 'relative']]
    ]
    HEIGHT_RATIOS = [30, 0, 30, 10, 30, 0, 30]
    PLOT_OPTIONS = {
        'compression': {'title': True, 'labels': [r'$a_{NM}$', r'$a_M$']},
        'relative': {'add_min_max_circles': True, 'show_xlabel': True}
    }

    def __init__(self, path, mode='global', datasets_names=None):
        assert(len(self.HEIGHT_RATIOS) == len(self.PLOTS_MATRIX))
        PDFSCommon.check_valid_mode(mode)

        self.df_NM = ResultsToDataframe(ResultsReader(mode, "NM")).create_full_df()
        self.df_M = ResultsToDataframe(ResultsReader(mode, "M")).create_full_df()

        self.col_index = None  # iteration variable
        self.latex_table_data = {}
        super(PDFS1, self).__init__(path + mode + "/", mode, datasets_names)

    def create_pdf_pages(self, pdf, dataset_name, filename):
        panda_utils_NM = PandasUtils(dataset_name, filename, self.df_NM, "NM")
        panda_utils_M = PandasUtils(dataset_name, filename, self.df_M, "M")

        for self.col_index in self.column_indexes(dataset_name):
            self.create_pdf_page(pdf, filename, panda_utils_NM, panda_utils_M)

    def create_pdf_page(self, pdf, filename, panda_utils_NM, panda_utils_M):
        pdf_page = PdfPage(panda_utils_NM, panda_utils_M, filename, self)

        # IMPORTANT: resize before setting the labels to avoid this issue: https://stackoverflow.com/q/50395392/4547232
        pdf_page.plt.subplots_adjust(wspace=PDFS1.SUBPLOT_SPACING_W_H[0], hspace=PDFS1.SUBPLOT_SPACING_W_H[1])

        fig, plt = pdf_page.create(self.CODERS_ARRAY, self.PLOTS_ARRAY, self.PLOTS_MATRIX)
        pdf.savefig(fig)
        if self.mode == 'global':
            plt.savefig(self.create_image_name(self.pdf_name, self.col_index), format='pdf')
        plt.close()

    ####################################################################################################################
    ####################################################################################################################
    ####################################################################################################################

    def check_min_max(self, algorithm, values):
        minimum, maximum = min(values), max(values)

        # (1) Add information to the latex table structure
        negative, zero, positive = 0, 0, 0
        for value in values:
            if value < 0:
                negative += 1
            elif value == 0:
                zero += 1
            else:
                positive += 1
        data = {'negative': negative, 'zero': zero, 'positive': positive, 'min': minimum, 'max': maximum}

        if not self.latex_table_data.get(self.dataset_name):
            self.latex_table_data[self.dataset_name] = []

        # (2) Check that the minimum and maximum do not change and occur in the expected dataset/coder
        expected_maximum = 50.77815044407712
        expected_minimum = -0.2898755656108619

        result = [None, None]
        if self.dataset_name == "NOAA-SST" and algorithm == "CoderPCA":
            assert(maximum == expected_maximum)
            result = ["PlotMax", maximum]
        else:
            assert(maximum < expected_maximum)

        if self.dataset_name == "NOAA-SPC-tornado" and algorithm == "CoderAPCA" and self.col_index == 2:
            assert(minimum == expected_minimum)
            result = ["PlotMin", minimum]
        else:
            assert(minimum > expected_minimum)

        data['info'] = result[0]
        self.latex_table_data[self.dataset_name].append(data)
        return result

    def create_latex_table(self, path):
        datasets_data = {}
        for dataset_name, plot_array in self.latex_table_data.items():
            negative, zero, positive = 0, 0, 0
            minimum, maximum = plot_array[0]['min'], plot_array[0]['max']
            info = None

            for plot_data in plot_array:
                negative += plot_data['negative']
                zero += plot_data['zero']
                positive += plot_data['positive']
                minimum = plot_data['min'] if plot_data['min'] < minimum else minimum
                maximum = plot_data['max'] if plot_data['max'] > maximum else maximum
                info = info or plot_data['info']

            short_name = ExperimentsUtils.get_dataset_short_name(dataset_name)
            datasets_data[short_name] = {
                'negative': negative, 'zero': zero, 'positive': positive, 'min': minimum, 'max': maximum, 'info': info
            }

        TableRelative(datasets_data, path).create_table()

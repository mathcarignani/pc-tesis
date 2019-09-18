import sys
sys.path.append('.')

from auxi.os_utils import python_project_path
from scripts.informe.results_parsing.results_reader import ResultsReader
from scripts.informe.results_parsing.results_to_dataframe import ResultsToDataframe
from file_utils.text_utils.text_file_writer import TextFileWriter
from file_utils.csv_utils.csv_writer import CSVWriter
from scripts.compress.experiments_utils import ExperimentsUtils
from scripts.informe.pandas_utils.pandas_utils import PandasUtils
from scripts.informe.data_analysis.threshold_compare import ThresholdCompare


#
# This script does the same as avances11/process_results.py but using pandas data handling.
#
class ProcessResults(object):
    CODERS_ARRAY = ['CoderPCA', 'CoderAPCA', 'CoderCA', 'CoderPWLH', 'CoderPWLHInt', 'CoderFR', 'CoderSF',
                    # 'CoderGAMPS', => ignore this coder
                    'CoderGAMPSLimit']
    DEFAULT_PATH = python_project_path() + "/scripts/informe/data_analysis/out_process_results"
    MM = 3

    def __init__(self, global_mode, path=None):
        self.path = path or self.DEFAULT_PATH
        self.debug_mode = False
        self.global_mode = global_mode
        key = 'global' if self.global_mode else 'raw_basic'
        self.results_reader = ResultsReader(key, ProcessResults.MM)
        self.df = ResultsToDataframe(self.results_reader).create_full_df()
        self.threshold_compare = ThresholdCompare(ResultsReader('raw', ProcessResults.MM))

    def process_results(self):
        self.__write_headers()
        self.__datasets_iteration()
        self.csv_writer_latex.print_end()

    def __write_headers(self):
        extra_str = 'global' if self.global_mode else 'local'
        self.csv_writer_1 = Writer1.filename(self.path, extra_str)
        self.csv_writer_1.write_row(Writer1.first_row())

        self.csv_writer_2 = Writer2.filename(self.path, extra_str)
        self.csv_writer_2.write_row(Writer2.first_row())
        self.csv_writer_2.write_row(Writer2.second_row())

        self.csv_writer_latex = WriterLatex(self.path, extra_str)

    def __datasets_iteration(self):
        for dataset_id, self.dataset_name in enumerate(ExperimentsUtils.DATASET_NAMES):
            print self.dataset_name
            self._print(self.dataset_name)
            self.__set_dataset(self.dataset_name)
            self.__filenames_iteration()

    def __filenames_iteration(self):
        dataset_filenames = ProcessResults.dataset_filenames(self.dataset_name, self.global_mode)
        for self.filename in dataset_filenames:
            self._print(self.filename)
            self.__set_filename(self.filename)
            self.__columns_iteration()

    def __columns_iteration(self):
        self.panda_utils = PandasUtils(self.dataset_name, self.filename, self.df, ProcessResults.MM)
        for self.col_index in range(1, ExperimentsUtils.get_dataset_data_columns_count(self.dataset_name) + 1):
            if self.__local_or_single_file():
                self.threshold_compare.calculate_matching_thresholds(self.dataset_name, self.filename, self.col_index)
            self.col_name = ExperimentsUtils.COLUMN_INDEXES[self.dataset_name][self.col_index - 1]
            self._print(self.col_name)
            self.__column_results_writer_1()
            self.__column_results_writer_2()

    def __column_results_writer_1(self):
        self.csv_writer_1.write_row(['', '', self.col_name])
        for self.coder_name in ProcessResults.CODERS_ARRAY:
            self._print(self.coder_name)
            self.__coder_results()

    #
    # Get the best Window for each <Coder, Column, Threshold> combination
    #
    def __coder_results(self):
        windows, percentages = [], []
        previous_window, previous_percentage = None, None
        for threshold in ExperimentsUtils.THRESHOLDS:
            row_df = self.panda_utils.min_value_for_threshold(self.coder_name, self.col_index, threshold)
            window, percentage, _ = ProcessResults.get_values(row_df, self.col_index)

            new_window, new_percentage = window, percentage
            if self.__same_result(threshold):
                assert(threshold > 0); assert(window == previous_window); assert(percentage == previous_percentage)
                new_window, new_percentage = '=', '='
            elif self.coder_name == 'CoderSF':
                new_window = ''  # CoderSF this coder doesn't have a window param

            windows.append(new_window); percentages.append(new_percentage)
            previous_window, previous_percentage = window, percentage

        self.csv_writer_1.write_row(['', '', '', self.coder_name] + windows + [''] + percentages)

    #
    # Get the best <Coder, Window> combination for each <Column, Threshold> combination
    #
    def __column_results_writer_2(self):
        previous_coder, previous_window, previous_percentage = None, None, None
        threshold_results = [None, None, self.col_name]
        for threshold in ExperimentsUtils.THRESHOLDS:
            row_df = self.panda_utils.min_value_for_threshold(None, self.col_index, threshold)
            window, percentage, coder_name = ProcessResults.get_values(row_df, self.col_index)
            coder_name = coder_name.replace("Coder", "")

            new_coder, new_window, new_percentage = coder_name, window, percentage
            if self.__same_result(threshold):
                assert(threshold > 0); assert(coder_name == previous_coder); assert(window == previous_window);
                assert(percentage == previous_percentage)
                new_coder, new_window, new_percentage = '=', '=', '='

            threshold_results += [new_coder, new_window, new_percentage]
            previous_coder, previous_window, previous_percentage = coder_name, window, percentage
        self.csv_writer_2.write_row(threshold_results)
        self.csv_writer_latex.set_threshold_results(threshold_results)

    def __set_dataset(self, dataset_name):
        self.__write_two_files([dataset_name])
        self.csv_writer_latex.set_dataset(dataset_name)

    def __set_filename(self, filename):
        self.__write_two_files(['', filename])
        self.csv_writer_latex.set_filename(filename)

    def __write_two_files(self, row):
        self.csv_writer_1.write_row(row)
        self.csv_writer_2.write_row(row)

    def __local_or_single_file(self):
        condition1 = not self.global_mode
        condition2 = self.global_mode and self.__single_file_dataset()
        return condition1 or condition2

    def __same_result(self, threshold):
        return self.__local_or_single_file() and self.threshold_compare.matching_threshold(threshold)

    def __single_file_dataset(self):
        return ExperimentsUtils.dataset_csv_files_count(self.dataset_name) == 1

    def _print(self, value):
        if self.debug_mode:
            print value

    @staticmethod
    def get_values(row_df, col_index):
        window = int(row_df['window'])
        percentage = ProcessResults.parse_percentage(row_df, col_index)
        coder_name = row_df['coder']
        return window, percentage, coder_name

    @staticmethod
    def parse_percentage(row_df, col_index):
        percentage_key = ResultsToDataframe.percentage_column_key(col_index)
        return round(row_df[percentage_key], 2)

    @staticmethod
    def dataset_filenames(dataset_name, global_mode):
        filenames = ExperimentsUtils.dataset_csv_filenames(dataset_name)
        return ['Global'] if global_mode and len(filenames) > 1 else filenames


class Writer1(object):
    @staticmethod
    def filename(path, extra_str):
        return CSVWriter(path, extra_str + '-process1.csv')

    @staticmethod
    def first_row():
        row = ["Dataset", "Filename", "Column", "Coder"]
        row += ExperimentsUtils.THRESHOLDS + [''] + ExperimentsUtils.THRESHOLDS
        return row


class Writer2(object):
    @staticmethod
    def filename(path, extra_str):
        return CSVWriter(path, extra_str + '-process2.csv')

    @staticmethod
    def first_row():
        return ["Dataset", "Filename", "Column"] + Writer2.thresholds_array()

    @staticmethod
    def thresholds_array():
        array = []
        for threshold in ExperimentsUtils.THRESHOLDS:
            array += [None, str(threshold) + " (%)", None]
        return array

    @staticmethod
    def second_row():
        array = []
        for _ in ExperimentsUtils.THRESHOLDS:
            array += ["Coder", "Win", "CR (%)"]
        return [None, None, None] + array


class WriterLatex(object):
    def __init__(self, path, extra_str):
        self.file = TextFileWriter(path, extra_str + '-process2-LATEX.txt')
        self.print_start()

    def write_line(self, line):
        self.file.write_line(line)

    def print_start(self):
        count = len(ExperimentsUtils.THRESHOLDS)
        self.write_line("\centering")
        self.write_line(r"\begin{tabular}{| l | l " + ("| c | c | c |" * count) + "}")
        self.write_line("\cline{3-" + str(count * 3 + 2)+ "}")
        self.write_line(WriterLatex.threshold_line())
        self.write_line("Dataset & Data Type" + (" & {c} & {w} & {CR}" * count) + r" \\\hline\hline")

    def set_dataset(self, dataset_name):
        print "set_dataset => " + dataset_name

    def set_filename(self, filename):
        print "set_filename => " + filename

    def set_threshold_results(self, threshold_results):
        print "set_threshold_results => " + str(threshold_results)

    @staticmethod
    def threshold_line():
        line = "\multicolumn{1}{c}{}& \multicolumn{1}{c|}{} "
        for thre in ExperimentsUtils.THRESHOLDS:
            line += "& \multicolumn{3}{c|" + ("|" if thre != 30 else "") + "}{e = " + str(thre) + "} "
        line += r"\\\hline"
        return line

    def print_end(self):
        self.write_line("\end{tabular}")
        self.write_line("\caption{Mask results overview.}")
        self.write_line("\label{experiments:mask-results-overview}")


def run():
    ProcessResults(True).process_results()
    ProcessResults(False).process_results()

# run()

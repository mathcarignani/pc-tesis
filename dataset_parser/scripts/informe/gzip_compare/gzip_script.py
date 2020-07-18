import sys
sys.path.append('.')


from file_utils.csv_utils.csv_writer import CSVWriter
from scripts.informe.results_parsing.results_reader import ResultsReader
from scripts.informe.results_parsing.results_to_dataframe import ResultsToDataframe
from scripts.informe.data_analysis.process_results.process_results import ProcessResults
from scripts.compress.experiments_utils import ExperimentsUtils
from scripts.informe.math_utils import MathUtils
from scripts.informe.pandas_utils.pandas_utils import PandasUtils
from scripts.informe.gzip_compare.gzip_compress import GZipCompress


class GZipScript(object):
    FIRST_ROW = ["Dataset", "Filename", "Column", "Compression Ratio", "Bits (Gzip)", "Bits (CoderBase)", "Bytes (Gzip)"]

    def __init__(self, path, filename, transpose=True):
        self.path = path
        self.transpose = transpose
        self.output = CSVWriter(path, filename)
        self.debug_mode = True

        self.results_reader = ResultsReader('local', 0)
        self.df = ResultsToDataframe(self.results_reader).create_full_df()

    def run(self):
        self.output.write_row(self.FIRST_ROW)
        self.__datasets_iteration()

    def __datasets_iteration(self):
        for dataset_id, self.dataset_name in enumerate(ExperimentsUtils.DATASET_NAMES):
            self.results_hash = {}
            print(self.dataset_name)
            self._print(self.dataset_name)
            self.output.write_row([self.dataset_name])
            self.__filenames_iteration()

    def __filenames_iteration(self):
        dataset_filenames = ProcessResults.dataset_filenames(self.dataset_name, False)

        for self.col_index in range(1, ExperimentsUtils.get_dataset_data_columns_count(self.dataset_name) + 1):
            self.col_name = ExperimentsUtils.COLUMN_INDEXES[self.dataset_name][self.col_index - 1]
            self.results_hash[self.col_name] = {'total_bits': 0, 'total_bits_base': 0, 'total_bytes': 0}

        for self.filename in dataset_filenames:
            self._print(self.filename)
            self.output.write_row(['', self.filename])
            self.__columns_iteration()
        if len(dataset_filenames) > 1:
            self.__global_results()

    def __columns_iteration(self):
        for self.col_index in range(1, ExperimentsUtils.get_dataset_data_columns_count(self.dataset_name) + 1):
            self.col_name = ExperimentsUtils.COLUMN_INDEXES[self.dataset_name][self.col_index - 1]
            compare = GZipCompress(self.dataset_name, self.filename, self.col_index, self.path, self.transpose)
            total_bytes, total_bits = compare.total_size()
            total_bits_base = self.__get_total_bits_coder_base()
            self.results_hash[self.col_name]['total_bits'] += total_bits
            self.results_hash[self.col_name]['total_bits_base'] += total_bits_base
            compression_ratio = MathUtils.calculate_percentage(total_bits_base, total_bits, 2)
            self.results_hash[self.col_name]['total_bytes'] += total_bytes
            self.output.write_row(['', '', self.col_name, compression_ratio, total_bits, total_bits_base, total_bytes])

    def __get_total_bits_coder_base(self):
            panda_utils = PandasUtils(self.dataset_name, self.filename, self.df, 0)
            base_df = panda_utils.coder_base_df()
            data_column_key = ResultsToDataframe.data_column_key(self.col_index)
            return base_df[data_column_key]

    def __global_results(self):
        self.output.write_row(['', 'Global'])
        for self.col_index in range(1, ExperimentsUtils.get_dataset_data_columns_count(self.dataset_name) + 1):
            self.col_name = ExperimentsUtils.COLUMN_INDEXES[self.dataset_name][self.col_index - 1]
            total_bits = self.results_hash[self.col_name]['total_bits']
            total_bits_base = self.results_hash[self.col_name]['total_bits_base']
            compression_ratio = MathUtils.calculate_percentage(total_bits_base, total_bits, 2)
            total_bytes = self.results_hash[self.col_name]['total_bytes']
            self.output.write_row(['', '', self.col_name, compression_ratio, total_bits, total_bits_base, total_bytes])

    def _print(self, value):
        if self.debug_mode:
            print(value)

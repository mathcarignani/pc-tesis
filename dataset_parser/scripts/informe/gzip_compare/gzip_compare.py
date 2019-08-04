import sys
sys.path.append('.')

import os

from file_utils.csv_utils.csv_reader import CSVReader
from file_utils.csv_utils.csv_writer import CSVWriter
from scripts.informe.results_parsing.results_reader import ResultsReader
from scripts.informe.results_parsing.results_to_dataframe import ResultsToDataframe
from scripts.compress.experiments_utils import ExperimentsUtils
from scripts.informe.data_analysis.process_results import ProcessResults
from scripts.informe.math_utils import MathUtils
from scripts.informe.pandas_utils.pandas_utils import PandasUtils


OUT_PATH = "/Users/pablocerve/Documents/FING/Proyecto/pc-tesis/dataset_parser/scripts/informe/gzip_compare/out"


class GZipCompare(object):
    COMPRESS_PATH = "/Users/pablocerve/Documents/FING/Proyecto/pc-tesis/dataset_parser/scripts/informe/gzip_compare/c/"

    def __init__(self, dataset_name, filename, col_index):
        self.dataset_name = dataset_name
        self.filename = filename
        self.col_index = col_index  # 1, 2, 3, ...

        # set filenames
        self.column_filename = filename + str(self.col_index) + ".csv"
        self.compressed_filename = self.column_filename + ".tar.gz"

    def total_bits(self):
        self.create_column_csv()
        self.compress_column_csv()
        total_bits = self.read_total_bits()
        self.remove_files()
        return total_bits

    def create_column_csv(self):
        dataset_columns_count = ExperimentsUtils.get_dataset_data_columns_count(self.dataset_name)
        reader = CSVReader(ExperimentsUtils.get_dataset_path(self.dataset_name), self.filename)
        writer = CSVWriter(GZipCompare.COMPRESS_PATH, self.column_filename)
        counter = 0
        while reader.continue_reading:
            row = reader.read_line()
            counter += 1
            if counter < 5:  # (1) REMOVE HEADER
                continue
            row.pop(0)  # (2) IGNORE TIME DELTA
            new_row = []
            for i, value in enumerate(row):
                # (3) APPEND VALUES FOR COLUMNS WITH THE MATCHING INDEX
                if i % dataset_columns_count == (self.col_index - 1):
                    new_row.append(row[i])
            writer.write_row(new_row)
        reader.close()
        writer.close()

    def compress_column_csv(self):
        #
        # tar cvf - input_file_path/input_filename | gzip -9 - > input_file_path/input_filename.tar.gz
        #
        input_file_path = GZipCompare.COMPRESS_PATH + self.column_filename
        output_file_path = GZipCompare.COMPRESS_PATH + self.compressed_filename
        command = "tar cvf - " + input_file_path + " | gzip -1 - > " + output_file_path
        os.system(command)

    def read_total_bits(self):
        st = os.stat(GZipCompare.COMPRESS_PATH + self.compressed_filename)
        byte_size = st.st_size
        bits_size = byte_size*8
        return bits_size

    def remove_files(self):
        os.remove(GZipCompare.COMPRESS_PATH + self.column_filename)
        os.remove(GZipCompare.COMPRESS_PATH + self.compressed_filename)


class ScriptGZipCompare(object):
    def __init__(self):
        self.output = CSVWriter(OUT_PATH, "results.csv")
        self.debug_mode = True

        self.results_reader = ResultsReader('raw', 0)
        self.df = ResultsToDataframe(self.results_reader).create_full_df()

    def run(self):
        self.output.write_row(["Dataset", "Filename", "Column", "Compression Ratio", "Bits (Gzip)", "Bits (CoderBase)"])
        self.__datasets_iteration()

    def __datasets_iteration(self):
        for dataset_id, self.dataset_name in enumerate(ExperimentsUtils.DATASET_NAMES):
            self.results_hash = {}
            print self.dataset_name
            self._print(self.dataset_name)
            self.output.write_row([self.dataset_name])
            self.__filenames_iteration()

    def __filenames_iteration(self):
        dataset_filenames = ProcessResults.dataset_filenames(self.dataset_name, False)

        for self.col_index in range(1, ExperimentsUtils.get_dataset_data_columns_count(self.dataset_name) + 1):
            self.col_name = ExperimentsUtils.COLUMN_INDEXES[self.dataset_name][self.col_index - 1]
            self.results_hash[self.col_name] = {'total_bits': 0, 'total_bits_base': 0}

        for self.filename in dataset_filenames:
            self._print(self.filename)
            self.output.write_row(['', self.filename])
            self.__columns_iteration()
        if len(dataset_filenames) > 1:
            self.__global_results()

    def __columns_iteration(self):
        for self.col_index in range(1, ExperimentsUtils.get_dataset_data_columns_count(self.dataset_name) + 1):
            self.col_name = ExperimentsUtils.COLUMN_INDEXES[self.dataset_name][self.col_index - 1]
            total_bits = GZipCompare(self.dataset_name, self.filename, self.col_index).total_bits()
            total_bits_base = self.__get_total_bits_coder_base()
            self.results_hash[self.col_name]['total_bits'] += total_bits
            self.results_hash[self.col_name]['total_bits_base'] += total_bits_base
            compression_ratio = MathUtils.calculate_percentage(total_bits_base, total_bits, 2)
            self.output.write_row(['', '', self.col_name, compression_ratio, total_bits, total_bits_base])

    def __get_total_bits_coder_base(self):
            panda_utils = PandasUtils(self.dataset_name, self.filename, self.df, 0)
            basic_df = panda_utils.coder_basic_df()
            data_column_key = ResultsToDataframe.data_column_key(self.col_index)
            return basic_df[data_column_key]

    def __global_results(self):
        self.output.write_row(['', 'Global'])
        for self.col_index in range(1, ExperimentsUtils.get_dataset_data_columns_count(self.dataset_name) + 1):
            self.col_name = ExperimentsUtils.COLUMN_INDEXES[self.dataset_name][self.col_index - 1]
            total_bits = self.results_hash[self.col_name]['total_bits']
            total_bits_base = self.results_hash[self.col_name]['total_bits_base']
            compression_ratio = MathUtils.calculate_percentage(total_bits_base, total_bits, 2)
            self.output.write_row(['', '', self.col_name, compression_ratio, total_bits, total_bits_base])

    def _print(self, value):
        if self.debug_mode:
            print value

ScriptGZipCompare().run()

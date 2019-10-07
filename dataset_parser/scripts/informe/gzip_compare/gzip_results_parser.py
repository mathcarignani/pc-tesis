import sys
sys.path.append('.')

from scripts.informe.gzip_compare.gzip_common import GZipCommon
from file_utils.csv_utils.csv_reader import CSVReader


class GzipResultsParser(object):
    def __init__(self, transpose=True):
        self.input = CSVReader(GZipCommon.OUT_PATH, GZipCommon.FILENAME[transpose])

    def compression_ratio(self, dataset_name, filename, col_name):
        # print dataset_name, filename, col_name
        self.input.goto_row(0)
        self.__find_match(0, dataset_name)
        self.__find_match(1, filename)
        self.__find_match(2, col_name)
        compression_ratio = float(self.line[3])
        return compression_ratio

    def __find_match(self, col_index, value):
        # print col_index, value
        while self.input.continue_reading:
            line = self.input.read_line()
            if line[col_index] == value:
                self.line = line
                return
        raise(StandardError, "Reached EOF")

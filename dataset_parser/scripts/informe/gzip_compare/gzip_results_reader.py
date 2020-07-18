import sys
sys.path.append('.')

from file_utils.csv_utils.csv_reader import CSVReader


class GzipResultsReader(object):
    def __init__(self, path, filename):
        self.input = CSVReader(path, filename)

    def gzip_and_base_bits(self, dataset_name, filename, column_name):
        self.input.goto_row(0)
        self.__find_match(0, dataset_name)
        self.__find_match(1, filename)  # filename can be 'Global'
        self.__find_match(2, column_name)
        gzip_bits, base_bits = int(self.line[4]), int(float(self.line[5]))
        return gzip_bits, base_bits

    def __find_match(self, col_index, value):
        # print col_index, value
        while self.input.continue_reading:
            line = self.input.read_line()
            if line[col_index] == value:
                self.line = line
                return
        raise KeyError('Reached EOF')

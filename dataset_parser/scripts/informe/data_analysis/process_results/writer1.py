import sys
sys.path.append('.')

from file_utils.csv_utils.csv_writer import CSVWriter
from scripts.compress.experiments_utils import ExperimentsUtils


class Writer1(object):
    def __init__(self, path, extra_str):
        self.file = CSVWriter(path, extra_str + '-process1.csv')
        self.write_first_row()
        self.data_rows = []

    def write_first_row(self):
        row = ["Dataset", "Filename", "Column", "Coder"]
        row += ExperimentsUtils.THRESHOLDS + [''] + ExperimentsUtils.THRESHOLDS + [''] + ExperimentsUtils.THRESHOLDS
        self.file.write_row(row)

    def write_dataset_name(self, dataset_name):
        self.file.write_row(([dataset_name]))

    def write_filename(self, filename):
        self.file.write_row(['', filename])

    def write_col_name(self, col_name):
        self.file.write_row(['', '', col_name])

    def save_data_row(self, coder_name, windows, percentages, total_bits):
        data_row = {'coder_name': coder_name, 'windows': windows, 'percentages': percentages, 'total_bits': total_bits}
        self.data_rows.append(data_row)

    def write_data_rows(self):
        for row in self.data_rows:
            coder_name, windows,  = row['coder_name'], row['windows']
            percentages, total_bits = row['percentages'], row['total_bits']
            self.file.write_row(['', '', '', coder_name] + windows + [''] + percentages + [''] + total_bits)
        self.data_rows = []

    def write_row(self, row):
        self.file.write_row(row)

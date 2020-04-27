import sys
sys.path.append('.')

from file_utils.csv_utils.csv_writer import CSVWriter
from scripts.compress.experiments_utils import ExperimentsUtils


class Writer1(object):
    def __init__(self, path, extra_str):
        self.file = CSVWriter(path, extra_str + '-process1.csv')
        self.write_first_row()

    def write_first_row(self):
        row = ["Dataset", "Filename", "Column", "Coder"]
        row += ExperimentsUtils.THRESHOLDS + [''] + ExperimentsUtils.THRESHOLDS
        self.file.write_row(row)

    def write_dataset_name(self, dataset_name):
        self.file.write_row(([dataset_name]))

    def write_filename(self, filename):
        self.file.write_row(['', filename])

    def write_col_name(self, col_name):
        self.file.write_row(['', '', col_name])

    def write_data_row(self, coder_name, windows, percentages):
        self.file.write_row(['', '', '', coder_name] + windows + [''] + percentages)

    def write_row(self, row):
        self.file.write_row(row)

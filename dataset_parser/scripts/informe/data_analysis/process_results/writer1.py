import sys
sys.path.append('.')

from file_utils.csv_utils.csv_writer import CSVWriter
from scripts.compress.experiments_utils import ExperimentsUtils


class Writer1(object):
    @staticmethod
    def filename(path, extra_str):
        return CSVWriter(path, extra_str + '-process1.csv')

    @staticmethod
    def first_row():
        row = ["Dataset", "Filename", "Column", "Coder"]
        row += ExperimentsUtils.THRESHOLDS + [''] + ExperimentsUtils.THRESHOLDS
        return row
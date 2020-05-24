import sys
sys.path.append('.')

from file_utils.csv_utils.csv_writer import CSVWriter
from scripts.compress.experiments_utils import ExperimentsUtils

class Writer2(object):
    def __init__(self, path, extra_str):
        self.file = CSVWriter(path, extra_str + '-process2.csv')
        self.write_first_row()
        self.write_second_row()

    def write_first_row(self):
        row = ["Dataset", "Filename", "Column"] + Writer2.thresholds_array()
        self.file.write_row(row)

    def write_second_row(self):
        array = []
        for _ in ExperimentsUtils.THRESHOLDS:
            array += ["Coder", "Win", "CR (%)"]
        row = [None, None, None] + array
        self.file.write_row(row)

    def write_dataset_name(self, dataset_name):
        self.file.write_row(([dataset_name]))

    def write_filename(self, filename):
        self.file.write_row((['', filename]))

    def write_row(self, row):
        self.file.write_row(row)

    @staticmethod
    def thresholds_array():
        array = []
        for threshold in ExperimentsUtils.THRESHOLDS:
            array += [None, str(threshold) + " (%)", None]
        return array


import sys
sys.path.append('.')

from file_utils.csv_utils.csv_writer import CSVWriter
from scripts.compress.experiments_utils import ExperimentsUtils

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
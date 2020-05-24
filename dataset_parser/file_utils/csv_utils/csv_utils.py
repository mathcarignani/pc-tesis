import sys
sys.path.append('.')

from file_utils.csv_utils.csv_reader import CSVReader


class CSVUtils:
    def __init__(self):
        pass

    @classmethod
    def csv_row_count(cls, input_path, input_filename):
        csv = CSVReader(input_path, input_filename)
        csv.close()
        return csv.total_lines - 4

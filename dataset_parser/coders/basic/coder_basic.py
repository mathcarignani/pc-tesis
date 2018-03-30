import sys
sys.path.append('.')

from coders.coder_base import CoderBase


class CoderBasic(CoderBase):
    def __init__(self, input_csv, output_path, output_filename, *_):
        super(CoderBasic, self).__init__(input_csv, output_path, output_filename)
        self.row_count = 0

    def get_info(self):
        return "CoderBase"

    def _code_data_rows(self):
        while self.input_csv.continue_reading:
            row = self.input_csv.read_line()
            self._code_delta(row[0])
            self._code_data(row[1:])
            self.row_count += 1

    def _code_data(self, row):
        for col_index, value in enumerate(row):
            self.dataset.set_column(col_index)
            alphabet_value = self._csv_to_alphabet(value, self.row_count, col_index)
            self._code_raw(alphabet_value)

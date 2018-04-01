import sys
sys.path.append('.')

from coders.coder_base import CoderBase


class CoderBasic(CoderBase):
    def __init__(self, input_csv, output_path, output_filename, *_):
        super(CoderBasic, self).__init__(input_csv, output_path, output_filename)

    def get_info(self):
        return "CoderBase"

    def _code_data_rows(self):
        row_index = 0
        while self.input_csv.continue_reading:
            row = self.input_csv.read_line()
            self._code_row(row, row_index)
            row_index += 1

    def _code_row(self, row, row_index):
        for col_index, value in enumerate(row):
            self.dataset.set_column(col_index)
            self._code_value_raw(value, row_index, col_index)

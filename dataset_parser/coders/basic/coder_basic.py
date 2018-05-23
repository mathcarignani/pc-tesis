import sys
sys.path.append('.')

from coders.cols.coder_cols import CoderCols


class CoderBasic(CoderCols):
    def __init__(self, input_csv, output_path, output_filename, *_):
        super(CoderBasic, self).__init__(input_csv, output_path, output_filename, None, None)

    @classmethod
    def name(cls):
        return "CoderBasic"

    def get_info(self):
        return "CoderBase"

    def _code_column(self):
        row_index = 0
        self.input_csv.goto_row(4)  # first data row
        while self.input_csv.continue_reading:
            value = self.input_csv.read_line()[self.column_index]
            self._code_value_raw(value, row_index, self.column_index)
            row_index += 1

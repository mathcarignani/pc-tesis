import sys
sys.path.append('.')

from coders.cols.coder_cols import CoderCols
from coders.pca.window_fixed import WindowFixed


class CoderPCA(CoderCols):
    def __init__(self, input_csv, output_path, output_filename, params):
        super(CoderPCA, self).__init__(input_csv, output_path, output_filename, WindowFixed, params)

    @classmethod
    def name(cls):
        return "CoderPCA"

    def get_info(self):
        return "CoderPCA" +\
               ("\n-> error_threshold = %s" % self.params['error_threshold']) +\
               ("\n-> fixed_window_size = %s" % self.params['fixed_window_size'])

    def _code_column(self):
        window = self._create_window()
        row_index = 0
        self.input_csv.goto_row(4)  # first data row
        while self.input_csv.continue_reading:
            value = self.input_csv.read_line()[self.column_index]
            window.add_value_2_output(value)
            if window.is_full():
                self._code_window(window.add_2_output(), row_index)
            row_index += 1

        if not window.is_empty():
            self._code_window(window.add_2_output(), row_index)

    def _code_window(self, res, row_index):
        if isinstance(res, list):
            self.dataset.add_bits(1)  # count the bits
            self.output_file.write_bit(1)  # fi = 1
            for value in res:
                self._code_value_raw(value, row_index, self.column_index)
                # print "window", value
        else:
            self.dataset.add_bits(1)  # count the bits
            self.output_file.write_bit(0)  # fi = 0
            self._code_value_raw(res, row_index, self.column_index)
            # print "constant", res

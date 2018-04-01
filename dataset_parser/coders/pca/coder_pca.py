import sys
sys.path.append('.')

from coders.coder_base import CoderBase
from coders.pca.window_fixed import WindowFixed


class CoderPCA(CoderBase):
    def __init__(self, input_csv, output_path, output_filename, params):
        super(CoderPCA, self).__init__(input_csv, output_path, output_filename)
        self.params = params
        self.column_index = 0

    def get_info(self):
        return "CoderPCA" +\
               ("\n-> error_threshold = %s" % self.params['error_threshold']) +\
               ("\n-> fixed_window_size = %s" % self.params['fixed_window_size'])

    def _code_data_rows(self):
        # self.input_csv.previous_row is the row with the column names
        data_columns_count = len(self.input_csv.previous_row)
        for _ in xrange(data_columns_count):
            print 'code column_index', self.column_index
            self.dataset.set_column(self.column_index)
            self._code_column()
            self.column_index += 1

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
        self._code_window(window.add_2_output(), row_index)

    def _create_window(self):
        if self.column_index == 0:
            # error_threshold must be 0 because deltas must be compressed with a lossless algorithm
            params = {'error_threshold': 0, 'fixed_window_size': self.params['fixed_window_size']}
        else:
            params = self.params
        return WindowFixed(params)

    def _code_window(self, res, row_index):
        if isinstance(res, list):
            self.output_file.write_bit(1)  # fi = 1
            for value in res:
                self._code_value_raw(value, row_index, self.column_index)
        else:
            self.output_file.write_bit(0)  # fi = 0
            self._code_value_raw(res, row_index, self.column_index)

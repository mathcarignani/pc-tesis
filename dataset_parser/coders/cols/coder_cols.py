import sys
sys.path.append('.')

from coders.coder_base import CoderBase


class CoderCols(CoderBase):
    def __init__(self, input_csv, output_path, output_filename, window_cls, params):
        super(CoderCols, self).__init__(input_csv, output_path, output_filename)
        self.params = params
        self.column_index = 0
        self.window_cls = window_cls

    def _code_data_rows(self):
        # self.input_csv.previous_row is the row with the column names
        data_columns_count = len(self.input_csv.previous_row)
        for _ in xrange(data_columns_count):
            print 'code column_index', self.column_index
            self.dataset.set_column(self.column_index)
            self._code_column()
            self.column_index += 1

    def _code_column(self):
        raise NotImplementedError

    def _create_window(self):
        params = {k:v for k,v in self.params.items()}
        if self.column_index == 0:
            # error_threshold must be 0 because deltas must be compressed with a lossless algorithm
            params['error_threshold'] = 0
        return self.window_cls(params)

    ####################################################################################################################
    # CoderBase abstract methods
    ####################################################################################################################
    def get_info(self):
        raise NotImplementedError

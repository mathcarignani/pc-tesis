import sys
sys.path.append('../')

from coders.cols.coder_cols import CoderCols
from coders.apca.window_variable import WindowVariable
from coders.pwlh.linear_bucket import LinearBucket


class CoderPWLH(CoderCols):
    def __init__(self, input_csv, output_path, output_filename, params):
        super(CoderPWLH, self).__init__(input_csv, output_path, output_filename, WindowVariable, params)
        self.max_bucket_size = self.params['max_bucket_size'].bit_length()
        self.bucket = LinearBucket()

    def get_info(self):
        return "CoderPWLH" +\
               ("\n-> error_threshold = %s" % self.params['error_threshold']) +\
               ("\n-> max_bucket_size = %s" % self.params['max_bucket_size'])

    def _code_column(self):
        window = self._create_window()
        row_index = 0
        self.input_csv.goto_row(4)  # first data row
        while self.input_csv.continue_reading:
            value = self.input_csv.read_line()[self.column_index]
            pass

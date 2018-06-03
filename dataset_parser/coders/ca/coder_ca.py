import sys
sys.path.append('../')

from coders.cols.coder_cols import CoderCols
from coders.ca.window_ca import WindowCA


class CoderCA(CoderCols):
    def __init__(self, input_csv, output_path, output_filename, params):
        super(CoderCA, self).__init__(input_csv, output_path, output_filename, WindowCA, params)
        self.window_size_bit_length = self.params['max_window_size'].bit_length()

    def get_info(self):
        return "CoderCA" +\
               ("\n-> error_threshold = %s" % self.params['error_threshold']) +\
               ("\n-> max_window_size = %s" % self.params['max_window_size'])

    def _code_column(self):
        self.total = 0
        window = self._create_window()
        self.row_index = 0
        self.input_csv.goto_first_data_row()
        # if self.column_index != 6:
        #     return
        while self.input_csv.continue_reading:  # and self.row_index < 10:
            value = self.input_csv.read_line()[self.column_index]
            # print str(self.row_index) + " " + value
            # if self.column_index == 6 and 3860 < self.row_index < 3880:
            #     print '>>>>>>>>>>>>>>>>>>>>>>>>> row_index', self.row_index, 'value', value
            # window.print_state()
            window.code(value, self)
            self.row_index += 1
        # print self.row_index
        window.code(None, self)  # Force code

    def code_window(self, window_length, window_value):
        if window_length == 0:
            return
        # if self.column_index == 6 and 3860 < self.row_index < 3880:
        #     print 'window_length = %s, window_value = %s' % (window_length, window_value)
        self.total += window_length
        self.dataset.add_bits(self.window_size_bit_length)  # count the bits used for coding the window length
        self.output_file.write_int(window_length, self.window_size_bit_length)
        self._code_value_raw(window_value, self.row_index, self.column_index)

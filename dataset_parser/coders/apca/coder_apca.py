import sys
sys.path.append('../')

from coders.cols.coder_cols import CoderCols
from coders.apca.window_variable import WindowVariable


class CoderAPCA(CoderCols):
    def __init__(self, input_csv, output_path, output_filename, params):
        super(CoderAPCA, self).__init__(input_csv, output_path, output_filename, WindowVariable, params)
        self.window_size_bit_length = self.params['max_window_size'].bit_length()

    @classmethod
    def name(cls):
        return "CoderAPCA"

    def get_info(self):
        return "CoderAPCA" +\
               ("\n-> error_threshold = %s" % self.params['error_threshold']) +\
               ("\n-> max_window_size = %s" % self.params['max_window_size'])

    def _code_column(self):
        window = self._create_window()
        row_index = 0
        self.input_csv.goto_first_data_row()
        while self.input_csv.continue_reading:
            value = self.input_csv.read_line()[self.column_index]
            if not window.condition_holds(value):
                self._code_window(window, row_index)
                window.clear(value)
            row_index += 1
        if not window.is_empty():
            self._code_window(window, row_index)

    def _code_window(self, window, row_index):
        self.dataset.add_bits(self.window_size_bit_length)  # count the bits used for coding the window length
        self.output_file.write_int(window.current_window_length, self.window_size_bit_length)
        self._code_value_raw(window.constant, row_index, self.column_index)

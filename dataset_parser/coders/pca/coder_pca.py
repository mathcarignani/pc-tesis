from .. import coder_base
from pca import PCA


class CoderPCA(coder_base.CoderBase, PCA):
    def __init__(self, parser, input_csv, output_path, output_filename, params={}):
        super(CoderPCA, self).__init__(parser, input_csv, output_path, output_filename)
        PCA.__init__(self, parser.NONE, params)

    def get_info(self):
        return "CODER: CoderPCA" +\
               ("\n-> error_threshold = %s" % self.error_threshold) +\
               ("\n-> fixed_window_size = %s" % self.fixed_window_size)

    def code_file(self):
        self.unprocessed_rows = []
        while self.input_csv.continue_reading:
            row = self.input_csv.read_line()
            self._code_row(row)
            self.count += 1

    def _code_row(self, row):
        self.parser.check_delta(row[0])
        self.unprocessed_rows.append(row[1:])
        if self.count % self.fixed_window_size == self.fixed_window_size - 1:
            self._code_unprocessed_rows()
            self.unprocessed_rows = []

    def _code_unprocessed_rows(self):
        windows = map(list, zip(*self.unprocessed_rows))
        for window in windows:
            self._code_window(window)

    def _code_window(self, window):
        condition_holds = True
        for value in window:
            alphabet_value = self.parser.csv_to_alphabet(value)
            if not condition_holds:
                self._code_raw(alphabet_value)
            elif self.window.condition_holds(alphabet_value):
                if self.window.full():
                    self._code_window_complete()
            else:
                condition_holds = False
                self._code_window_incomplete()
                self._code_raw(alphabet_value)
        self.window.clear()

    def _code_window_complete(self):
        self.output_file.write_bit(0)  # fi = 0
        self._code_raw(self.window.constant())

    def _code_window_incomplete(self):
        self.output_file.write_bit(1)  # fi = 1
        for value in self.window.array:
            self._code_raw(value)

# OLD CODE:
#
# class CoderPCA(coder_base.CoderBase, PCA):
#     def __init__(self, input_path, input_filename, output_path, output_filename, params):
#         super(CoderPCA, self).__init__(input_path, input_filename, output_path, output_filename)
#         PCA.__init__(self, params)
#
#     def _code(self, value):
#         value = self._map_value(value)
#         if self.window.condition_holds(value):
#             if self.window.full():
#                 self._code_window()
#                 self.window.clear()
#         else:
#             self._code_window_incomplete()
#             self.window.clear()
#             self.window.condition_holds(value)
#
#     def _map_value(self, value):
#         value = None if value == self.nodata else value
#         return value
#
#     def _code_window(self):
#         self.output_file.write_bit(0)  # fi = 0
#         self._code_value(self.window.constant())
#
#     def _code_window_incomplete(self):
#         for value in self.window.array:
#             self.output_file.write_bit(1)  # fi = 1
#             self._code_value(value)
#
#     def _code_value(self, value):
#         if value is None:
#             self.output_file.write_bit(1)  # nodata = 1
#         else:
#             self.output_file.write_bit(0)  # nodata = 0
#             self._code_raw(value)

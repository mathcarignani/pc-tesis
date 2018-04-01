import sys
sys.path.append('.')

from coders.decoder_base import DecoderBase


class DecoderPCA(DecoderBase):
    def __init__(self, input_path, input_filename, output_csv, params):
        super(DecoderPCA, self).__init__(input_path, input_filename, output_csv)
        self.fixed_window_size = params['fixed_window_size']
        self.row_index = None
        self.column_index = 0
        self.column = None

    def _decode_data_rows(self):
        columns = []
        for _ in xrange(self.data_columns_count):
            print 'decode column_index', self.column_index
            self.dataset.set_column(self.column_index)
            self._decode_column()
            columns.append(self.column)
            self.column_index += 1

        rows = map(list, zip(*columns))  # transpose list of lists https://stackoverflow.com/a/6473724/4547232
        for row in rows:
            self.output_csv.write_row(row)

    def _decode_column(self):
        self.row_index, self.column = 0, []

        while self.data_rows_count - self.row_index >= self.fixed_window_size:
            self._decode_window(self.fixed_window_size)

        unprocessed_rows = self.data_rows_count - self.row_index
        if unprocessed_rows > 0:
            self._decode_window(unprocessed_rows)

    def _decode_window(self, window_size):
        window = []
        fi = self.input_file.read_bit()
        if fi:
            for _ in xrange(window_size):
                value = self._decode_value_raw(self.row_index, self.column_index)
                window.append(value)
                self.row_index += 1
        else:
            constant = self._decode_value_raw(self.row_index, self.column_index)
            window = [constant] * window_size
            self.row_index += window_size
        self.column.extend(window)

# class DecoderPCA(decoder_base.DecoderBase):
#     def __init__(self, parser, input_path, input_filename, output_csv, row_length, params):
#         super(DecoderPCA, self).__init__(parser, input_path, input_filename, output_csv, row_length)
#         # PCA.__init__(self, self.parser.NONE, params)
#         self.current_column = 0  # between 0 and row_length - 1
#         self.window_matrix = []
#
#     def _decode(self):
#         module = self.count % self.fixed_window_size
#         if module == 0:
#             self.window_matrix.append(self._decode_window())
#         value = self.window_matrix[self.current_column][module]
#         self.current_column += 1
#         if self.current_column == self.row_length:
#             self.current_column = 0
#             if module + 1 == self.fixed_window_size:
#                 self.window_matrix = []
#         return self.parser.alphabet_to_csv(value)
#
#     def _decode_window(self):
#         fi = self.input_file.read_bit()
#         if fi == 0:
#             return self._decode_window_complete()
#         else:  # fi == 1
#             return self._decode_window_incomplete()
#
#     def _decode_window_complete(self):
#         csv_value = self._decode_raw()
#         return [csv_value] * self.fixed_window_size
#
#     def _decode_window_incomplete(self):
#         array = []
#         for _ in xrange(self.fixed_window_size):
#             array.append(self._decode_raw())
#         return array

    #
    # def _new_window(self, count, value):
    #     self.window = {'count': count, 'value': value}
    #
    # # PRE: self.window['count'] > 0
    # def _window_value(self):
    #     self.window['count'] -= 1
    #     return self.window['value']
    #
    # def _decode_value(self):
    #     nodata = self.input_file.read_bit()
    #     if nodata == 1:
    #         return self.nodata
    #     else:  # nodata == 0
    #         return self._decode_raw()

# OLD CODE:
#
# class DecoderPCA(decoder_base.DecoderBase, PCA):
#     def __init__(self, input_path, input_filename, output_path, output_filename, params):
#         super(DecoderPCA, self).__init__(input_path, input_filename, output_path, output_filename)
#         PCA.__init__(self, params)
#         self._new_window(0, None)
#
#     def _decode(self):
#         if self.window['count'] > 0:
#             return self._window_value()
#         else:
#             fi = self.input_file.read_bit()
#             value = self._decode_value()
#             if fi == 0:
#                 self._new_window(self.fixed_window_size, value)
#                 return self._window_value()
#
#             else:  # fi == 1
#                 return value
#
#     def _new_window(self, count, value):
#         self.window = {'count': count, 'value': value}
#
#     # PRE: self.window['count'] > 0
#     def _window_value(self):
#         self.window['count'] -= 1
#         return self.window['value']
#
#     def _decode_value(self):
#         nodata = self.input_file.read_bit()
#         if nodata == 1:
#             return self.nodata
#         else:  # nodata == 0
#             return self._decode_raw()

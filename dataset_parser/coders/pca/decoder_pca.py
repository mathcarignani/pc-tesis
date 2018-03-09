from .. import decoder_base
from pca import PCA


class DecoderPCA(decoder_base.DecoderBase, PCA):
    def __init__(self, parser, input_path, input_filename, output_csv, row_length, params):
        super(DecoderPCA, self).__init__(parser, input_path, input_filename, output_csv, row_length)
        PCA.__init__(self, self.parser.NONE, params)
        self.current_column = 0  # between 0 and row_length - 1
        self.window_matrix = []

    def _decode(self):
        module = self.count % self.fixed_window_size
        if module == 0:
            self.window_matrix.append(self._decode_window())
        value = self.window_matrix[self.current_column][module]
        self.current_column += 1
        if self.current_column == self.row_length:
            self.current_column = 0
            if module + 1 == self.fixed_window_size:
                self.window_matrix = []
        return self.parser.alphabet_to_csv(value)

    def _decode_window(self):
        fi = self.input_file.read_bit()
        if fi == 0:
            return self._decode_window_complete()
        else:  # fi == 1
            return self._decode_window_incomplete()

    def _decode_window_complete(self):
        csv_value = self._decode_raw()
        return [csv_value] * self.fixed_window_size

    def _decode_window_incomplete(self):
        array = []
        for _ in xrange(self.fixed_window_size):
            array.append(self._decode_raw())
        return array

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

import sys
sys.path.append('../')

from coders.cols.decoder_cols import DecoderCols


class DecoderAPCA(DecoderCols):
    def __init__(self, input_path, input_filename, output_csv, params):
        super(DecoderAPCA, self).__init__(input_path, input_filename, output_csv)
        self.window_size_bit_length = params['max_window_size'].bit_length()

    def _decode_column(self):
        self.row_index, self.column = 0, []

        while self.row_index < self.data_rows_count:
            window_length, value = self._decode_window()
            window = [value] * window_length
            self.column.extend(window)
            self.row_index += window_length

        return self.column

    def _decode_window(self, _=None):
        window_length = self.input_file.read_int(self.window_size_bit_length)
        value = self._decode_value_raw(self.row_index, self.column_index)
        return [window_length, value]

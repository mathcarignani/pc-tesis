import sys
sys.path.append('.')

from coders.cols.decoder_cols import DecoderCols


class DecoderPCA(DecoderCols):
    def __init__(self, input_path, input_filename, output_csv, params):
        super(DecoderPCA, self).__init__(input_path, input_filename, output_csv)
        self.fixed_window_size = params['fixed_window_size']

    def _decode_column(self):
        self.row_index, self.column = 0, []

        while self.data_rows_count - self.row_index >= self.fixed_window_size:
            self._decode_window(self.fixed_window_size)

        unprocessed_rows = self.data_rows_count - self.row_index
        if unprocessed_rows > 0:
            self._decode_window(unprocessed_rows)
        return self.column

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

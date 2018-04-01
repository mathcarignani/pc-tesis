import sys
sys.path.append('.')

from coders.decoder_base import DecoderBase


class DecoderBasic(DecoderBase):
    def __init__(self, input_path, input_filename, output_csv, *_):
        super(DecoderBasic, self).__init__(input_path, input_filename, output_csv)

    def _decode_data_rows(self):
        row_index = 0
        row, col_index = [], 0  # col_index is always the same as len(row)
        while self.input_file.continue_reading:  # and count < 20:
            row, col_index = self._decode_row(row_index, row, col_index)
            row_index += 1

    def _decode_row(self, row_index, row, col_index):
        self.dataset.set_column(col_index)
        value = self._decode_value_raw(row_index, col_index)
        row.append(value)
        col_index += 1
        if col_index == self.data_columns_count + 1:
            self.output_csv.write_row(row)
            row, col_index = [], 0
        return [row, col_index]

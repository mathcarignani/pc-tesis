import sys
sys.path.append('.')

from coders.cols.decoder_cols import DecoderCols


class DecoderBasic(DecoderCols):
    def __init__(self, input_path, input_filename, output_csv, *_):
        super(DecoderBasic, self).__init__(input_path, input_filename, output_csv)

    def _decode_column(self):
        row_index, column = 0, []
        while row_index < self.data_rows_count:
            value = self._decode_value_raw(row_index, self.column_index)
            column.append(value)
            row_index += 1
        return column
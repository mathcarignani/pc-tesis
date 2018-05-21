import sys
sys.path.append('.')

from coders.decoder_base import DecoderBase


class DecoderCols(DecoderBase):
    def __init__(self, input_path, input_filename, output_csv):
        super(DecoderCols, self).__init__(input_path, input_filename, output_csv)
        self.column_index = 0

    def _decode_data_rows(self):
        columns = []
        for _ in xrange(self.data_columns_count + 1):
            print 'decode column_index', self.column_index
            self.dataset.set_column(self.column_index)
            column = self._decode_column()
            columns.append(column)
            self.column_index += 1

        rows = map(list, zip(*columns))  # transpose list of lists https://stackoverflow.com/a/6473724/4547232
        for row in rows:
            self.output_csv.write_row(row)

    def _decode_column(self):
        raise NotImplementedError

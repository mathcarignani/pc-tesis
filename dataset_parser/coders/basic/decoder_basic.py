import sys
sys.path.append('.')

from coders.decoder_base import DecoderBase


class DecoderBasic(DecoderBase):
    def __init__(self, input_path, input_filename, output_csv, *_):
        super(DecoderBasic, self).__init__(input_path, input_filename, output_csv)
        self.row_count = 0  # This variable is not necessary but it is useful for debugging
        self.row = []

    def _decode_data_rows(self):
        while self.input_file.continue_reading:  # and count < 20:
            if len(self.row) == 0:
                decoded_delta = self._decode_delta()
                self.row.append(decoded_delta)
            else:
                decoded_val = self._decode_data()
                self.row.append(decoded_val)
                if len(self.row) == self.columns_count + 1:
                    self.output_csv.write_row(self.row)
                    self.row_count += 1
                    self.row = []

    def _decode_data(self):
        self.dataset.set_column(len(self.row) - 1)
        value = self._decode_raw()
        return self._alphabet_to_csv(value)

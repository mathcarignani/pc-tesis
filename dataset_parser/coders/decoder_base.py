import sys
sys.path.append('../')

from coders.coder_base import CoderBase
from coders.header_utils import HeaderUtils
from file_utils.bit_stream.bit_stream_reader import BitStreamReader


class DecoderBase(object):
    def __init__(self, input_path, input_filename, output_csv, *_):
        self.input_file = BitStreamReader(input_path, input_filename)
        self.output_csv = output_csv
        self.dataset = None  # Dataset object
        self.columns_count = None
        self.row = []

    def decode_file(self):
        self.dataset, self.columns_count = HeaderUtils.decode_header(self.input_file, self.output_csv)
        self._decode_data_rows()

    def close(self):
        self.input_file.close()
        self.output_csv.close()

    ####################################################################################################################

    def _decode_data_rows(self):
        count = 0  # TODO: count variable is not necessary but it is useful for debugging
        while self.input_file.continue_reading:  # and count < 20:
            decoded_val = self._decode_delta() if len(self.row) == 0 else self._decode_data()
            self.row.append(decoded_val)
            if len(self.row) == self.columns_count + 1:
                self.output_csv.write_row(self.row)
                count += 1
                self.row = []

    def _decode_delta(self):
        return self.input_file.read_int(CoderBase.DELTA_BITS)

    def _decode_data(self):
        self.dataset.set_column(len(self.row) - 1)
        value = self._decode_raw()
        return self._alphabet_to_csv(value)

    def _alphabet_to_csv(self, y):
        if y == self.dataset.nan:
            return 'N'
        else:
            y -= self.dataset.offset
            if self.dataset.min <= y <= self.dataset.max:
                return y
            else:
                raise StandardError("Invalid value in the alphabet = %s" % y)

    def _decode_raw(self):
        return self.input_file.read_int(self.dataset.bits)

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
        self.data_columns_count = None
        self.data_rows_count = None

    def decode_file(self):
        self.dataset, self.data_columns_count = HeaderUtils.decode_header(self.input_file, self.output_csv)
        self._decode_data_rows_count()
        self._decode_data_rows()

    def close(self):
        self.input_file.close()
        self.output_csv.close()

    ####################################################################################################################

    def _decode_data_rows_count(self):
        self.data_rows_count = self.input_file.read_int(24)  # 24 bits for the data rows count

    def _decode_data_rows(self):
        raise NotImplementedError

    # def _alphabet_to_csv(self, y, row_index, col_index):
    def _decode_value(self, y, row_index, col_index):
        if y == self.dataset.nan:
            return 'N'

        y -= self.dataset.offset
        if self.dataset.min <= y <= self.dataset.max:
            return y

        CoderBase.raise_range_error(self.dataset.min, self.dataset.max, y, row_index, col_index)

    def _decode_raw(self):
        return self.input_file.read_int(self.dataset.bits)

    def _decode_value_raw(self, row_index, col_index):
        value = self._decode_raw()
        return self._decode_value(value, row_index, col_index)

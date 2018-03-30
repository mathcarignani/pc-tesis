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

    def decode_file(self):
        self.dataset, self.columns_count = HeaderUtils.decode_header(self.input_file, self.output_csv)
        self._decode_data_rows()

    def close(self):
        self.input_file.close()
        self.output_csv.close()

    ####################################################################################################################

    def _decode_data_rows(self):
        raise NotImplementedError

    def _decode_delta(self):
        return self.input_file.read_int(CoderBase.DELTA_BITS)

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

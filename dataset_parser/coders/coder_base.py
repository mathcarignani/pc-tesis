import sys
sys.path.append('../')

from coders.header_utils import HeaderUtils
from file_utils.bit_stream.bit_stream_writer import BitStreamWriter


class CoderBase(object):
    DELTA_BITS = 17

    def __init__(self, input_csv, output_path, output_filename, *_):
        self.input_csv = input_csv
        self.output_file = BitStreamWriter(output_path, output_filename)
        self.count = 0

    @classmethod
    def get_info(cls):
        return "CoderBase"

    def code_file(self):
        self.dataset = HeaderUtils.code_header(self.input_csv, self.output_file)
        self._code_data_rows()

    def close(self):
        self.input_csv.close()
        self.output_file.close()

    ####################################################################################################################

    def _code_data_rows(self):
        while self.input_csv.continue_reading:
            row = self.input_csv.read_line()
            self._code_delta(row[0])
            self._code_data(row[1:])
            self.count += 1

    def _code_delta(self, delta):
        int_delta = int(delta)
        if int_delta >= 2**self.DELTA_BITS:
            raise StandardError("delta cannot be >= 2**%s and delta=%s" % (str(self.DELTA_BITS), str(int_delta)))
        self.output_file.write_int(int_delta, self.DELTA_BITS)

    def _code_data(self, row):
        for value in row:
            alphabet_value = self._csv_to_alphabet(value)
            self._code_raw(alphabet_value)

    def _csv_to_alphabet(self, x):
        if x == 'N':
            return self.dataset.nan
        else:
            x = int(x)
            if self.dataset.min <= x <= self.dataset.max:
                return x + self.dataset.offset
            else:
                raise StandardError("Invalid value in the csv = %s. line = %s" % (x, self.count))

    def _code_raw(self, value):
        self.output_file.write_int(value, self.dataset.bits)

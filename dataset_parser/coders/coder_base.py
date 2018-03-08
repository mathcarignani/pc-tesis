import sys
sys.path.append('../')

from file_utils.bit_stream.bit_stream_writer import BitStreamWriter


class CoderBase(object):
    def __init__(self, parser, input_csv, output_path, output_filename):
        self.parser = parser
        self.input_csv = input_csv
        self.output_file = BitStreamWriter(output_path, output_filename)
        self.count = 0

    def code_file(self):
        while self.input_csv.continue_reading:
            row = self.input_csv.read_line()
            self._code_row(row)
            self.count += 1

    def _code_row(self, row):
        self.parser.check_delta(row[0])
        for value in row[1:]:
            coded_value = self.parser.code_value(value)
            self._code_raw(coded_value, self.parser.BITS)

    def _code_raw(self, value, bits):
        self.output_file.write_int(value, bits)

    def close(self):
        self.input_csv.close()
        self.output_file.close()

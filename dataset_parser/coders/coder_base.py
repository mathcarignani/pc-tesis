import sys
sys.path.append('../')

from file_utils.bit_stream import BitStreamWriter
from file_utils.text_utils.text_file_reader import TextFileReader


class CoderBase(object):
    def __init__(self, input_path, input_filename, output_path, output_filename, params={}):
        self.bit_count = params.get('bit_count') or 24
        self.nodata = params.get('nodata') or 'nodata'
        self.input_file = TextFileReader(input_path, input_filename)
        self.output_file = BitStreamWriter(output_path, output_filename)
        self.count = 0

    def code_file(self):
        while self.input_file.continue_reading:
            line = self.input_file.read_line()
            value = line.rstrip('\n')
            value = value if value == self.nodata else int(value)
            self._code(value)
            self.count += 1

    def _code(self, value):
        value = 0 if value == self.nodata else value
        self._code_raw(value)

    def _code_raw(self, value):
        self.output_file.write_int(value, self.bit_count)

    def close(self):
        self.input_file.close()
        self.output_file.close()

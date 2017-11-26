import sys
sys.path.append('../')

from bit_stream.bit_stream_writer import BitStreamWriter
from file_utils.file_reader import FileReader
from parsers.irkis.parser_vwc import ParserVWC


class CoderBase(object):
    def __init__(self, input_path, input_filename, output_path, output_filename):
        self.NO_DATA = '-999.000000'
        self.input_file = FileReader(input_path, input_filename)
        self.output_file = BitStreamWriter(output_path, output_filename)
        self.parser = ParserVWC()
        self.count = 0

    def code_file(self):
        while self.input_file.continue_reading and self.count < 20:
            line = self.input_file.read_line()
            parsing_header = self.parser.parsing_header
            data = self.parser.parse_line(line)
            if not parsing_header and data[0] != '-999.000000':
                self._code(data[0])
                self.count += 1
                # print value

    def _code(self, value):
        if value == self.NO_DATA:
            self.output_file.write_int(0, 24)
        else:
            print value
            value = float(value) * 1000000
            value = int(value)
            self.output_file.write_int(value, 24)

    def close(self):
        self.input_file.close()
        self.output_file.close()

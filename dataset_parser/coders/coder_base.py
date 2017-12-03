import sys
sys.path.append('../')

from bit_stream.bit_stream_writer import BitStreamWriter
from file_utils.file_reader import FileReader
# from parsers.irkis.parser_vwc import ParserVWC


class CoderBase(object):
    def __init__(self, input_path, input_filename, output_path, output_filename, params={}):
        self.input_file = FileReader(input_path, input_filename)
        self.output_file = BitStreamWriter(output_path, output_filename)
        self.count = 0
        self.NO_DATA = 'nodata'

    def code_file(self):
        while self.input_file.continue_reading:
            line = self.input_file.read_line()
            value = line.rstrip('\n')
            value = value if value == self.NO_DATA else int(value)
            self._code(value)
            self.count += 1

    def _code(self, value):
        value = 0 if value == self.NO_DATA else value
        self._code_raw(value)

    def _code_raw(self, value):
        self.output_file.write_int(value, 24)

    def close(self):
        self.input_file.close()
        self.output_file.close()

    # def code_file_parser(self):
    #     self.NO_DATA = '-999.000000'
    #     self.parser = ParserVWC()
    #
    #     while self.input_file.continue_reading and self.count < 20:
    #         line = self.input_file.read_line()
    #         parsing_header = self.parser.parsing_header
    #         data = self.parser.parse_line(line)
    #         if not parsing_header and data[0] != '-999.000000':
    #             self._code(data[0])
    #             self.count += 1
    #             # print value

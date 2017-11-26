import sys
sys.path.append('../')

from bit_stream.bit_stream_reader import BitStreamReader
from file_utils.file_writer import FileWriter


class DecoderBase(object):
    def __init__(self, input_path, input_filename, output_path, output_filename):
        self.NO_DATA = '-999.000000'
        self.input_file = BitStreamReader(input_path, input_filename)
        self.output_file = FileWriter(output_path, output_filename)
        self.count = 0

    def decode_file(self):
        while self.input_file.continue_reading and self.count < 20:
            decoded_val = self._decode()
            print decoded_val, '\n'
            self.output_file.write_line(str(decoded_val))
            self.count += 1

    def _decode(self):
        value = self.input_file.read_int(24)
        if value == 0:
            return self.NO_DATA
        else:
            return value

    def close(self):
        self.input_file.close()
        self.output_file.close()

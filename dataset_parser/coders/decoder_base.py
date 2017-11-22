import sys
sys.path.append('../')

from bit_stream.bit_stream_reader import BitStreamReader
from file_utils.file_writer import FileWriter


class DecoderBase(object):
    def __init__(self, input_path, input_filename, output_path, output_filename):
        self.input_file = BitStreamReader(input_path, input_filename)
        self.output_file = FileWriter(output_path, output_filename)
        self.count = 0

    def decode(self):
        while self.input_file.continue_reading and self.count < 50:
            decoded_val = self.input_file.read_int(24)
            self.output_file.write_line(str(decoded_val))

    def close(self):
        self.input_file.close()
        self.output_file.close()

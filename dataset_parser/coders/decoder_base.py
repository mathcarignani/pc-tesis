import sys
sys.path.append('../')

from file_utils.bit_stream import BitStreamReader
from file_utils.text_utils.file_writer import FileWriter


class DecoderBase(object):
    def __init__(self, input_path, input_filename, output_path, output_filename, params={}):
        self.bit_count = params.get('bit_count') or 24
        self.nodata = 'nodata'
        self.input_file = BitStreamReader(input_path, input_filename)
        self.output_file = FileWriter(output_path, output_filename)
        self.count = 0

    def decode_file(self):
        while self.input_file.continue_reading: # and self.count < 20:
            decoded_val = self._decode()
            # print 'deco', self.count, decoded_val
            self.output_file.write_line(str(decoded_val))
            self.count += 1

    def _decode(self):
        value = self._decode_raw()
        value = self.nodata if value == 0 else value
        return value

    def _decode_raw(self):
        return self.input_file.read_int(self.bit_count)

    def close(self):
        self.input_file.close()
        self.output_file.close()

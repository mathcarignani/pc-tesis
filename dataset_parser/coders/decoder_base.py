import sys
sys.path.append('../')

from file_utils.bit_stream.bit_stream_reader import BitStreamReader


class DecoderBase(object):
    def __init__(self, parser, input_path, input_filename, output_csv, row_length):
        self.parser = parser
        self.input_file = BitStreamReader(input_path, input_filename)
        self.output_csv = output_csv
        self.count = 0
        self.row = []
        self.row_length = row_length

    def decode_file(self):
        while self.input_file.continue_reading:  # and self.count < 20:
            decoded_val = self._decode()
            self.row.append(decoded_val)
            if len(self.row) == self.row_length:
                self.output_csv.write_row([self.parser.DELTA] + self.row)
                self.count += 1
                self.row = []

    def _decode_raw(self):
        return self.input_file.read_int(self.parser.BITS)

    def close(self):
        self.input_file.close()
        self.output_csv.close()

    ####################################################################################################################

    def _decode(self):
        value = self._decode_raw()
        return self.parser.alphabet_to_csv(value)

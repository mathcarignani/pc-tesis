import sys
sys.path.append('../')

from aux.dataset_utils import DatasetUtils
from file_utils.bit_stream.bit_stream_reader import BitStreamReader


class DecoderBase(object):
    def __init__(self, parser, input_path, input_filename, output_csv, *_):
        self.parser = parser
        self.input_file = BitStreamReader(input_path, input_filename)
        self.output_csv = output_csv
        self.count = 0
        self.row = []

    def decode_file(self):
        self._decode_header()
        self._decode_data_rows()

    def close(self):
        self.input_file.close()
        self.output_csv.close()

    ####################################################################################################################

    def _decode_header(self):
        coded_dataset = self.input_file.read_int(4)  # 4 bits for the dataset name
        coded_time_unit = self.input_file.read_int(4)  # 4 bits for the time unit

        dataset_utils = DatasetUtils('decode')
        dataset = dataset_utils.dataset_value(coded_dataset)
        self.output_csv.write_row(['DATASET:', dataset])

        time_unit = dataset_utils.time_unit_value(coded_time_unit)
        self.output_csv.write_row(['TIME UNIT:', time_unit])

        pass

    def _decode_data_rows(self):
        while self.input_file.continue_reading:  # and self.count < 20:
            decoded_val = self._decode()
            self.row.append(decoded_val)
            if len(self.row) == 55:
                self.output_csv.write_row([self.parser.DELTA] + self.row)
                self.count += 1
                self.row = []

    def _decode(self):
        value = self._decode_raw()
        return self.parser.alphabet_to_csv(value)

    def _decode_raw(self):
        return self.input_file.read_int(self.parser.BITS)

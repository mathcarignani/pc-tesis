import sys
sys.path.append('../')

from aux.dataset_utils import DatasetUtils
from file_utils.bit_stream.bit_stream_writer import BitStreamWriter


class CoderBase(object):
    def __init__(self, parser, input_csv, output_path, output_filename, *_):
        self.parser = parser
        self.input_csv = input_csv
        self.output_file = BitStreamWriter(output_path, output_filename)
        self.count = 0

    @classmethod
    def get_info(cls):
        return "CoderBase"

    def code_file(self):
        self._code_header()
        self._code_data_rows()

    def close(self):
        self.input_csv.close()
        self.output_file.close()

    ####################################################################################################################

    def _code_header(self):
        dataset = self.input_csv.read_line()[1]
        time_unit = self.input_csv.read_line()[1]
        timestamp = self.input_csv.read_line()[1]
        column_names = self.input_csv.read_line()

        dataset_utils = DatasetUtils('code')
        print "dataset", dataset_utils.dataset_value(dataset)
        self.output_file.write_int(dataset_utils.dataset_value(dataset), 4)  # 4 bits for the dataset name

        print "time_unit", dataset_utils.time_unit_value(time_unit)
        self.output_file.write_int(dataset_utils.time_unit_value(time_unit), 4)  # 4 bits for the time unit

        pass

    def _code_data_rows(self):
        while self.input_csv.continue_reading:
            row = self.input_csv.read_line()
            self._code_row(row)
            self.count += 1

    def _code_row(self, row):
        self.parser.check_delta(row[0])
        for value in row[1:]:
            alphabet_value = self.parser.csv_to_alphabet(value)
            self._code_raw(alphabet_value)

    def _code_raw(self, value):
        self.output_file.write_int(value, self.parser.BITS)



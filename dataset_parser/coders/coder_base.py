import sys
sys.path.append('../')

from coders.header_utils import HeaderUtils
from file_utils.bit_stream.bit_stream_writer import BitStreamWriter


class CoderBase(object):
    def __init__(self, input_csv, output_path, output_filename, *_):
        self.input_csv = input_csv
        self.output_file = BitStreamWriter(output_path, output_filename)
        self.dataset = None  # Dataset object

    def get_info(self):
        raise NotImplementedError

    def code_file(self):
        self.dataset = HeaderUtils.code_header(self.input_csv, self.output_file)
        self._code_data_rows_count()
        self._code_data_rows()

    def close(self):
        self.input_csv.close()
        self.output_file.close()

    ####################################################################################################################

    def _code_data_rows_count(self):
        data_rows_count = self.input_csv.total_lines - 4
        self.output_file.write_int(data_rows_count, 24)  # 24 bits for the data rows count

    def _code_data_rows(self):
        raise NotImplementedError

    #
    # This method maps a value read in the csv file into an integer to be written in the output file.
    # It also checks the minimum and maximum constraints.
    #
    def _code_value(self, x, row_index, col_index):
        if x == 'N':
            return self.dataset.nan

        x = int(x)
        if self.dataset.min <= x <= self.dataset.max:
            return x + self.dataset.offset

        CoderBase.raise_range_error(self.dataset.min, self.dataset.max, x, row_index, col_index)

    def _code_raw(self, value):
        self.output_file.write_int(value, self.dataset.get_bits())

    def _code_value_raw(self, x, row_index, col_index):
        # print "codeValue(x) = " + str(x)
        value = self._code_value(x, row_index, col_index)
        return self._code_raw(value)

    ####################################################################################################################

    #
    # TODO: move this code to a utils module
    #
    @classmethod
    def raise_range_error(cls, minimum, maximum, x, row_index, col_index):
        error_str = ("ERROR: min = %s <= x = %s <= max = %s\n" % (minimum, x, maximum)) +\
                    ("POSITION = [%s,%s]" % (row_index, col_index))
        raise StandardError(error_str)

import sys
sys.path.append('.')

from file_utils.csv_utils.csv_reader import CSVReader
from pandas_tools.pandas_tools import PandasTools


class CSVCompare:
    def __init__(self, file1_path, file1_filename, file2_path, file2_filename):
        self.file1 = CSVReader(file1_path, file1_filename)
        self.file2 = CSVReader(file2_path, file2_filename)

        self.file1_first_data_row = CSVReader.first_data_row(file1_path, file1_filename)
        self.file2_first_data_row = CSVReader.first_data_row(file2_path, file2_filename)

        assert(self.file1_first_data_row == self.file2_first_data_row)

    #
    # error_thresholds is an array with the the maximum difference between the original and the compressed values
    # in a near-lossless compression schema.
    # If error_thresholds is None then we consider a lossless compression schema.
    #
    # if abort is True then the comparison stops as soon as an error is found.
    #
    # Returns True iff there is no error.
    #
    def compare(self, error_thresholds=None, abort=True):
        self.error_thresholds = self._check_error_thresholds(error_thresholds)
        self.abort = abort
        same_file = self._check_same_file()
        self._print_result(same_file)
        return same_file

    ####################################################################################################################

    @classmethod
    def _check_error_thresholds(cls, error_thresholds):
        if error_thresholds is not None:
            for error in error_thresholds:
                assert(error == PandasTools.NO_DATA or (isinstance(error, int) and error >= 0))
        return error_thresholds

    def _get_threshold(self, col_index):
        if self.error_thresholds is None:
           return 0
        error_thresholds_len = len(self.error_thresholds)
        assert(col_index < error_thresholds_len)
        return self.error_thresholds[col_index]
        # else:  # GAMPS coder
        #     data_columns_group_count = len(self.error_thresholds) - 1
        #     if data_columns_group_count == 1:
        #         index = 1
        #     else:
        #         index = col_index % data_columns_group_count
        #         index = data_columns_group_count if index == 0 else index
        #     return self.error_thresholds[index]

    def _print_result(self, same_file):
        if same_file:
            print("SAME FILES!")
        else:
            print("DIFFERENT FILES!")
        if self.error_thresholds is None:
            print("Compared with all thresholds = 0.")
        else:
            print("Compared with thresholds = ", self.error_thresholds)

    def _check_same_file(self):
        same_file = True
        continue_while = True
        self.row_count = 0

        while continue_while and self.file1.continue_reading and self.file2.continue_reading:
            row1, row2 = self.file1.read_line(), self.file2.read_line()
            if self.row_count < self.file1_first_data_row + 1:
                same_file = self._compare_header_rows(row1, row2)
                continue_while = same_file  # if there is a mismatch in the header rows, exit the while
            else:
                same_row = self._compare_data_rows(row1, row2)
                if not same_row:
                    same_file = False
                    # if there is a mismatch in the data rows, exit or not depending on the self.abort flag
                    if self.abort:
                        continue_while = False

            self.row_count += 1

        if self._only_one_file_ends():
            same_file = False

        return same_file

    @classmethod
    def _compare_header_rows(cls, row1, row2):
        if row1 == row2:
            return True
        # the non-data rows must match exactly
        print("Difference in the header rows")
        print(row1)
        print(row2)
        return False

    #
    # Returns False iff:
    # - the length of the rows does not match.
    # OR
    # - the error_threshold constraint does not hold.
    #
    def _compare_data_rows(self, row1, row2):
        if len(row1) != len(row2):
            print("len(row1) = %s != %s = len(row2)" % (len(row1), len(row2)))
            return False

        same_row = True
        for col_index in range(len(row1)):
            value1, value2 = row1[col_index], row2[col_index]
            same_row_value = self._compare_values(value1, value2, col_index)

            if not same_row_value:
                same_row = False
                self._print_idx_error(col_index, value1, value2)

        return same_row

    def _compare_values(self, value1, value2, col_index):
        same_row_value = True

        if value1 == PandasTools.NO_DATA or value2 == PandasTools.NO_DATA:  # both values must be PandasTools.NO_DATA
            if value1 != PandasTools.NO_DATA or value2 != PandasTools.NO_DATA:
                same_row_value = False

        else:
            error = self._get_threshold(col_index)
            # print(value1, value2)
            assert(isinstance(error, int) and error >= 0)

            if error == 0:  # compare strings instead of int
                if value1 != value2:
                    same_row_value = False

            else:
                # compare ints
                abs_diff = abs(int(value1) - int(value2))
                if abs_diff > error:
                    print('abs_diff', abs_diff, 'error_threshold', error)
                    same_row_value = False

        return same_row_value

    def _print_idx_error(self, col_index, value1, value2):
        print("row_count = %s, col_index = %s, value1 = '%s', value2 = '%s'" % (self.row_count, col_index, value1, value2))

    #
    # Returns true iff one file has more rows than the other.
    #
    def _only_one_file_ends(self):
        if not self.file1.continue_reading and self.file2.continue_reading:
            print("file1 is shorter than file2")
            return True
        elif self.file1.continue_reading and not self.file2.continue_reading:
            print("file2 is shorter than file1")
            return True
        return False

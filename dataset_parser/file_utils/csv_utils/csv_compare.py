from csv_reader import CSVReader


class CSVCompare:
    def __init__(self, file1_path, file1_filename, file2_path, file2_filename):
        self.file1 = CSVReader(file1_path, file1_filename)
        self.file2 = CSVReader(file2_path, file2_filename)

    #
    # threshold is an array with the the maximum difference between the original and the compressed values
    # in a near-lossless compression schema
    #
    # if abort is True then the comparision stops as soon as an error is found.
    #
    def compare(self, error_thresholds = None, abort=True):
        self.error_thresholds = error_thresholds
        if self.error_thresholds is not None:
            for error in self.error_thresholds:
                assert(error >= 0)
        self.abort = abort
        self.message = "Same files!"

        self.row_count = 0
        idx_error = False
        while not idx_error and self.file1.continue_reading and self.file2.continue_reading:
            row1, row2 = self.file1.read_line(), self.file2.read_line()
            if self.row_count < 4:
                idx_error = self._compare_first_four_rows(row1, row2)
            else:
                idx_error = self._compare_rows(row1, row2)
            self.row_count += 1

            if not self.file1.continue_reading and self.file2.continue_reading:
                self.message = "file1 is shorter than file2"
                idx_error = True
            elif self.file1.continue_reading and not self.file2.continue_reading:
                self.message = "file2 is shorter than file1"
                idx_error = True

            elif not self.abort:
                idx_error = False

        if self.message == "Same files!":
            if self.error_thresholds is None:
                print "Same files! - compared with all thresholds = 0."
            else:
                print "Same files! - compared with thresholds = ", self.error_thresholds
            return True
        else:
            print self.message
            return False

        # if idx_error:
        #     print "ERROR IN LINE %s", self._print_row_count()
        #     return False
        # elif self.file1.continue_reading or self.file2.continue_reading:
        #     file_name = "file2" if self.file1.continue_reading else "file2"
        #     print "ERROR: reach end of file", file_name
        #     return False
        # else:
        #     print "Same files! - compared with thresholds = ", self.error_thresholds
        #     return True

    @classmethod
    def _compare_first_four_rows(cls, row1, row2):
        return True if row1 != row2 else False

    def _compare_rows(self, row1, row2):
        if len(row1) != len(row2):
            print "len(row1) = %s != %s = len(row2)" % (len(row1), len(row2))
            return True

        for col_index in xrange(len(row1)):
            idx_error = False
            error = 0 if self.error_thresholds is None else self.error_thresholds[col_index]
            value1, value2 = row1[col_index], row2[col_index]
            if value1 == 'N' or value2 == 'N':  # both values must be 'N'
                if value1 != 'N' or value2 != 'N':
                    idx_error = True
            elif error == 0:  # compare strings instead of int
                if value1 != value2:
                    idx_error = True
            else:  # compare ints
                # two numbers
                abs_diff = abs(int(value1) - int(value2))
                if abs_diff > error:
                    print 'abs_diff', abs_diff, 'error_threshold', error
                    idx_error = True

            if idx_error:
                self._print_idx_error(col_index, value1, value2)
                self.message = "Error in at least one line"
                if self.abort:
                    return True

        return False

    # def _print_row_count(self):
    #     print "row_count = %s" % str(self.row_count)

    def _print_idx_error(self, col_index, value1, value2):
        print "row_count = %s, col_index = %s, value1 = '%s', value2 = '%s'" % (self.row_count, col_index, value1, value2)


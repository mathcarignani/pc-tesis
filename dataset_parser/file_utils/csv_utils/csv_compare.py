from csv_reader import CSVReader


class CSVCompare:
    def __init__(self, file1_path, file1_filename, file2_path, file2_filename):
        self.file1 = CSVReader(file1_path, file1_filename)
        self.file2 = CSVReader(file2_path, file2_filename)

    #
    # threshold is an array with the the maximum difference between the original and the compressed values
    # in a near-lossless compression schema
    #
    def compare(self, threshold=None):
        self.row_count = 0
        idx_error = False
        while not idx_error and self.file1.continue_reading and self.file2.continue_reading:
            row1, row2 = self.file1.read_line(), self.file2.read_line()
            if self.row_count < 4:
                idx_error = self._compare_first_four_rows(row1, row2)
            else:
                idx_error = self._compare_rows(row1, row2, threshold)
            self.row_count += 1

        if idx_error:
            print "ERROR IN LINE %s", self._print_row_count()
            return False
        elif self.file1.continue_reading or self.file2.continue_reading:
            file_name = "file2" if self.file1.continue_reading else "file2"
            print "ERROR: reach end of file", file_name
            return False
        else:
            if threshold is None:
                print "Same files! - without threshold"
            else:
                print "Same files! - compared with threshold = ", threshold
            return True

    @classmethod
    def _compare_first_four_rows(cls, row1, row2):
        return True if row1 != row2 else False

    def _compare_rows(self, row1, row2, threshold):
        if len(row1) != len(row2):
            print "len(row1) = %s != %s = len(row2)" % (len(row1), len(row2))
            return True

        idx_error = False
        for idx in xrange(len(row1)):
            if row1[idx] == 'N' or row2[idx] == 'N':  # both values must be 'N'
                if row1[idx] != 'N' or row2[idx] != 'N':
                    idx_error = True
            else:
                if threshold is None:  # compare strings instead of int
                    # print self.row_count
                    if row1[idx] != row2[idx]:
                        idx_error = True
                else:
                    error_threshold = threshold[idx]
                    # two numbers
                    abs_diff = abs(int(row1[idx]) - int(row2[idx]))
                    if abs_diff > error_threshold:
                        print 'abs_diff', abs_diff, 'error_threshold', error_threshold
                        idx_error = True

            if idx_error:
                self._print_idx_error(idx, row1, row2)
                return True

        return False

    def _print_row_count(self):
        print "row_count = %s" % str(self.row_count)

    @classmethod
    def _print_idx_error(cls, idx, row1, row2):
        print "[idx = %s] row1 = '%s', row2 = '%s'" % (idx, row1[idx], row2[idx])


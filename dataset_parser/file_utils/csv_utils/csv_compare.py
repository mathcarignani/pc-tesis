from csv_reader import CSVReader

class CSVCompare:
    def __init__(self, file1_path, file1_filename, file2_path, file2_filename):
        self.file1 = CSVReader(file1_path, file1_filename)
        self.file2 = CSVReader(file2_path, file2_filename)

    #
    # threshold >=0 is the maximum difference between the original and the compressed values
    # in a near-lossless compression schema
    #
    def compare(self, threshold=0):
        self.row_count = 0
        while self.file1.continue_reading and self.file2.continue_reading:
            row1, row2 = self.file1.read_line(), self.file2.read_line()
            if self.row_count < 4:
                self._compare_first_four_rows(row1, row2)
            else:
                self._compare_rows(row1, row2, threshold)
            self.row_count += 1

        if self.file1.continue_reading or self.file2.continue_reading:
            file_name = "file2" if self.file1.continue_reading else "file2"
            print "ERROR: reach end of file", file_name
            return False
        else:
            print "Same files!"
            return True

    def _compare_first_four_rows(self, row1, row2):
        if row1 != row2:
            self._print_row_count()
            for idx, val in enumerate(row1):
                if row1[idx] != row2[idx]:
                    self._print_idx_error(idx, row1, row2)

    def _compare_rows(self, row1, row2, threshold):
        first_error = True
        for idx, val in enumerate(row2):
            idx_error = False
            if idx == 0:  # timestamp
                if row1[idx] != row2[idx]:
                    idx_error = True
            elif row1[idx] == 'N' or row2[idx] == 'N':  # both values must be 'N'
                if row1[idx] != 'N' or row2[idx] != 'N':
                    idx_error = True
            else:  # two numbers
                abs_diff = abs(int(row1[idx]) - int(row2[idx]))
                if abs_diff > threshold:
                    idx_error = True

            if idx_error and first_error:
                first_error = False
                self._print_row_count()
            if idx_error:
                self._print_idx_error(idx, row1, row2)

    def _print_row_count(self):
        print "row_count = %s" % str(self.row_count)

    @classmethod
    def _print_idx_error(cls, idx, row1, row2):
        print "[idx = %s] row1 = '%s', row2 = '%s'" % (idx, row1[idx], row2[idx])


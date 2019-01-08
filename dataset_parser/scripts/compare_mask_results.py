import sys
sys.path.append('.')

from file_utils.csv_utils.csv_reader import CSVReader
from file_utils.csv_utils.csv_writer import CSVWriter


class CompareMaskResults:
    def __init__(self):
        self.reader1 = None
        self.reader2 = None
        self.writer = None
        self.current_coder = None
        self.current_file_data = {}

        self.open()
        self.copy_header()
        while self.reader1.continue_reading:
            self.iterate()
        print self.current_file_data
        self.close()

    def open(self):
        path = "/Users/pablocerve/Documents/FING/Proyecto/results/avances-8/2-resultados-3-enero/mac/"
        self.reader1 = CSVReader(path + "mask-true", "results-mask-true.csv")
        self.reader2 = CSVReader(path + "mask-false", "results-mask-false.csv")
        self.writer = CSVWriter(path, "comparison.csv")

    def copy_header(self):
        header = self.reader1.read_line()
        self.reader2.read_line()
        self.writer.write_row(header)

    def close(self):
        self.reader1.close()
        self.reader2.close()
        self.writer.close()

    def iterate(self):
        line1 = self.reader1.read_line()
        filename, coder = line1[1], line1[3]

        if len(coder) > 0:
            if coder == "CoderBasic":
                print self.current_file_data
                self.current_file_data = {"name": filename, "TRUE": 0, "FALSE": 0, "SAME": 0}
            self.current_coder = coder

        if self.current_coder in ["CoderFR", "CoderSF"]:
            return

        # must compare two lines
        line2 = self.reader2.read_line()
        self.compare_two_lines(line1, line2)

    def compare_two_lines(self, line1, line2):
        assert(line1.count('') == line2.count(''))

        line1_indexes, line2_indexes = self.size_indexes(line1), self.size_indexes(line2)
        assert(line1_indexes == self.size_indexes(line2))

        # print "-------------------------------------------------"

        # [e] * n
        new_list = line1[:7]  # new_list = line1

        for i in line1_indexes:
            value1, value2 = int(line1[i]), int(line2[i])
            # print "true = " + str(value1) + " || false = " + str(value2)
            string, per = self.result(value1, value2)
            new_list.append(string + " = " + str(per) + "%")  # new_list[i] = res
            self.current_file_data[string] += 1
            # print res

        self.writer.write_row(new_list)

    @staticmethod
    def size_indexes(line1):
        length = len(line1)
        index = 15
        res = []
        while index < length:
            res.append(index)
            index += 4
        return res

    @staticmethod
    def result(value1, value2):
        if value1 < value2:
            return ["TRUE", CompareMaskResults.percentage(value2, value1)]
        elif value2 < value1:
            return ["FALSE", CompareMaskResults.percentage(value1, value2)]
        else:
            return ["SAME", 0]

    @staticmethod
    def percentage(big_value, small_value):
        assert(big_value > small_value)
        diff = float(big_value - small_value)
        percentage = diff / big_value  # e.g. 0.0214343854572
        return percentage * 100

CompareMaskResults()

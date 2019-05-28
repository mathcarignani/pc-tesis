import sys
sys.path.append('.')

from scripts.avances14.row_plot import RowPlot
from scripts.avances14.plotter import Plotter
from file_utils.csv_utils.csv_reader import CSVReader

class Script(object):
    ALGORITHMS = ["CoderPCA", "CoderAPCA", "CoderCA", "CoderPWLH", "CoderPWLHInt", "CoderGAMPSLimit"]
    THRESHOLD_PERCENTAGES = [0, 1, 3, 5, 10, 15, 20, 30]
    WINDOW_SIZES = [4, 8, 16, 32, 64, 128, 256]

    def __init__(self, filename):
        path = "/Users/pablocerve/Documents/FING/Proyecto/results/avances-13/3-0vs3"
        self.input_file = CSVReader(path, "0vs3.csv")
        self.filename = filename
        self.plotter = None
        self.row_plot = None
        self.__goto_file_start()

    def run(self):
        self.plotter = Plotter(self.filename, 1)
        for threshold in self.THRESHOLD_PERCENTAGES:
            print "threshold = " + str(threshold)
            self.row_plot = RowPlot(threshold)

            for algorithm in self.ALGORITHMS:
                print "  algorithm = " + algorithm

                self.row_plot.begin_algorithm(algorithm)
                self.__find_combination(self.filename, algorithm, threshold)

                for window_size in self.WINDOW_SIZES:
                    print "    window_size = " + str(window_size)
                    self.__find_next_line(6, window_size, True)
                    window, value0, value3 = self.__parse_line_values()
                    self.row_plot.add_values(window, value0, value3)

                self.row_plot.end_algorithm()
                self.__goto_file_start()
            self.plotter.add_row_plot(self.row_plot)
        self.plotter.plot()

    def __find_combination(self, filename, algorithm, threshold):
        self.__find_next_line(1, filename, False)
        self.__find_next_line(3, algorithm, False)
        self.__find_next_line(4, threshold, True)

    def __matching_line(self, index, value, is_integer):
        value_in_index = self.line[index]
        if len(value_in_index) == 0:
            return False
        value_to_compare = int(value_in_index) if is_integer else value_in_index
        return value == value_to_compare

    def __read_line(self):
        self.line = self.input_file.read_line()
        self.line_count += 1

    def __find_next_line(self, index, value, is_integer):
        print (index, value, is_integer)

        if self.line_count > 0 and self.__matching_line(index, value, is_integer):
            return True

        while self.input_file.continue_reading:
            self.__read_line()
            if self.__matching_line(index, value, is_integer):
                return True
        print "__find_next_line"
        print (index, value, is_integer)
        raise Exception("ERROR: __find_next_line")

    def __parse_line_values(self):
        window = int(self.line[6])
        first_index = 7
        value0 = self.__get_int(self.line[first_index])
        value3 = self.__get_int(self.line[first_index + 7])
        return window, value0, value3

    @classmethod
    def __get_int(cls, string):
        # string = "1,285,310 - W - 1.36"
        return int(string.split()[0].replace(",", ""))

    def __goto_file_start(self):
        self.input_file.goto_row(0)
        self.line = None
        self.line_count = 0

script = Script("vwc_1202.dat.csv")
script.run()





# plotter = Plotter('filename.png', 1)
# for y in xrange(8):
#     r_plot = RowPlot(y + 1)
#     for x in xrange(6):
#         c = 'Coder ' + str(x + 1)
#         r_plot.begin_algorithm(c)
#         r_plot.add_values(4, 779670, 759969)
#         r_plot.add_values(8, 988620, 838923)
#         r_plot.add_values(16, 1053306, 1054779)
#         r_plot.add_values(32, 1054368, 1053153)
#         r_plot.add_values(64, 1052724, 1051509)
#         r_plot.add_values(128, 1051908, 1050693)
#         r_plot.add_values(256, 1051500, 1050285)
#         r_plot.end_algorithm()
#     plotter.add_row_plot(r_plot)
#
# plotter.plot()

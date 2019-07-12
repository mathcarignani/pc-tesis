import sys
sys.path.append('.')

from scripts.informe.plot.csv_constants import CSVConstants
from scripts.informe.math_utils import MathUtils
from scripts.informe.results_reader import ResultsReader


#
# Methods used by the following scripts:
# + avances18/globalize_results.py
# + avances19/use_basic_coder.py
#
class GlobalizeUtils(object):
    @staticmethod
    def convert_line(line, global_mode=True):
        new_line = []
        #    0         1        2     3    4         5                6
        # Dataset, Filename, #rows, Coder, %, Error Threshold, Window Param
        #
        new_line.append(line[CSVConstants.INDEX_DATASET])

        filename = line[CSVConstants.INDEX_FILENAME]
        if global_mode:
            filename = 'Global' if len(filename) > 0 else filename
        new_line.append(filename)

        no_rows = line[CSVConstants.INDEX_NO_ROWS]
        new_line.append(MathUtils.str_to_int(no_rows) if isinstance(no_rows, int) else '')

        new_line += line[CSVConstants.INDEX_ALGORITHM:(CSVConstants.INDEX_THRESHOLD + 1)]  # Coder, %
        new_line.append('')  # Error Threshold
        new_line.append(line[CSVConstants.INDEX_WINDOW])  # Window Param

        #    7         8             9                     10                  11                 12
        # Size (B), CR (%), Delta - Size (data), Delta - Size (mask), Delta - Size (total), Delta - CR (%), ...
        #
        for index in range(CSVConstants.INDEX_TOTAL_SIZE, len(line)):
            if CSVConstants.is_percentage_index(index):
                new_line.append("?")
            else:
                new_line.append(MathUtils.str_to_int(line[index]))
        return new_line

    @staticmethod
    def write_other_coders_lines(output_file, coder_basic_line, other_coders_lines):
        for index, line in enumerate(other_coders_lines):
            if index > 0:  # Ignore CoderBasic
                line_with_percentages = ResultsReader.set_percentages(line, coder_basic_line)
                output_file.write_row(line_with_percentages)
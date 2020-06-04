import sys
sys.path.append('.')

from scripts.informe.plot.csv_constants import CSVConstants
from scripts.informe.math_utils import MathUtils
from scripts.informe.results_parsing.results_reader import ResultsReader


#
# Methods used by the following scripts:
# + avances18/globalize_results.py
#
class GlobalizeUtils(object):
    @staticmethod
    def convert_line(line, global_mode=True):
        new_line = ResultsReader.convert_line(line)
        if global_mode:
            filename = new_line[1]
            new_filename = 'Global' if len(filename) > 0 else filename
            new_line[1] = new_filename
        return new_line

    @staticmethod
    def write_other_coders_lines(output_file, coder_base_line, other_coders_lines):
        for index, line in enumerate(other_coders_lines):
            if index > 0:  # Ignore CoderBase
                line_with_percentages = ResultsReader.set_percentages(line, coder_base_line)
                output_file.write_row(line_with_percentages)

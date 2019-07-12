import sys
sys.path.append('.')


from scripts.avances18.globalize_utils import GlobalizeUtils
from scripts.compress.compress_aux import DATASETS_ARRAY, dataset_csv_filenames
from file_utils.csv_utils.csv_writer import CSVWriter
from scripts.informe.plot.csv_constants import CSVConstants
from scripts.informe.results_reader import ResultsReader


#
# Takes the Coder Basic results for MM=0 and substitutes the Coder Basic results in MM=3 (recalculating percentages)
#
class UseBasicCoder(object):
    def __init__(self, output_path, output_file):
        self.input_file_0 = ResultsReader('raw', 0)
        self.input_file_3 = ResultsReader('raw', 3)

        self.output_file = CSVWriter(output_path, output_file)
        self.output_file.write_row(self.input_file_3.read_line_no_count())

        for dataset_obj in DATASETS_ARRAY:
            self.__use_basic_coder_dataset(dataset_obj['name'])

    def __use_basic_coder_dataset(self, dataset_name):
        filenames = dataset_csv_filenames(dataset_name)
        for filename in filenames:
            self.__use_basic_coder_filename(filename)

    def __use_basic_coder_filename(self, filename):
        self.input_file_0.find_filename(filename)
        self.input_file_3.find_filename(filename)

        # MM=0 => CoderBasic
        coder_basic_line = self.input_file_0.line
        coder_basic_line = GlobalizeUtils.convert_line(coder_basic_line, False)
        coder_basic_line_with_percentages = ResultsReader.set_percentages(coder_basic_line, coder_basic_line)
        self.output_file.write_row(coder_basic_line_with_percentages)

        # MM=3 => CoderBasic, CoderPCA, CoderAPCA, etc.
        other_coders_lines = ResultsReader.add_until_change(self.input_file_3, CSVConstants.INDEX_FILENAME)
        other_coders_lines = [GlobalizeUtils.convert_line(line, False) for line in other_coders_lines]
        GlobalizeUtils.write_other_coders_lines(self.output_file, coder_basic_line, other_coders_lines)


def run():
    output_path = "/Users/pablocerve/Documents/FING/Proyecto/results/avances-19"
    output_file = "complete-mask-mode=3-use_basic_coder.csv"
    UseBasicCoder(output_path, output_file)

run()

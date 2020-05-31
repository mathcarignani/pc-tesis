import sys
sys.path.append('.')

from file_utils.csv_utils.csv_writer import CSVWriter
from scripts.compress.experiments_utils import ExperimentsUtils
from scripts.informe.math_utils import MathUtils
from scripts.informe.data_analysis.process_results.writer_min_max import WriterMinMax

class Writer1(object):
    def __init__(self, path, extra_str):
        self.file = CSVWriter(path, extra_str + '-process1.csv')
        self.write_first_row()
        self.data_rows = []
        self.data = {}
        self.writer_min_max = WriterMinMax(path)

    def write_first_row(self):
        row = ["Dataset", "Filename", "Column", "Coder"]
        row += 2 * (ExperimentsUtils.THRESHOLDS + [''])
        row += ExperimentsUtils.THRESHOLDS + ['WORST', ''] + ExperimentsUtils.THRESHOLDS
        self.file.write_row(row)

    def write_dataset_name(self, dataset_name):
        self.file.write_row(([dataset_name]))

    def write_filename(self, filename):
        self.file.write_row(['', filename])

    def write_col_name(self, col_name):
        self.file.write_row(['', '', col_name])

    def save_data_row(self, coder_name, windows, percentages, total_bits):
        data_row = {'coder_name': coder_name, 'windows': windows, 'percentages': percentages, 'total_bits': total_bits}
        self.data_rows.append(data_row)

    def write_data_rows(self):
        self._calculate_relative_differences()
        for row in self.data_rows:
            coder_name, windows,  = row['coder_name'], row['windows']
            percentages, total_bits = row['percentages'], row['total_bits']
            relative_diffs = row['relative_diffs_string']
            worst_relative_diff = row['worst_relative_diff']
            worst_relative_diff_string = row['worst_relative_diff_string']

            row = ['', '', '', coder_name] + windows + [''] + percentages + ['']
            row += relative_diffs + [worst_relative_diff_string, ''] + total_bits
            self.file.write_row(row)

            if coder_name not in self.data:
                self.data[coder_name] = []
            self.data[coder_name].append(worst_relative_diff)

        self.writer_min_max.save_data_rows(self.data_rows)
        self.data_rows = []

    def show_data(self):
        for key in self.data:
            max_rd = max(self.data[key])
            print(self.format_rd(max_rd) + ' <= ' + key)
        self.writer_min_max.show_data()

    def _calculate_relative_differences(self):
        for row in self.data_rows:
            row['relative_diffs'] = []
            row['relative_diffs_string'] = []

        for threshold_index in range(len(ExperimentsUtils.THRESHOLDS)):
            for row in self.data_rows:
                smallest = self._smallest_total_bits(threshold_index)
                total_bits = row['total_bits'][threshold_index]
                rd = MathUtils.relative_difference(total_bits, smallest)
                rd_string = self.format_rd(rd)

                row['relative_diffs'].append(rd)
                row['relative_diffs_string'].append(rd_string)

        self._calculate_worst_relative_diff()

    def _calculate_worst_relative_diff(self):
        for row in self.data_rows:
            # row['relative_diffs'] = [row['relative_diffs'][0]]  # ONLY LOSSLESS
            # row['relative_diffs'] = row['relative_diffs'][1:]  # ONLY LOSSY
            worst_rd = max(row['relative_diffs'])

            row['worst_relative_diff'] = worst_rd
            row['worst_relative_diff_string'] = self.format_rd(worst_rd)

    def _smallest_total_bits(self, threshold_index):
        smallest = None
        for row in self.data_rows:
            total_bits = row['total_bits'][threshold_index]
            if smallest is None or total_bits < smallest:
                smallest = total_bits
        return smallest

    def write_row(self, row):
        self.file.write_row(row)

    @staticmethod
    def format_rd(rd):
        return "%0.2f" % rd
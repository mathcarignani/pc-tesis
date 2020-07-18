import sys
sys.path.append('.')

from file_utils.text_utils.text_file_writer import TextFileWriter
from scripts.compress.experiments_utils import ExperimentsUtils
from scripts.informe.data_analysis.process_results.latex_utils import LatexUtils

class WriterMinMax:
    def __init__(self, path, mode):
        self.path = path
        self.mode = mode
        self.dataset_name = None
        self.filename = None
        self.data_rows_array = []
        self.table_results = []

    def set_dataset(self, dataset_name):
        self.dataset_name = dataset_name

    def set_filename(self, filename):
        self.filename = filename

    def save_data_rows(self, data_rows):
        # save the data rows for a data type
        self.data_rows_array.append(data_rows)

    def show_data(self):
        assert(len(self.data_rows_array) == 21)
        first_data_rows = self.data_rows_array[0]  # array of objects corresponding to first data type
        for data_row in first_data_rows:
            coder_name = data_row['coder_name']
            self._populate_data(coder_name)

        best_rds = self._calculate_best_rd_for_each_threshold()
        data_lines = self._data_lines(best_rds)
        filename = "table-minmax-" + str(self.mode) + ".tex"
        self._create_latex_file(filename, data_lines)

    def _populate_data(self, coder_name):
        coder_rds = []
        for idx, threshold in enumerate(ExperimentsUtils.THRESHOLDS):
            max_rd = None
            for data_rows in self.data_rows_array:
                for row in data_rows:
                    if row['coder_name'] != coder_name:
                        continue
                    rd = row['relative_diffs'][idx]
                    if max_rd is None or max_rd < rd:
                        max_rd = rd
            coder_rds.append(max_rd)
        self.table_results.append({'coder_name': coder_name, 'coder_rds': coder_rds})

    def _data_lines(self, best_rds):
        first_row = ['Algorithm'] + ["e = " + str(threshold) for threshold in ExperimentsUtils.THRESHOLDS]
        output_rows = [first_row]

        for result in self.table_results:
            coder = result['coder_name'].replace('Coder', '')  # e.g. "PCA"
            coder_style = LatexUtils.coder_style(coder)
            coder_row = [coder + coder_style]
            for idx, value in enumerate(result['coder_rds']):
                rd_str = self._format_rd(value)
                if value == best_rds[idx]:
                    rd_str = self._format_best(rd_str)
                coder_row.append(rd_str)
            if coder != 'Base':  # do not show CoderBase results
                output_rows.append(coder_row)
        data_lines = [LatexUtils.array_to_table_row(row) for row in output_rows]
        return data_lines

    def _calculate_best_rd_for_each_threshold(self):
        best_rds = []
        for idx, threshold in enumerate(ExperimentsUtils.THRESHOLDS):
            threshold_best = None
            for result in self.table_results:
                rd = result['coder_rds'][idx]
                if threshold_best is None or threshold_best > rd:
                    threshold_best = rd
                else:
                    assert(threshold_best < rd)  # check that there are no cases in which there are two best values
            best_rds.append(threshold_best)
        return best_rds

    @staticmethod
    def _format_best(value):
        return r"\best" + value

    @staticmethod
    def _format_rd(rd):
        if rd == 0:
            return '0'
        return "%0.2f" % rd

    def _create_latex_file(self, filename, data_lines):
        output = TextFileWriter(self.path, filename)
        output.write_line(r"\begin{table}[h]")
        for line in LatexUtils.print_commands():
            output.write_line(line)
        first_lines = [
            r"\newcommand{\best}{\cellcolor{gray!30}}",
            r"\centering"
            r"\hspace*{0cm}\begin{tabular}{| l | c | c | c | c | c | c | c | c |}"
            r"\cline{2-9}"
            r"\multicolumn{1}{c|}{}& \multicolumn{8}{c|}{maxRD (\%)}\\\hline"
        ]
        last_lines = [
            r"\end{tabular}",
            r"\caption{\captionminmax}",
            r"\label{experiments:minmax}",
            r"\end{table}"
        ]
        for line in first_lines + data_lines + last_lines:
            output.write_line(line)

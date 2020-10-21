
import sys
sys.path.append('.')

import os

from scripts.compress.experiments_utils import ExperimentsUtils
from scripts.informe.data_analysis.process_results.latex_utils import LatexUtils
from scripts.informe.math_utils import MathUtils
from file_utils.text_utils.text_file_reader import TextFileReader
from file_utils.text_utils.text_file_writer import TextFileWriter


class RangesTable(object):
    FILENAME = "table-relative.tex"

    def __init__(self, datasets_data, path):
        self.datasets_data = datasets_data
        self.writer = TextFileWriter(path, self.FILENAME)

    def create_table(self):
        reader = TextFileReader(os.path.dirname(__file__), '_begin.tex')
        self.writer.append_file(reader)

        for name in ["IRKIS", "SST", "ADCP", "ElNino", "Solar", "Hail", "Tornado", "Wind"]:
            self.add_dataset_line(name)

        reader = TextFileReader(os.path.dirname(__file__), '_end.tex')
        self.writer.append_file(reader)
        self.writer.close()

    def add_dataset_line(self, name):
        data = self.datasets_data[name]
        dataset_key = LatexUtils.get_dataset_key(name)
        gaps_info = ExperimentsUtils.get_gaps_info(name)
        assert(data['zero'] == 0)
        total = data['negative'] + data['positive']
        percentage = MathUtils.calculate_percentage(total, data['positive'], 2)
        percentage = int(percentage) if int(percentage) == percentage else round(percentage, 1)
        outperform_str = str(data['positive']) + "/" + str(total) + " (" + str(percentage) + "\%)"
        range_str = self.range_str(data)
        self.add_line([dataset_key, gaps_info, outperform_str, range_str])

    def add_line(self, array):
        line = "    " + " & ".join(array) + r" \\\hline"
        self.writer.write_line(line)

    @staticmethod
    def range_str(data):
        min_str = str(round(data['min'], 2))
        max_str = str(round(data['max'], 2))
        max_zero = max_str == "-0.0"
        if max_zero:
            max_str = "0"

        if data['info'] == "PlotMin":
            min_str = RangesTable.color_value(min_str, 'blue')
        elif data['info'] == "PlotMax":
            max_str = RangesTable.color_value(max_str, 'red')
        return "[" + min_str + "; " + max_str + (")" if max_zero else "]")

    @staticmethod
    def color_value(value, color):
        return r"\textcolor{" + color + "}{" + value + "}"

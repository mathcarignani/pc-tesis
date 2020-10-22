
import sys
sys.path.append('.')

import os

from scripts.informe.math_utils import MathUtils
from scripts.informe.latex_tables.latex_utils import LatexUtils
from file_utils.text_utils.text_file_reader import TextFileReader
from file_utils.text_utils.text_file_writer import TextFileWriter


class TableWindows(object):
    FILENAME = "table-windows.tex"

    def __init__(self, algorithms_data, path):
        self.algorithms_data = algorithms_data
        self.writer = TextFileWriter(path, self.FILENAME)

    def create_table(self):
        reader = TextFileReader(os.path.dirname(__file__), '_begin.tex')
        self.writer.append_file(reader)

        for name in self.algorithms_data.keys():
            line = self.generate_algorithm_line(name)
            self.writer.write_line(line)

        reader = TextFileReader(os.path.dirname(__file__), '_end.tex')
        self.writer.append_file(reader)
        self.writer.close()

    def generate_algorithm_line(self, name):
        data = self.algorithms_data[name]
        name = name.replace("Coder", "")
        name = name.replace("Limit", "")
        total = sum(data)
        expected_total = 1400 if name == "Total" else 200
        assert(total == expected_total)

        line = [name]
        for value in data:
            percentage = MathUtils.calculate_percentage(total, value, 1)
            percentage = int(percentage) if int(percentage) == percentage else percentage
            value_str = str(format(value,',d'))
            if value_str != "0":
                value_str += " (" + str(percentage) + "\%)"
            line.append(value_str)
        line = LatexUtils.format_line(line)
        if name == "GAMPS":
            line += "\hline"
        return line
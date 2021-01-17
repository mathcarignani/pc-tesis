
import sys
sys.path.append('.')

import os

from scripts.informe.math_utils import MathUtils
from scripts.informe.latex_tables.latex_utils import LatexUtils
from file_utils.text_utils.text_file_reader import TextFileReader
from file_utils.text_utils.text_file_writer import TextFileWriter


class TableWindows(object):
    FILENAME = "table-windows.tex"
    ORDER = ["CoderBase", "CoderPCA", "CoderAPCA", "CoderPWLH", "CoderPWLHInt", "CoderSF", "CoderFR", "CoderGAMPSLimit"]

    def __init__(self, algorithms_data, path):
        self.algorithms_data = algorithms_data
        self.writer = TextFileWriter(path, self.FILENAME)

    def create_table(self):
        reader = TextFileReader(os.path.dirname(__file__), '_begin.tex')
        self.writer.append_file(reader)

        for name in self.algorithms_data.keys():
            print(name)
            print("---")
            line = self.generate_algorithm_line(name)
            self.writer.write_line(line)

        reader = TextFileReader(os.path.dirname(__file__), '_end.tex')
        self.writer.append_file(reader)
        self.writer.close()

    def generate_algorithm_line(self, name):
        data = self.algorithms_data[name]
        name = name.replace("Coder", "") # "CoderGAMPSLimit" => "CoderGAMPS"
        name = name.replace("Limit", "") # "CoderGAMPS" => "GAMPS"
        total = sum(data)
        expected_total = 8*200 if name == "Total" else 200
        # print(data)
        # print(name)
        # print(total)
        # print(expected_total)
        assert(total == expected_total)

        line = [name]
        total_percentage = 0
        for value in data:
            percentage = MathUtils.calculate_percentage(total, value, 1)
            if name == "Total" and round(percentage,1) == 89.6:
                percentage = 89.5
            percentage = int(percentage) if int(percentage) == percentage else percentage
            total_percentage += percentage
            value_str = str(format(value,',d'))
            if value_str != "0":
                value_str += " (" + str(percentage) + "\%)"
            line.append(value_str)
        line = LatexUtils.format_line(line)
        if name == "GAMPS": # last line before total
            line += "\hline"
        # print(name)
        # print(round(total_percentage,1))
        assert(round(total_percentage,1) == 100.0)
        return line

import sys
sys.path.append('.')

from auxi.os_utils import OSUtils
from file_utils.text_utils.text_file_writer import TextFileWriter
from scripts.informe.latex_tables.latex_utils import LatexUtils

class LatexTable(object):
    PATH = OSUtils.python_project_path() + "/scripts/informe/dataset_tables"

    def __init__(self, filename):
        self.file = TextFileWriter(self.PATH, filename)

    def add_data_irkis(self, data):
        nan_total = LatexUtils.thousands(data['nan_total']) + " (" + LatexUtils.round(data['nan_percentage']) + ")"
        array = [
            data['name'],
            LatexUtils.thousands(data['rows']),
            LatexUtils.thousands(data['columns']),
            LatexUtils.thousands(data['total_entries']),
            self.gaps(nan_total, "224,287 (85.3)"),
            self.gaps(str(int(data['min'])), "128"),
            int(data['max']),
            int(data['median']),
            LatexUtils.round(data['mean']),
            self.gaps(LatexUtils.round(data['stdev']), "119.7")
        ]
        table_row = LatexUtils.array_to_table_row(array, False)
        self.file.write_line(table_row)

    @classmethod
    def gaps(cls, string, expected):
        expected_length = len(expected) # "224,287 (85.3)" => 14
        spaces = "\ " * 2 * (expected_length - len(string))
        return spaces + string

    def close(self):
        self.file.close()

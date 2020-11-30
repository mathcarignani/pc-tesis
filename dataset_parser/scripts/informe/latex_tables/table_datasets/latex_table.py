import sys
sys.path.append('.')

from auxi.os_utils import OSUtils
from file_utils.text_utils.text_file_writer import TextFileWriter
from scripts.informe.latex_tables.latex_utils import LatexUtils

class LatexTable(object):
    PATH = OSUtils.python_project_path() + "/scripts/informe/latex_tables/table_datasets/output"

    def __init__(self, filename):
        self.file = TextFileWriter(self.PATH, filename)

    def add_data_irkis(self, data):
        array = [
            data['name'],
            LatexUtils.thousands(data['rows']),
            LatexUtils.thousands(data['columns']),
            LatexUtils.thousands(data['total_entries']),
            self.add_spaces(LatexTable.nan_total(data), "224,287 (85.3)"),
            self.add_spaces(str(int(data['min'])), "128"),
            int(data['max']),
            int(data['median']),
            LatexUtils.round(data['mean']),
            self.add_spaces(LatexUtils.round(data['stdev']), "119.7")
        ]
        table_row = LatexUtils.array_to_table_row(array, False)
        self.file.write_line(table_row)

    def add_data_sst(self, data):
        array = [
            data['name'],
            LatexUtils.thousands(data['rows']),
            LatexUtils.thousands(data['columns']),
            LatexUtils.thousands(data['total_entries']),
            LatexTable.nan_total(data),
            int(data['min']),
            LatexUtils.thousands(int(data['max'])),
            LatexUtils.thousands(int(data['median'])),
            LatexUtils.round_thousands(data['mean']),
            LatexUtils.round_thousands(data['stdev'])
        ]
        table_row = LatexUtils.array_to_table_row(array, False)
        self.file.write_line(table_row)

    def add_data_adcp(self, data):
        array = [
            data['name'],
            LatexUtils.thousands(data['rows']),
            LatexUtils.thousands(data['columns']),
            LatexUtils.thousands(data['total_entries']),
            LatexTable.nan_total(data),
            int(data['min']),
            LatexUtils.thousands(int(data['max'])),
            LatexUtils.thousands(int(data['median'])),
            LatexUtils.round_thousands(data['mean']),
            LatexUtils.round_thousands(data['stdev'])
        ]
        table_row = LatexUtils.array_to_table_row(array, False)
        self.file.write_line(table_row)

    def add_data_elnino(self, data):
        assert(LatexUtils.thousands(data['rows']) == "6,371")
        assert(LatexUtils.thousands(data['columns']) == "78")
        assert(LatexUtils.thousands(data['total_entries']) == "496,938")
        array = [
            data['name'],
            LatexTable.nan_total(data),
            self.add_spaces2(LatexUtils.thousands(int(data['min'])), "-18,000"),
            self.add_spaces2(LatexUtils.thousands(int(data['max'])), "17,108"),
            self.add_spaces2(LatexUtils.thousands(int(data['median'])), "-11,126"),
            self.add_spaces2(LatexUtils.round_thousands(data['mean']), "-5,402.5"),
            self.add_spaces2(LatexUtils.round_thousands(data['stdev']), "13,536.4")
        ]
        table_row = LatexUtils.array_to_table_row(array, False)
        self.file.write_line(table_row)

    def add_data_hail(self, data):
        assert(LatexUtils.thousands(data['rows']) == "17,059")
        assert(LatexUtils.thousands(data['columns']) == "1")
        assert(LatexUtils.thousands(data['total_entries']) == "17,059")
        array = [
            data['name'],
            LatexTable.nan_total(data),
            self.add_spaces3(LatexUtils.thousands(int(data['min'])), "-12,442"),
            self.add_spaces3(LatexUtils.thousands(int(data['max'])), "-6,783"),
            self.add_spaces3(LatexUtils.thousands(int(data['median'])), "-9,676"),
            self.add_spaces3(LatexUtils.round_thousands(data['mean']), "-9,487.4"),
            self.add_spaces2(LatexUtils.round_thousands(data['stdev']), "841.4")
        ]
        table_row = LatexUtils.array_to_table_row(array, False)
        self.file.write_line(table_row)

    def add_data_tornado(self, data):
        assert(LatexUtils.thousands(data['rows']) == "3,841")
        assert(LatexUtils.thousands(data['columns']) == "1")
        assert(LatexUtils.thousands(data['total_entries']) == "3,841")
        array = [
            data['name'],
            LatexTable.nan_total(data),
            self.add_spaces3(LatexUtils.thousands(int(data['min'])), "-12,397"),
            self.add_spaces3(LatexUtils.thousands(int(data['max'])), "-6,822"),
            self.add_spaces3(LatexUtils.thousands(int(data['median'])), "-9,313"),
            self.add_spaces3(LatexUtils.round_thousands(data['mean']), "-9,260.0"),
            self.add_spaces2(LatexUtils.round_thousands(data['stdev']), "787.9")
        ]
        table_row = LatexUtils.array_to_table_row(array, False)
        self.file.write_line(table_row)

    def add_data_wind(self, data):
        assert(LatexUtils.thousands(data['rows']) == "40,260")
        assert(LatexUtils.thousands(data['columns']) == "1")
        assert(LatexUtils.thousands(data['total_entries']) == "40,260")
        array = [
            data['name'],
            LatexTable.nan_total(data),
            self.add_spaces3(LatexUtils.thousands(int(data['min'])), "-12,432"),
            self.add_spaces2(LatexUtils.thousands(int(data['max'])), "2,359"),
            self.add_spaces3(LatexUtils.thousands(int(data['median'])), "-8,732"),
            self.add_spaces3(LatexUtils.round_thousands(data['mean']), "-8,870.1"),
            self.add_spaces2(LatexUtils.round_thousands(data['stdev']), "968.4")
        ]
        table_row = LatexUtils.array_to_table_row(array, False)
        self.file.write_line(table_row)

    def add_data_solar(self, data):
        assert(LatexUtils.thousands(data['rows']) == "8,759")
        assert(LatexUtils.thousands(data['columns']) == "12")
        assert(LatexUtils.thousands(data['total_entries']) == "105,108")
        array = [
            data['name'],
            LatexTable.nan_total(data,2),
            self.add_spaces2(LatexUtils.thousands(int(data['min'])), "0"),
            self.add_spaces4(LatexUtils.thousands(int(data['max'])), "1,005"),
            self.add_spaces4(LatexUtils.thousands(int(data['median'])), "11"),
            self.add_spaces4(LatexUtils.round_thousands(data['mean']), "187.6"),
            self.add_spaces2(LatexUtils.round_thousands(data['stdev']), "274.7")
        ]
        table_row = LatexUtils.array_to_table_row(array, False)
        self.file.write_line(table_row)


    @classmethod
    def nan_total(cls, data, round_=1):
        rounded = LatexUtils.round(data['nan_percentage'], round_)
        return LatexUtils.thousands(data['nan_total']) + " (" + rounded + ")"

    @classmethod
    def add_spaces(cls, string, expected):
        assert(len(string) <= len(expected))
        expected_length = len(expected) # "224,287 (85.3)" => 14
        spaces = "\ " * 2 * (expected_length - len(string))
        return spaces + string

    @classmethod
    def add_spaces2(cls, string, expected):
        assert(len(string) <= len(expected))
        expected_length = len(expected) # "224,287 (85.3)" => 14
        spaces = "\ " * 1 * (expected_length - len(string))
        spaces = spaces + "\ " if len(string) != len(expected) else spaces
        return spaces + string

    @classmethod
    def add_spaces3(cls, string, expected):
        assert(len(string) <= len(expected))
        expected_length = len(expected) # "224,287 (85.3)" => 14
        spaces = "\ " * 1 * (expected_length - len(string))
        spaces = spaces + "\ " if len(string) != len(expected) else spaces
        spaces = spaces + "\ " if "-" in string else spaces
        spaces = spaces + "\ " if len(string) == 3 else spaces
        spaces = spaces + "\ " * 2 if string == "0" else spaces
        return spaces + string

    @classmethod
    def add_spaces4(cls, string, expected):
        assert(len(string) <= len(expected))
        expected_length = len(expected) # "224,287 (85.3)" => 14
        spaces = "\ " * 1 * (expected_length - len(string))
        spaces = spaces + "\ " if len(string) != len(expected) else spaces
        spaces = spaces + "\ " if "-" in string else spaces
        spaces = spaces + "\ " if string == "11" else spaces
        return spaces + string

    def close(self):
        self.file.close()

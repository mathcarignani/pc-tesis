import sys
sys.path.append('.')

from auxi.os_utils import OSUtils
from file_utils.text_utils.text_file_writer import TextFileWriter

class LatexTable(object):
    PATH = OSUtils.python_project_path() + "/scripts/informe/dataset_tables"

    def __init__(self, filename):
        self.file = TextFileWriter(self.PATH, filename)

    def add_data(self, data):
        attributes = [
            'name', 'rows', 'columns', 'total_entries', 'nan_total', 'nan_percentage',
            'min', 'mean', 'median', 'max', 'stdev'
        ]
        line = []
        for attr in attributes:
            line.append(str(data[attr]))
        print(line)
        line = " & ".join(line)
        self.file.write_line(str(line))

    def close(self):
        self.file.close()

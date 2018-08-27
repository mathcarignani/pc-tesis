import csv
from file_utils.auxi import full_path


class CSVWriter:
    def __init__(self, path, filename):
        self.file = open(full_path(path, filename), "w")
        self.csv_writer = csv.writer(self.file)

    def write_row(self, row):
        self.csv_writer.writerow(row)

    def close(self):
        self.file.close()

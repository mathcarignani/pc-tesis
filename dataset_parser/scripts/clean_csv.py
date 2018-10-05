import sys
sys.path.append('.')

from auxi.os_utils import datasets_csv_path, python_project_path
from file_utils.csv_utils.csv_reader import CSVReader
from file_utils.csv_utils.csv_writer import CSVWriter

input_path = datasets_csv_path() + "[1]irkis/"
input_filename = "vwc_1202.dat.csv"

output_path = python_project_path()
output_filename = "vwc_1202.dat_CLEAN.csv"  # "vwc_1202.dat_CONSTANT_TIME.csv"


def line_contains_nodata(line_):
    return "N" in line_


def set_line_timestamp(line_, timestamp_):
    line_[0] = timestamp_
    return line_

csv_reader = CSVReader(input_path, input_filename)
csv_writer = CSVWriter(output_path, output_filename)

first_value = True
while csv_reader.continue_reading:
    line = csv_reader.read_line()

    if csv_reader.current_line_count < 5:
        # copy header rows verbatim
        csv_writer.write_row(line)
        continue

    if line_contains_nodata(line):
        # don't copy rows which contain nodata entries
        continue

    timestamp = 0 if first_value else 1
    first_value = False
    line = set_line_timestamp(line, timestamp)
    csv_writer.write_row(line)

csv_reader.close()
csv_writer.close()

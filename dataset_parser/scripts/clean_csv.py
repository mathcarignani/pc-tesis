import sys
sys.path.append('.')

from auxi.os_utils import datasets_csv_path, python_project_path, cpp_project_path
from file_utils.csv_utils.csv_reader import CSVReader
from file_utils.csv_utils.csv_writer import CSVWriter

########################################################################################################################


def line_contains_nodata(line_):
    return "N" in line_


def set_line_timestamp(line_, timestamp_):
    line_[0] = timestamp_
    return line_


def clean():
    input_path = datasets_csv_path() + "[1]irkis/"
    input_filename = "vwc_1202.dat.csv"

    output_path = python_project_path()
    output_filename = "vwc_1202.dat_CLEAN.csv"  # "vwc_1202.dat_CONSTANT_TIME.csv"

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

# clean()

########################################################################################################################


def get_n_indexes(line):
    return [i for i, e in enumerate(line) if e == "N"]


def remove_n_indexes(line, n_indexes):
    return [j for i, j in enumerate(line) if i not in n_indexes]


def compare_lines(line_1, line_2, current_line_count):
    error_threshold = 5

    if current_line_count < 4:
        # header rows should match
        assert(line_1 == line_2)
        return

    line_1_N_indexes = get_n_indexes(line_1)
    line_2_N_indexes = get_n_indexes(line_2)

    assert(line_1_N_indexes == line_2_N_indexes)

    line_1_int = [int(item) for item in remove_n_indexes(line_1, line_1_N_indexes)]
    line_2_int = [int(item) for item in remove_n_indexes(line_2, line_2_N_indexes)]

    list_diff = [abs(x1 - x2) for (x1, x2) in zip(line_1_int, line_2_int)]
    print [current_line_count] + list_diff
    assert(list_diff[0] == 0)
    assert(max(list_diff) <= error_threshold)


def compare():
    test_files_path = cpp_project_path() + "/test_files"
    csv_reader_1 = CSVReader(test_files_path + "/sf", "vwc_1202.dat_CLEAN.csv")
    csv_reader_2 = CSVReader(test_files_path, "vwc_1202.dat_CLEAN.csv-CoderSF-Decode.csv")

    while csv_reader_1.continue_reading:
        assert(csv_reader_1.current_line_count == csv_reader_2.current_line_count)
        current_line_count = csv_reader_1.current_line_count

        line_1 = csv_reader_1.read_line()
        line_2 = csv_reader_2.read_line()

        compare_lines(line_1, line_2, current_line_count)

    csv_reader_1.close()
    csv_reader_2.close()

compare()



import sys
sys.path.append('.')

from auxi.os_utils import OSUtils
from file_utils.csv_utils.csv_reader import CSVReader
from file_utils.csv_utils.csv_writer import CSVWriter
from file_utils.text_utils.text_file_reader import TextFileReader

########################################################################################################################


def set_line_timestamp(line_, timestamp_):
    line_[0] = timestamp_
    return line_


def iterate(csv_reader, csv_writer):
    first_value = True
    last_column = 2

    while csv_reader.continue_reading:
        line = csv_reader.read_line()

        if csv_reader.current_line_count < 5:  # header rows
            if csv_reader.current_line_count == 4:  # column titles row
                line = [line[0], line[516], line[519]]
            csv_writer.write_row(line)
            continue

        line = [line[0], line[516], line[519]]
        # line = set_line_timestamp(line, timestamp)
        # if last_column:
        #     line = line[:last_column]

            # data rows
        # if "N" in line:
        #     line[1] = "397"

        csv_writer.write_row(line)


def clean():
    input_path = OSUtils.cpp_project_path() + "/test_files"
    input_filename = "noaa-adcp-201501.csv"

    output_path = OSUtils.cpp_project_path() + "/test_files"
    output_filename = "noaa-adcp-201501_2cols.csv"

    csv_reader = CSVReader(input_path, input_filename)
    csv_writer = CSVWriter(output_path, output_filename)

    iterate(csv_reader, csv_writer)

    csv_reader.close()
    csv_writer.close()

########################################################################################################################
########################################################################################################################
########################################################################################################################
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
    # print [current_line_count] + list_diff
    assert(list_diff[0] == 0)
    assert(max(list_diff) <= error_threshold)


def compare():
    test_files_path = OSUtils.cpp_project_path() + "/test_files"
    csv_reader_1 = CSVReader(OSUtils.datasets_csv_path() + "[1]irkis/", "vwc_1202.dat.csv")
    csv_reader_2 = CSVReader(test_files_path, "vwc_1202.dat.csv-CoderSF-Decode.csv")

    while csv_reader_1.continue_reading:
        assert(csv_reader_1.current_line_count == csv_reader_2.current_line_count)
        current_line_count = csv_reader_1.current_line_count

        line_1 = csv_reader_1.read_line()
        line_2 = csv_reader_2.read_line()

        compare_lines(line_1, line_2, current_line_count)

    print "COMPARE SUCCESS!!"
    csv_reader_1.close()
    csv_reader_2.close()

########################################################################################################################


def check_match(line1, line2):
    values = ["Documents", "python scripts/compress/compress_script.py", "elapsed time"]
    found_match = False
    for value in values:
        if not found_match and value in line1:
            assert(value in line2)
            found_match = True
    return found_match


def check_stds(line1, line2):
    if line1 == line2:
        print "-"
        return

    print "diff line"
    values1 = line1[line1.find("[")+1:line1.find("]")].split(",")
    values2 = line1[line1.find("[")+1:line1.find("]")].split(",")

    for value in zip(values1, values2):
        assert(value[0] == value[1])

def compare_mac_ubuntu():
    path = "/Users/pablocerve/Documents/FING/Proyecto/results/avances-8/2-resultados-3-enero/"
    reader1 = TextFileReader(path + "mac/mask-true", "full-output-mask-true.txt")
    reader2 = TextFileReader(path + "ubuntu/mask-true", "full-output-mask-true.txt")

    assert(reader1.total_lines == reader2.total_lines)

    while reader1.continue_reading:
        line1 = reader1.read_line()
        line2 = reader2.read_line()

        if check_match(line1, line2):
            continue

        if "stds" in line1:
            assert("stds" in line2)
            check_stds(line1, line2)
            continue

        if line1 != line2:
            print line1
            print line2
        assert(line1 == line2)

    print "COMPARE SUCCESS!!"
    reader1.close()
    reader2.close()


########################################################################################################################

clean()
# compare()
# compare_mac_ubuntu()

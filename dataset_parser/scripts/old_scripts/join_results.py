import sys
sys.path.append('.')

from file_utils.csv_utils.csv_reader import CSVReader
from file_utils.csv_utils.csv_writer import CSVWriter


def copy_rows(input_csv, output_csv, number_of_rows):
    for _ in range(number_of_rows):
        output_csv.write_row(input_csv.read_line())

path = "/Users/pablocerve/Documents/FING/Proyecto/results/"


def join12():
    results1_path, results1_filename = path + "results1", "results.csv"
    results2_path, results2_filename = path + "results2", "results.csv"
    joined_results_path, joined_results_filename = path, "resultsjoin.csv"

    results1 = CSVReader(results1_path, results1_filename)
    results2 = CSVReader(results2_path, results2_filename)
    joined_results = CSVWriter(joined_results_path, joined_results_filename)

    # read header
    line1 = results1.read_line()
    line2 = results2.read_line()
    joined_results.write_row(line1)
    assert(line1 == line2)

    while True:
        continue_reading = results1.continue_reading and results2.continue_reading
        if not continue_reading:
            break

        line1 = results1.read_line()
        line2 = results2.read_line()

        assert(line1[3] == "CoderBase")
        assert(line1 == line2)

        joined_results.write_row(line1)

        for _ in range(2):  # CoderPCA and CoderAPCA
            copy_rows(results1, joined_results, 4)

            line2 = results2.read_line()
            assert(line2[3] == "CoderPCA" or line2[3] == "CoderAPCA")
            line2[3] = ""
            joined_results.write_row(line2)
            copy_rows(results2, joined_results, 10)

            for _ in range(4):
                copy_rows(results1, joined_results, 4)
                copy_rows(results2, joined_results, 1)

    results1.close()
    results2.close()
    joined_results.close()

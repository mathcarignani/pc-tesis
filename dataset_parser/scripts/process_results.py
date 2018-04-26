import sys
sys.path.append('.')

from file_utils.csv_utils.csv_reader import CSVReader
from file_utils.csv_utils.csv_writer import CSVWriter

input_path = "/Users/pablocerve/Documents/FING/Proyecto/pc-tesis/dataset_parser/scripts/output/"


def get_best(line, index, best_perc, best_window, best_row):
    perc = float(line[index])
    window = line[6]
    if best_perc is None or perc < best_perc:
        return [perc, window, line]
    else:
        return [best_perc, best_window, best_row]


def print_best_windows(csv_writer, current_coder, best_windows, best_values):
    if current_coder and len(best_windows) > 0:
        csv_writer.write_row([''] * 2 + [current_coder] + best_windows + [''] + best_values)
    return [], []


def update_arrays(best_perc, best_window, best_windows, best_values):
    if best_perc is not None:
        best_windows.append(best_window)
        best_values.append(best_perc)
    return [None, best_windows, best_values]


def process(input_folder, input_filename, output_filename, index):
    full_path = input_path + '/' + input_folder
    csv_reader = CSVReader(full_path, input_filename)
    csv_writer = CSVWriter(full_path, output_filename)

    percentages = [0, 3, 5, 10, 15, 20, 30]
    csv_writer.write_row(["Dataset", "Filename", "Coder"] + percentages + [''] + percentages)

    current_coder = None
    best_windows, best_values = [], []
    best_perc, best_window, best_row = [None] * 3

    while csv_reader.continue_reading:
        line = csv_reader.read_line()

        if len(line[1]) > 0:
            if line[1] != 'Filename':  # CoderBasic row
                best_perc, best_windows, best_values = update_arrays(best_perc, best_window, best_windows, best_values)
                best_windows, best_values = print_best_windows(csv_writer, current_coder, best_windows, best_values)
                out_row = line[:2] + [line[4]]
                csv_writer.write_row(out_row)
            continue

        coder = line[3]
        if len(coder) > 0:  # CoderPCA, CoderAPCA or CoderCA row
            best_perc, best_windows, best_values = update_arrays(best_perc, best_window, best_windows, best_values)
            best_windows, best_values = print_best_windows(csv_writer, current_coder, best_windows, best_values)
            current_coder = coder
            best_perc = None

        perc = line[4]
        if len(perc) > 0:  # new percentage
            best_perc, best_windows, best_values = update_arrays(best_perc, best_window, best_windows, best_values)

        best_perc, best_window, best_row = get_best(line, index, best_perc, best_window, best_row)

    best_perc, best_windows, best_values = update_arrays(best_perc, best_window, best_windows, best_values)
    print_best_windows(csv_writer, current_coder, best_windows, best_values)

# process("[1]irkis", "results1_irkis.csv", "results1_irkis-col.csv", 12)
process("[2]noaa-sst", "results2_noaa-sst.csv", "results2_noaa-sst-col.csv", 12)

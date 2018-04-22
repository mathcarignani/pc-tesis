import math

import sys
sys.path.append('.')

from file_utils.csv_utils.csv_reader import CSVReader
from file_utils.csv_utils.csv_writer import CSVWriter
from scripts.utils import csv_files_filenames


def calculate_stats(csv_reader, columns_count):
    totals = [0] * columns_count
    counts = [0] * columns_count
    mins = [None] * columns_count
    maxs = [None] * columns_count

    while csv_reader.continue_reading:
        line = csv_reader.read_line()
        for i, item in enumerate(line):
            if item == 'N':
                continue
            value = int(item)
            totals[i] += value
            counts[i] += 1
            mins[i] = value if mins[i] is None or value < mins[i] else mins[i]
            maxs[i] = value if maxs[i] is None or value > maxs[i] else maxs[i]
    return totals, counts, mins, maxs


def calculate_means(csv_reader):
    csv_reader.goto_row(3)  # columns
    columns_count = len(csv_reader.read_line())
    totals, counts, mins, maxs = calculate_stats(csv_reader, columns_count)

    means = [0] * columns_count
    for i, total in enumerate(totals):
        count = float(counts[i])
        means[i] = 'N' if count == 0 else float(total) / float(count)
    # print "totals", totals
    # print "means", means
    # print "mins", mins
    # print "maxs", maxs
    return counts, means


def calculate_summs(csv_reader, means, columns_count):
    summs = [0] * columns_count
    while csv_reader.continue_reading:
        line = csv_reader.read_line()
        for i, item in enumerate(line):
            if item == 'N':
                continue
            value = float(item)
            value = (value - means[i]) ** 2
            summs[i] += value
    return summs


def calculate_stds(csv_reader, counts, means):
    csv_reader.goto_row(4)  # first data row

    columns_count = len(counts)
    summs = calculate_summs(csv_reader, means, columns_count)

    stds = [0] * columns_count
    for i, summ in enumerate(summs):
        # print 'summ', summ
        # print 'totals[i]', counts[i]
        stds[i] = 'N' if counts[i] == 0 else math.sqrt(summ / counts[i])

    print 'stds', stds
    return stds


def calculate_file_stats(input_path, input_filename):
    csv_reader = CSVReader(input_path, input_filename)
    print input_path + '/' + input_filename
    counts, means = calculate_means(csv_reader)
    stds = calculate_stds(csv_reader, counts, means)
    csv_reader.close()
    return stds


def calculate_folder_stats(input_path):
    stds_arrays = []
    for i, filename in enumerate(csv_files_filenames(input_path)):
        file_stds = calculate_file_stats(input_path, filename)
        stds_arrays.append([filename] + file_stds)
    return stds_arrays


def irkis():
    input_path = "/Users/pablocerve/Documents/FING/Proyecto/datasets-csv/[1]irkis"
    stds_arrays = calculate_folder_stats(input_path)

    percentages = [0, 3, 5, 10, 15, 20, 30]

    output_path = "/Users/pablocerve/Documents/FING/Proyecto/pc-tesis/dataset_parser/scripts/output"
    output_filename = "out.csv"
    csv_write = CSVWriter(output_path, output_filename)

    # header
    cols = ["Filename", "Time Delta"]
    for col_id in range(1, len(stds_arrays[0]) - 1):
        cols.append("Column %s" % col_id)
    csv_write.write_row(cols)

    for std_array in stds_arrays:
        row = ['N' if value == 'N' else round(value, 2) for value in std_array[1:]]
        csv_write.write_row([std_array[0]] + row)

    for percentage in percentages:
        csv_write.write_row(["%s %%" % percentage])
        div_percentage = float(percentage) / 100

        for std_array in stds_arrays:
            row = ['N' if value == 'N' else round(value * div_percentage, 0) for value in std_array[1:]]
            csv_write.write_row([std_array[0]] + row)

    csv_write.close()

irkis()

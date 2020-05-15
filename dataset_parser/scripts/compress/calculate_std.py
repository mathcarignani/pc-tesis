import math

import sys
sys.path.append('.')

from file_utils.csv_utils.csv_reader import CSVReader
from file_utils.csv_utils.csv_writer import CSVWriter
from scripts.utils import csv_files_filenames
from scripts.compress.experiments_utils import ExperimentsUtils


class CalculateSTD:
    @classmethod
    def calculate_file_stats(cls, input_path, input_filename):
        csv_reader = CSVReader(input_path, input_filename)
        print(input_path + '/' + input_filename)
        counts, means = cls._calculate_means(csv_reader)
        stds = cls._calculate_stds(csv_reader, counts, means)
        csv_reader.close()
        return stds

    @classmethod
    def calculate_stds_percentages(cls, stds, percentages):
        res = []
        for percentage in percentages:
            div_percentage = percentage / 100
            row = ['N' if value == 'N' else int(round(value * div_percentage, 0)) for value in stds[1:]]
            row.insert(0, 0)  # the error threshold for the timedelta is always 0
            res.append({'percentage': percentage, 'values': row})
        return res

    @classmethod
    def _calculate_means(cls, csv_reader):
        csv_reader.goto_row(3)  # columns
        columns_count = len(csv_reader.read_line())
        totals, counts, mins, maxs = cls._calculate_stats(csv_reader, columns_count)

        means = [0] * columns_count
        for i, total in enumerate(totals):
            count = float(counts[i])
            means[i] = 'N' if count == 0 else total / count
        return counts, means

    @classmethod
    def _calculate_stats(cls, csv_reader, columns_count):
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


    @classmethod
    def _calculate_stds(cls, csv_reader, counts, means):
        csv_reader.goto_first_data_row()

        columns_count = len(counts)
        summs = cls._calculate_summs(csv_reader, means, columns_count)

        stds = [0] * columns_count
        for i, summ in enumerate(summs):
            stds[i] = 'N' if counts[i] == 0 else math.sqrt(summ // counts[i])

        print('stds', stds)
        return stds

    @classmethod
    def _calculate_summs(cls, csv_reader, means, columns_count):
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


# TODO: remove
def calculate_folder_stats(input_path):
    stds_arrays = []
    for i, filename in enumerate(csv_files_filenames(input_path)):
        file_stds = CalculateSTD.calculate_file_stats(input_path, filename)
        stds_arrays.append([filename] + file_stds)
    return stds_arrays

def irkis():
    input_path = "/Users/pablocerve/Documents/FING/Proyecto/datasets-csv/[1]irkis"
    stds_arrays = calculate_folder_stats(input_path)

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

    for percentage in ExperimentsUtils.THRESHOLDS:
        csv_write.write_row(["%s %%" % percentage])
        div_percentage = float(percentage) / 100

        for std_array in stds_arrays:
            row = ['N' if value == 'N' else round(value * div_percentage, 0) for value in std_array[1:]]
            csv_write.write_row([std_array[0]] + row)

    csv_write.close()

# irkis()

#
# TODO: remove this file after writing the thesis, since we only use it to check against the stds obtained by
# the CompressUtils class
#
import math

import sys
sys.path.append('.')

from file_utils.csv_utils.csv_reader import CSVReader
from pandas_tools.pandas_tools import PandasTools


class CalculateSTDManual:
    @classmethod
    def calculate_stds(cls, input_path, input_filename, first_data_row):
        csv_reader = CSVReader(input_path, input_filename)
        counts, means = cls._calculate_means(csv_reader, first_data_row)
        stds = cls._calculate_stds(csv_reader, counts, means)
        csv_reader.close()
        return stds

    @classmethod
    def _calculate_means(cls, csv_reader, first_data_row):
        csv_reader.goto_row(first_data_row)  # columns
        columns_count = len(csv_reader.read_line())
        totals, counts, mins, maxs = cls._calculate_stats(csv_reader, columns_count)

        means = [0] * columns_count
        for i, total in enumerate(totals):
            count = float(counts[i])
            means[i] = PandasTools.NO_DATA if count == 0 else total / count
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
                if item == PandasTools.NO_DATA:
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
            stds[i] = PandasTools.NO_DATA if counts[i] == 0 else math.sqrt(summ / counts[i]) # TODO: // in python 2 = / in python 3

        print('stds', stds)
        return stds

    @classmethod
    def _calculate_summs(cls, csv_reader, means, columns_count):
        summs = [0] * columns_count
        while csv_reader.continue_reading:
            line = csv_reader.read_line()
            for i, item in enumerate(line):
                if item == PandasTools.NO_DATA:
                    continue
                value = float(item)
                value = (value - means[i]) ** 2
                summs[i] += value
        return summs

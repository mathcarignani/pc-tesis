import sys
sys.path.append('.')

import numpy as np
import math
from matplotlib import pyplot as plt

from file_utils.csv_utils.csv_reader import CSVReader
from scripts.compress.experiments_utils import ExperimentsUtils
from scripts.utils import csv_files_filenames


def read_data(input_path, input_filename, column_index):
    data = []
    data = np.array(data)

    csv_file = CSVReader(input_path, input_filename)
    csv_file.goto_row(3)
    column_name = csv_file.read_line()[column_index]
    csv_file.goto_first_data_row()
    while csv_file.continue_reading:
        value = csv_file.read_line()[column_index]
        data = np.append(data, float(value))

    return [column_name, data]


def make_histogram(input_path, input_filename, column_index=0):
    column_name, data = read_data(input_path, input_filename, column_index)
    title = "FILE: '" + input_filename + "' | COL: '" + column_name + "' (col index=" + str(column_index) + ")"
    figure_path = input_path + "/" + "histo-" + input_filename.replace(".csv", "") + "-col" + str(column_index) + "--.png"

    # print data
    #
    # SOURCE: https://stackoverflow.com/a/24814204/4547232
    #
    # data = np.random.normal(0, 20, 1000)

    number_of_bins = 100  # fixed number of bins
    max_bin = 100  # math.floor(max(data))
    bins = np.linspace(math.ceil(min(data)), max_bin, number_of_bins)

    max_lim = 100  # max(data)
    plt.xlim([min(data)-5, max_lim+5])

    plt.hist(data, bins=bins, alpha=1)

    plt.title(title)
    plt.xlabel('variable X (20 evenly spaced bins)')
    plt.ylabel('count')

    plt.savefig(figure_path)
    # plt.show()


def make_all_histograms():
    for dataset_dictionary in ExperimentsUtils.DATASETS_ARRAY:
        print dataset_dictionary['name']
        if "SPC" not in dataset_dictionary['name']:
            continue
        input_path = ExperimentsUtils.CSV_PATH + dataset_dictionary['folder']
        for input_filename in csv_files_filenames(input_path):
            print input_filename
            make_histogram(input_path, input_filename)
        print

make_all_histograms()


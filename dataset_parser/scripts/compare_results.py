import sys
sys.path.append('.')

from file_utils.csv_utils.csv_reader import CSVReader
from file_utils.csv_utils.csv_writer import CSVWriter


datasets = ["IRKIS", "NOAA-SST", "NOAA-ADCP", "SolarAnywhere", "ElNino", "NOAA-SPC-hail", "NOAA-SPC-tornado", "NOAA-SPC-wind"]

root_path = "/Users/pablocerve/Documents/FING/Proyecto/results/avances-dudas-5/"

original_folder_path = root_path + "1-output1/"
original_dataset_path = {
    "IRKIS": "[1]irkis",
    "NOAA-SST": "[2]noaa-sst",
    "NOAA-ADCP": "[3]noaa-adcp",
    "SolarAnywhere": "[4]solar-anywhere",
    "ElNino": "[5]el-nino",
    "NOAA-SPC-hail": "[6]noaa-spc-reports-hail",
    "NOAA-SPC-tornado": "[6]noaa-spc-reports-tornado",
    "NOAA-SPC-wind": "[6]noaa-spc-reports-wind"
}

pwlh_mod_folder = root_path + "2-PWLH-with-delta-results/"
ca_mod_folder = root_path + "3-CA-with-delta-results/"
pca_mask_folder = root_path + "4-PCA-with-no-data-mask/"

########################################################################################################################


#
# Given a results.csv file, this scripts creates a new csv file which filters out the results from algorithms
# which are not in the algorithms_array
#
def filter_dataset(original_path, original_filename, csv_writer, algorithms_array, print_header=False):
    csv_reader = CSVReader(original_path, original_filename)

    matching_algorithm = False
    while csv_reader.continue_reading:
        line = csv_reader.read_line()

        filename, algorithm_name = line[1], line[3]

        if len(algorithm_name) > 0:
            if matching_algorithm and algorithm_name not in algorithms_array:
                matching_algorithm = False
            elif not matching_algorithm and algorithm_name in algorithms_array:
                matching_algorithm = True

        if line[0] == "Dataset":
            if print_header:
                csv_writer.write_row(line)
        elif len(filename) > 0 or matching_algorithm:
            csv_writer.write_row(line)

    csv_reader.close()


def filter_datasets(input_path, csv_writer, algorithms_array):
    for idx, dataset in enumerate(datasets):
        # print dataset
        folder_path = input_path + original_dataset_path[dataset]
        filter_dataset(folder_path, "results.csv", csv_writer, algorithms_array, idx == 0)
    csv_writer.close()

########################################################################################################################


def parse_line(line):
    first_col, last_col = 7, 11
    return line[:first_col] + line[last_col:]


def c_int(value):
    return int(value.replace('.', ''))


def diff_scenarios(diff_value):
    string = ""
    abs_diff = abs(diff_value)
    if abs_diff > 0:
        sign_string = '-' if diff_value < 0 else '+'
        range_string = '0'

        for val in [30, 20, 15, 10, 5, 1]:
            if abs_diff > val:
                range_string = str(val)
                break
        string = "DIFF" + sign_string + range_string + sign_string + " "  # example: "DIFF+30+"
    return string + str(diff_value)


def write_params_line(csv_writer, original_line, results_line):
    info_line = original_line[:6]
    csv_writer.write_row(info_line)
    original_line[:6] = [None] * 6
    results_line[:6] = [None] * 6
    return original_line, results_line


def compare_results(folder):
    original = CSVReader(folder, "results-original.csv")
    results = CSVReader(folder, "results.csv")
    csv_writer = CSVWriter(folder, "results-merge.csv")

    assert(original.total_lines == results.total_lines)

    while original.continue_reading:
        original_line = original.read_line()
        results_line = results.read_line()

        coder_name = original_line[3]
        if len(coder_name) > 0 and coder_name in ["Coder", "CoderBasic"]:
            assert(original_line == results_line)
            csv_writer.write_row(parse_line(original_line))
        else:
            if len(original_line[4]) > 0:  # algorithm params line
                original_line, results_line = write_params_line(csv_writer, original_line, results_line)
            original_line = parse_line(original_line)
            results_line = parse_line(results_line)

            # if original_line == results_line:
            #     continue

            csv_writer.write_row(['O'] + original_line[1:] + ['O'])
            csv_writer.write_row(['M'] + results_line[1:] + ['M'])

            diff = []
            for i in range(7, len(original_line)):
                original_value, results_value = original_line[i], results_line[i]
                if i % 2 == 0:
                    # floats (percentages)
                    # diff_value = results_value + ' - ' + original_value
                    diff_value = float(results_value) - float(original_value)
                    diff_value = diff_scenarios(diff_value)
                else:
                    # integers (bits)
                    if original_value == results_value:
                        diff_value = '==='
                    else:
                        diff_value = c_int(results_value) - c_int(original_value)
                        diff_value = '+++' + str(diff_value) if diff_value > 0 else '---' + str(diff_value)
                diff.append(diff_value)
            diff_line = original_line[:7] + diff
            csv_writer.write_row(diff_line)

    original.close()
    results.close()
    csv_writer.close()


########################################################################################################################

# shared columns:
# Dataset,Filename,#rows,Coder,%,Error Threshold,Window Param,Size (B),CR (%),

# original
# Delta - Size (b),Delta - CR (%),Other columns - Size (b),Other columns - CR (%)

# PCA with mask column
# Delta - Size (data),Delta - Size (mask),Delta - Size (total),Delta - CR (%),Other columns - Size (data),Other columns - Size (mask),Other columns - Size (total),Other columns - CR (%)


# INPUT:
#                                    *          *         *      *      *         *        *        *                            *         *                           *        *
# ['', '', '', '', '', '', '200', '282.398', '99.82', '684420', '0', '684420', '100.0', '523582', '2835', '526417', '100.04', '563842', '2835', '566677', '100.04', '478546', '2835', '481381', '99.06']
# OUTPUT:
# ['', '', '', '', '', '', '200', '526417', '100.04', '566677', '100.04', '481381', '99.06']


def parse_mask_line(line):
    first_col, last_col = 7, 13
    line = line[:first_col] + line[last_col:]
    new_line = line[:7]
    for idx, i in enumerate(line[7:]):
        if (idx + 2) % 4 == 0:  # 2, 6, 10, 14, etc. => values
            i = "{:,}".format(int(i)).replace(',', '.')  # '526417' = '526.417'
            new_line.append(i)
        elif (idx + 1) % 4 == 0:  # 3, 7, 11, 15, etc. => percentages
            new_line.append(i)
    return new_line


def compare_pca_results():
    original = CSVReader(pca_mask_folder, "results-original.csv")
    results = CSVReader(pca_mask_folder, "results-mask.csv")
    csv_writer = CSVWriter(pca_mask_folder, "results-merge.csv")

    assert(original.total_lines == results.total_lines)

    while original.continue_reading:
        original_line = original.read_line()
        results_line = results.read_line()

        coder_name = original_line[3]
        if coder_name in ["Coder", "CoderBasic"]:
            # assert(original_line == results_line)
            csv_writer.write_row(parse_line(original_line))
        else:
            if len(original_line[4]) > 0:  # algorithm params line
                original_line, results_line = write_params_line(csv_writer, original_line, results_line)
            original_line = parse_line(original_line)
            results_line = parse_mask_line(results_line)

            # if original_line == results_line:
            #     continue

            csv_writer.write_row(['O'] + original_line[1:] + ['O'])
            csv_writer.write_row(['M'] + results_line[1:] + ['M'])

            diff = []
            for i in range(7, len(original_line)):
                original_value, results_value = original_line[i], results_line[i]
                if i % 2 == 0:
                    # floats (percentages)
                    # diff_value = results_value + ' - ' + original_value
                    diff_value = float(results_value) - float(original_value)
                    diff_value = diff_scenarios(diff_value)
                else:
                    # integers (bits)
                    if original_value == results_value:
                        diff_value = '==='
                    else:
                        diff_value = c_int(results_value) - c_int(original_value)
                        diff_value = '+++' + str(diff_value) if diff_value > 0 else '---' + str(diff_value)
                diff.append(diff_value)
            diff_line = original_line[:7] + diff
            csv_writer.write_row(diff_line)

    original.close()
    results.close()
    csv_writer.close()


########################################################################################################################

#
# EXPERIMENTOS AVANCES / DUDAS (V)
#

# filter_datasets(original_folder_path, CSVWriter(pwlh_mod_folder, "results-original.csv"), ["CoderPWLH", "CoderPWLHint"])
compare_results(pwlh_mod_folder)

# filter_datasets(original_folder_path, CSVWriter(ca_mod_folder, "results-original.csv"), ["CoderCA"])
# compare_results(ca_mod_folder)

# filter_datasets(original_folder_path, CSVWriter(pca_mask_folder, "results-original.csv"), ["CoderPCA"])
# filter_datasets(pca_mask_folder, CSVWriter(pca_mask_folder, "results-mask.csv"), ["CoderPCA"])
# compare_pca_results()
import sys
sys.path.append('.')

from file_utils.csv_utils.csv_reader import CSVReader
from file_utils.csv_utils.csv_writer import CSVWriter
from scripts.compress.compress_aux import THRESHOLD_PERCENTAGES

percentages = THRESHOLD_PERCENTAGES
percentages_len = len(percentages)
coders_len = 5
coder_index = 2


def calculate_results(csv_reader, csv_writer):
    csv_reader.read_line()  # ignore headers
    row = csv_reader.read_line()

    dataset = row[0]
    output_header(csv_writer, dataset)

    csv_reader.goto_row(1)
    while csv_reader.continue_reading:
        row = csv_reader.read_line()
        print row
        results = calculate_results_file(row)
        csv_writer.write_row(results)
    csv_writer.write_row([])


def output_header(csv_writer, dataset):
    csv_writer.write_row([dataset])
    row = ['FILENAME / STD']
    for percentage in percentages:
        row += ['', percentage, '']
    csv_writer.write_row(row)


def get_values(coders_array, c_index, percentage_index):
    coder = coders_array[c_index]
    name = coder['name']
    window = int(coder['windows'][percentage_index])
    val = float(coder['crs'][percentage_index])
    return [name, window, val]


def create_coders_array():
    coders_array = []
    for _ in range(coders_len):
        row = csv_reader.read_line()
        coder_name = row[coder_index].replace("CoderCA", "CA1").replace("CoderAPCA", "APCA2").replace("CoderPCA", "PCA3")
        row = row[coder_index+1:]
        coders_array.append({'name': coder_name, 'windows': row[0:percentages_len], 'crs': row[-percentages_len:]})
    return coders_array


def create_results_row(coders_array):
    out_row = []
    for percentage_index in range(percentages_len):
        best_name, best_window, best_val = None, None, None
        for c_index in range(coders_len):
            name, window, val = get_values(coders_array, c_index, percentage_index)
            if best_val is None or val < best_val:
                best_name, best_window, best_val = name, window, val
        out_row += [best_name, str(best_val) + '%', best_window]
    return out_row


def calculate_results_file(row):
    filename = row[1]

    coders_array = create_coders_array()
    out_row = create_results_row(coders_array)

    out_row = [filename] + out_row
    return out_row


input_path = "/Users/pablocerve/Documents/FING/Proyecto/results/avances-dudas-4/results/MERGED_RESULTS2/cols"
output_file = "PROCESS_RESULTS2-cols.csv"
filenames = [
    "results1_irkis-col.csv",
    "results2_noaa-sst-col.csv",
    "results3_noaa-adcp-col.csv",
    "results4_solar-anywhere-col1.csv",
    "results4_solar-anywhere-col2.csv",
    "results4_solar-anywhere-col3.csv",
    "results5_el-nino-col1.csv",
    "results5_el-nino-col2.csv",
    "results5_el-nino-col3.csv",
    "results5_el-nino-col4.csv",
    "results5_el-nino-col5.csv",
    "results5_el-nino-col6.csv",
    "results5_el-nino-col7.csv",
    "results6_noaa-spc-hail-col1.csv",
    "results6_noaa-spc-hail-col2.csv",
    "results6_noaa-spc-hail-col3.csv",
    "results7_noaa-spc-tornado-col1.csv",
    "results7_noaa-spc-tornado-col2.csv",
    "results8_noaa-spc-wind-col1.csv",
    "results8_noaa-spc-wind-col2.csv",
    "results8_noaa-spc-wind-col3.csv"
]

# input_path = "/Users/pablocerve/Documents/FING/Proyecto/results/avances-dudas-4/results/MERGED_RESULTS2/td"
# output_file = "PROCESS_RESULTS2-td.csv"
# filenames = [
#     "results1_irkis-td.csv",
#     "results2_noaa-sst-td.csv",
#     "results3_noaa-adcp-td.csv",
#     "results4_solar-anywhere-td.csv",
#     "results5_el-nino-td.csv",
#     "results6_noaa-spc-hail-td.csv",
#     "results7_noaa-spc-tornado-td.csv",
#     "results8_noaa-spc-wind-td.csv",
# ]
csv_writer = CSVWriter(input_path, output_file)
for filename in filenames:
    csv_reader = CSVReader(input_path, filename)
    calculate_results(csv_reader, csv_writer)
    csv_reader.close()
csv_writer.close()


# PAPER-OUTPUT
# input_path = "/Users/pablocerve/Documents/FING/Proyecto/pc-tesis/dataset_parser/scripts/paper-output/results"
# csv_writer = CSVWriter(input_path, "RESULTS.csv")
# csv_reader = CSVReader(input_path, "results1+2.process_results.out.csv")
# calculate_results(csv_reader, csv_writer)
# csv_writer.close()

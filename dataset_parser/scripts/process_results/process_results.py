import sys
sys.path.append('.')

from file_utils.csv_utils.csv_reader import CSVReader
from file_utils.csv_utils.csv_writer import CSVWriter
from scripts.compress.compress_aux import THRESHOLD_PERCENTAGES
from auxi.os_utils import python_project_path

input_path = python_project_path() + "/scripts/compress/output/all-mask-false"

window_index = 6

# Other columns - CR (%) index
column_indexes = {
    'IRKIS': [{'index': 16, 'name': 'VWC'}],
    'NOAA-SST': [{'index': 16, 'name': 'SST'}],
    'NOAA-ADCP': [{'index': 16, 'name': 'Vel'}],
    'SolarAnywhere': [{'index': 16, 'name': 'GHI'}, {'index': 20, 'name': 'DNI'}, {'index': 24, 'name': 'DHI'}],
    'ElNino': [{'index': 16, 'name': 'Lat'}, {'index': 20, 'name': 'Long'}, {'index': 24, 'name': 'Zonal Winds'}, {'index': 28, 'name': 'Merid. Winds'},
               {'index': 32, 'name': 'Humidity'}, {'index': 36, 'name': 'AirTemp'}, {'index': 40, 'name': 'SST'}],
    'NOAA-SPC-hail': [{'index': 16, 'name': 'Lat'}, {'index': 20, 'name': 'Long'}, {'index': 24, 'name': 'Size'}],
    'NOAA-SPC-tornado': [{'index': 16, 'name': 'Lat'}, {'index': 20, 'name': 'Long'}],
    'NOAA-SPC-wind': [{'index': 16, 'name': 'Lat'}, {'index': 20, 'name': 'Long'}, {'index': 24, 'name': 'Speed'}]
}


def thresholds_array():
    array = []
    for threshold in THRESHOLD_PERCENTAGES:
        array += [None, None, str(threshold) + " (%)", None]
    return array


def second_line():
    array = []
    for _ in THRESHOLD_PERCENTAGES:
        array += [None, "Coder", "Win", "CR (%)"]
    return array


class Script1Read(object):
    def __init__(self, input_filename):
        self.csv_reader = CSVReader(input_path, input_filename)
        self.hash = {'Datasets': []}
        self.dataset_hash = None
        self.file_hash = None
        self.coder_hash = None
        self.thresholds_hash = None

    def get_hash(self):
        while self.csv_reader.continue_reading:
            # Dataset	Filename	#rows	Coder	%	ErrorThreshold	WindowParam
            line = self.csv_reader.read_line()

            if line[0] == "Dataset":  # First row
                continue

            if len(line[0]) > 0:  # Dataset name
                self.read_dataset_name(line[0])

            if len(line[1]) > 0:  # Filename
                self.read_filename(line[1])
                continue

            if len(line[3]) > 0:  # Coder
                self.read_coder(line[3])

            if len(line[4]) > 0:  # %
                self.read_threshold(line[4])

            if len(line[6]) > 0:  # Window Param
                self.read_window_param(line)

        self.csv_reader.close()
        return self.hash

    def read_dataset_name(self, dataset_name):
        self.dataset_hash = {'Dataset': dataset_name, 'Files': []}
        self.hash['Datasets'].append(self.dataset_hash)

    def read_filename(self, filename):
        self.file_hash = {'Filename': filename, 'Coders': []}
        self.dataset_hash['Files'].append(self.file_hash)

    def read_coder(self, coder_name):
        self.coder_hash = {'Coder': coder_name, 'Thresholds': []}
        self.file_hash['Coders'].append(self.coder_hash)

    def read_threshold(self, threshold):
        self.thresholds_hash = {'Threshold': threshold, 'Window Params': []}
        self.coder_hash['Thresholds'].append(self.thresholds_hash)

    def read_window_param(self, line):
        window_param = int(line[6])
        columns = column_indexes[self.dataset_hash['Dataset']]
        col_hash = {}
        for col in columns:
            index, col_name = col['index'], col['name']
            percentage = float(line[index])
            col_hash[col_name] = percentage

        window_params_hash = {'Window Param': window_param, 'Columns': col_hash}
        self.thresholds_hash['Window Params'].append(window_params_hash)


class Script1Write(object):
    def __init__(self, output_filename1, output_filename2, hash):
        self.csv_writer1 = CSVWriter(input_path, output_filename1)
        self.csv_writer2 = CSVWriter(input_path, output_filename2)
        self.hash = hash
        self.dataset_name = None
        self.column_name = None
        self.file = None
        self.coder_name = None

    def write(self):
        row = ["Dataset", "Filename", "Column", "Coder"] + THRESHOLD_PERCENTAGES + [''] + THRESHOLD_PERCENTAGES
        self.csv_writer1.write_row(row)
        self.csv_writer2.write_row(["Dataset", "Filename", "Column"] + thresholds_array())
        self.csv_writer2.write_row([None, None, None] + second_line())

        for dataset_hash in self.hash['Datasets']:
            self.write_dataset(dataset_hash)

        self.csv_writer1.close()
        self.csv_writer2.close()

    def write_dataset(self, dataset_hash):
        print dataset_hash['Dataset']
        self.dataset_name = dataset_hash['Dataset']
        self.csv_writer1.write_row([self.dataset_name])
        self.csv_writer2.write_row([self.dataset_name])

        for self.file in dataset_hash['Files']:
            self.write_file()

    def write_file(self):
        print " " * 2 + self.file['Filename']
        self.csv_writer1.write_row([None, self.file['Filename']])
        self.csv_writer2.write_row([None, self.file['Filename']])

        for column in column_indexes[self.dataset_name]:
            self.write_columns(column)

    def write_columns(self, column):
        self.column_name = column['name']
        print " " * 4 + self.column_name
        self.csv_writer1.write_row([None, None, self.column_name])
        self.print_line(column)

        for coder in self.file['Coders']:
            self.write_coder(coder)

    def write_coder(self, coder):
        self.coder_name = coder['Coder']
        print " " * 6 + self.coder_name
        best_windows, best_percentages = [], []

        for threshold in coder['Thresholds']:
            print " " * 8 + threshold['Threshold']
            self.get_best_values(threshold, best_windows, best_percentages)

        self.csv_writer1.write_row([None, None, None, self.coder_name] + best_windows + [None] + best_percentages)

    def get_best_values(self, threshold, best_windows, best_percentages):
        best_window, best_percentage = 1000, 1000

        for params in threshold['Window Params']:
            col_percentage = params['Columns'][self.column_name]
            print " " * 10 + str(params['Window Param']) + " => " + str(col_percentage)
            if col_percentage < best_percentage:
                best_window = params['Window Param']
                best_percentage = col_percentage
        print " " * 10 + str(best_window) + " => " + str(best_percentage) + " ***"
        best_windows.append(best_window)
        best_percentages.append(best_percentage)

    def get_best_values_for_threshold(self, threshold, column):
        best_coder, best_window, best_percentage = None, None, None

        for coder in self.file['Coders']:
            for threshold_hash in coder['Thresholds']:
                if int(threshold_hash['Threshold']) != int(threshold):
                    continue

                for window_param in threshold_hash['Window Params']:
                    window = window_param['Window Param']
                    percentage = window_param['Columns'][column['name']]

                    if best_coder is None or percentage < best_percentage:
                        best_coder = coder['Coder']
                        best_window = window
                        best_percentage = percentage
        return best_coder, best_percentage, best_window

    def print_line(self, column):
        array = []
        for threshold in THRESHOLD_PERCENTAGES:
            best_coder, best_percentage, best_window = self.get_best_values_for_threshold(threshold, column)
            array += [None, best_coder, best_window, best_percentage]
        self.csv_writer2.write_row([None, None, self.column_name] + array)


class Script1(object):
    def __init__(self, input_filename, output_filename1, output_filename2):
        hash = Script1Read(input_filename).get_hash()
        Script1Write(output_filename1, output_filename2, hash).write()

Script1("results.csv", "results_process1.csv", "results_process2.csv")







# TD
# process("results1_irkis.csv", "results1_irkis-td.csv", 10)
# process("results2_noaa-sst.csv", "results2_noaa-sst-td.csv", 10)
# process("results3_noaa-adcp.csv", "results3_noaa-adcp-td.csv", 10)
# process("results4_solar-anywhere.csv", "results4_solar-anywhere-td.csv", 10)
# process("results5_el-nino.csv", "results5_el-nino-td.csv", 10)
# process("results6_noaa-spc-hail.csv", "results6_noaa-spc-hail-td.csv", 10)
# process("results7_noaa-spc-tornado.csv", "results7_noaa-spc-tornado-td.csv", 10)
# process("results8_noaa-spc-wind.csv", "results8_noaa-spc-wind-td.csv", 10)

# PAPER-OUTPUT
# process("results1+2.csv", "results1+2.process_results.out.csv", 12)

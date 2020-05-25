import datetime

import sys
sys.path.append('.')

from auxi.logger import setup_logger
from file_utils.csv_utils.csv_writer import CSVWriter
from file_utils.text_utils.text_file_reader import TextFileReader
from pandas_tools.pandas_tools import PandasTools
from parsers.elnino.parser_elnino import ParserElNino


class Data:
    def __init__(self, count, timestamp, lat, longi):
        self.count = count
        self.timestamp = timestamp
        self.lat_min = self.lat_max = lat
        self.long_min = self.long_max = longi

    def update_dictionary(self, lat, longi):
        if lat < self.lat_min:
            self.lat_min = lat
        elif lat > self.lat_max:
            self.lat_max = lat

        if longi < self.long_min:
            self.long_min = longi
        elif longi > self.long_max:
            self.long_max = longi

    def dictionary_row(self, count, last_timestamp, buoy_count):
        row = [self.count, count, count - self.count + 1]  # counts
        row += [str(self.timestamp)[0:10], str(last_timestamp)[0:10]]  # timestamps
        row += [self.lat_min, self.lat_max]  # lat
        row += [self.long_min, self.long_max]  # long

        diff_lat = round(self.lat_max - self.lat_min, 2)
        diff_long = round(self.long_max - self.long_min, 2)
        row += [diff_lat, diff_long, buoy_count]
        return row


class DataFrameUtils:
    def __init__(self, parser, logger):
        self.parser = parser
        self.logger = logger
        self.pandas_tools = PandasTools(self.parser, self.logger)
        self.current_pandas_tools = None

    def buoy_start(self, new_buoy_id):
        print "new buoy", new_buoy_id
        columns = ["lat", "long", "ZonWinds", "MerWinds", "Humidity", "AirTemp", "SST"]
        columns = ["%s_%s" % (new_buoy_id, column) for column in columns]

        if new_buoy_id != 1:  # this is only False the first time this method is called
            self.buoy_end()

        self.current_pandas_tools = PandasTools(self.parser, self.logger)
        self.current_pandas_tools.new_df(columns, False)

    def add_row(self, timestamp, row):
        self.current_pandas_tools.add_row(timestamp, row)

    def buoy_end(self):
        self.pandas_tools.concat_df(self.current_pandas_tools.df)

    def df_to_output_csv(self, output_path, output_filename):
        # print stats
        self.pandas_tools.print_stats()
        # output to file
        output_file = CSVWriter(output_path, output_filename)
        output_file.write_row(['DATASET:', self.parser.NAME])
        output_file.write_row(['TIME UNIT:', 'hours'])
        output_file.write_row(['FIRST TIMESTAMP:', self.pandas_tools.first_timestamp()])
        row = ['Time Delta']
        row.extend(self.pandas_tools.df.columns)
        output_file.write_row(row)
        self.pandas_tools.df_to_csv(output_file, 'hours')
        output_file.close()


class Script:
    def __init__(self, text_file, csv_file1, csv_file2, parser, df_utils):
        self.text_file = text_file
        self.csv_file1 = csv_file1
        self.csv_file2 = csv_file2
        self.parser = parser
        self.df_utils = df_utils

        # loop variables
        self.buoy_count = 1
        self.count = 1
        self.last_timestamp = None
        self.dictionary = {}
        self.buoy_dictionary = {}

    def run_loop(self):
        min_max_values = [None] * 2 * 7
        while self.text_file.continue_reading:  # and self.count < 10289:
            line = self.text_file.read_line()
            data = self.parser.parse_data(line)  # {'timestamp': timestamp, 'values': data}
            timestamp = data['timestamp']
            lat, longi, zon_winds, mer_winds, humidity, air_temp, ss_temp = data['values']

            # calculate min and max for each column
            self.update_min_max_values(min_max_values, [lat, longi, zon_winds, mer_winds, humidity, air_temp, ss_temp])

            self.iteration(timestamp, lat, longi)
            self.df_utils.add_row(timestamp, [lat, longi, zon_winds, mer_winds, humidity, air_temp, ss_temp])

            self.last_timestamp = timestamp
            self.count += 1
        print min_max_values
        self.print_data(True)
        self.df_utils.buoy_end()

    @classmethod
    def update_min_max_values(cls, min_max_values, values):
        for idx, val in enumerate(values):
            if val != PandasTools.NO_DATA:
                val = float(val)
                if val > 0:
                    min_index, max_index = idx*2, idx*2 + 1
                    min_value, max_value = min_max_values[min_index], min_max_values[max_index]
                    if min_value is None:  # and max_value is None:
                        min_max_values[min_index] = val
                        min_max_values[max_index] = val
                    elif val < min_value:
                        min_max_values[min_index] = val
                    elif val > max_value:
                        min_max_values[max_index] = val

    def iteration(self, timestamp, lat, longi):
        if self.last_timestamp is None:  # first time the method is called
            self.dictionary = Data(self.count, timestamp, lat, longi)
            self.buoy_dictionary = Data(self.count, timestamp, lat, longi)
            self.df_utils.buoy_start(self.buoy_count)
        else:
            next_timestamp = self.last_timestamp + datetime.timedelta(days=1)
            if timestamp == next_timestamp:  # normal sequence, 1 day delta
                self.dictionary.update_dictionary(lat, longi)
                self.buoy_dictionary.update_dictionary(lat, longi)
            else:
                force_buoy_change = self.count in [142692, 144778]  # original buoys 59 and 61
                change_buoy = timestamp < self.last_timestamp or force_buoy_change
                if change_buoy:
                    self.print_data(True)
                    self.buoy_dictionary = Data(self.count, timestamp, lat, longi)
                    self.buoy_count += 1
                    self.df_utils.buoy_start(self.buoy_count)
                else:
                    self.print_data()
                self.dictionary = Data(self.count, timestamp, lat, longi)

    def print_data(self, change=False):
        row = self.dictionary.dictionary_row(self.count - 1, self.last_timestamp, self.buoy_count)
        self.csv_file1.write_row(row)

        if not change:
            return
        self.csv_file1.write_row([])  # separator empty row in csv_file1
        row = self.buoy_dictionary.dictionary_row(self.count - 1, self.last_timestamp, self.buoy_count)
        # diff_lat, diff_long = row[9:11]
        # if abs(diff_lat) >= 1 or abs(diff_long) >= 5:  # ony print weird scenarios
        self.csv_file2.write_row(row)

    def close(self):
        self.text_file.close()
        self.csv_file1.close()
        self.csv_file2.close()


def run():
    text_file = TextFileReader("/Users/pablocerve/Documents/FING/Proyecto/datasets/[5]el-nino/large/data", "tao-all2.dat")
    csv_file1 = CSVWriter("/Users/pablocerve/Documents/FING/Proyecto/pc-tesis/dataset_parser/scripts", "nino1.csv")
    csv_file2 = CSVWriter("/Users/pablocerve/Documents/FING/Proyecto/pc-tesis/dataset_parser/scripts", "nino2.csv")
    row = ["index_start", "index_end", "count", "timestamp_start", "timestamp_end", "min_lat", "max_lat", "min_long", "max_long", "dif_lat", "dif_long", "buoy_id"]
    csv_file1.write_row(row)
    csv_file2.write_row(row)
    parser = ParserElNino()

    logger = setup_logger('el-nino.log', 'el-nino.log')
    df_utils = DataFrameUtils(parser, logger)

    script = Script(text_file, csv_file1, csv_file2, parser, df_utils)
    script.run_loop()
    script.close()

    path = "/Users/pablocerve/Documents/FING/Proyecto/pc-tesis/dataset_parser/scripts/[5]el-nino"
    filename = "el-nino.csv"
    df_utils.df_to_output_csv(path, filename)

run()



import datetime

import sys
sys.path.append('.')

from file_utils.csv_utils.csv_writer import CSVWriter
from file_utils.text_utils.text_file_reader import TextFileReader
from parsers.elnino.parser_elnino import ParserElNino


def new_dictionary(count, timestamp, lat, longi):
    return {'count': count, 'timestamp': timestamp, 'lat': {'min': lat, 'max': lat}, 'longi': {'min': longi, 'max': longi}}


def update_dictionary(dictionary, lat, longi):
    if lat < dictionary['lat']['min']:
        dictionary['lat']['min'] = lat
    elif lat > dictionary['lat']['max']:
        dictionary['lat']['max'] = lat

    if longi < dictionary['longi']['min']:
        dictionary['longi']['min'] = longi
    elif longi > dictionary['longi']['max']:
        dictionary['longi']['max'] = longi


def dictionary_row(dictionary, count, last_timestamp, buoy_count):
    row = [dictionary['count'], count, count - dictionary['count'] + 1]  # counts
    row += [str(dictionary['timestamp'])[0:10], str(last_timestamp)[0:10]]  # timestamps
    row += [dictionary['lat']['min'], dictionary['lat']['max']]  # lat
    row += [dictionary['longi']['min'], dictionary['longi']['max']]  # long

    diff_lat = round(dictionary['lat']['max'] - dictionary['lat']['min'], 2)
    diff_long = round(dictionary['longi']['max'] - dictionary['longi']['min'], 2)
    row += [diff_lat, diff_long, buoy_count]
    return row


def print_data(csv_file1, csv_file2, dictionary, count, last_timestamp, buoy_count, buoy_dictionary, change=False):
    row = dictionary_row(dictionary, count, last_timestamp, buoy_count)
    csv_file1.write_row(row)

    if change:
        csv_file1.write_row([])  # separator empty row in csv_file1
        row = dictionary_row(buoy_dictionary, count, last_timestamp, buoy_count)
        diff_lat, diff_long = row[9:11]
        if abs(diff_lat) >= 1 or abs(diff_long) >= 5:  # ony print weird scenarios
            csv_file2.write_row(row)


def run_loop(text_file, csv_file1, csv_file2, parser):
    buoy_count = 1
    count = 1
    last_timestamp = None
    dictionary = {}
    buoy_dictionary = {}
    while text_file.continue_reading:  # and count < 5:
        line = text_file.read_line()
        data = parser.parse_data(line)  # {'timestamp': timestamp, 'values': data}
        timestamp = data['timestamp']
        lat, longi = data['values'][0:2]

        if last_timestamp is None:
            dictionary = new_dictionary(count, timestamp, lat, longi)
            buoy_dictionary = new_dictionary(count, timestamp, lat, longi)
        else:
            next_timestamp = last_timestamp + datetime.timedelta(days=1)
            if timestamp == next_timestamp:
                update_dictionary(dictionary, lat, longi)
                update_dictionary(buoy_dictionary, lat, longi)
            else:
                if timestamp < last_timestamp:
                    print_data(csv_file1, csv_file2, dictionary, count-1, last_timestamp, buoy_count, buoy_dictionary, True)
                    buoy_dictionary = new_dictionary(count, timestamp, lat, longi)
                    buoy_count += 1
                else:
                    print_data(csv_file1, None, dictionary, count-1, last_timestamp, buoy_count, buoy_dictionary)
                dictionary = new_dictionary(count, timestamp, lat, longi)

        last_timestamp = timestamp
        count += 1

    print_data(csv_file1, csv_file2, dictionary, count-1, last_timestamp, buoy_count, buoy_dictionary, True)


text_file = TextFileReader("/Users/pablocerve/Documents/FING/Proyecto/datasets/[5]el-nino/large/data", "tao-all2.dat")
csv_file1 = CSVWriter("/Users/pablocerve/Documents/FING/Proyecto/pc-tesis/dataset_parser/scripts", "nino1.csv")
csv_file2 = CSVWriter("/Users/pablocerve/Documents/FING/Proyecto/pc-tesis/dataset_parser/scripts", "nino2.csv")
csv_file1.write_row(["index_start", "index_end", "count", "timestamp_start", "timestamp_end", "min_lat", "max_lat", "min_long", "max_long", "dif_lat", "dif_long", "buoy_id"])
csv_file2.write_row(["index_start", "index_end", "count", "timestamp_start", "timestamp_end", "min_lat", "max_lat", "min_long", "max_long", "dif_lat", "dif_long", "buoy_id"])
parser = ParserElNino()

run_loop(text_file, csv_file1, csv_file2, parser)

text_file.close()
csv_file1.close()
csv_file2.close()



import sys
sys.path.append('.')

from csv_converter.csv_converter import CSVConverter
from file_utils.csv_utils.csv_reader import CSVReader
from parsers.irkis.parser_vwc import ParserVWC
from parsers.noaa.parser_noaa import ParserNOAA

import os
current_path = os.path.dirname(os.path.abspath(__file__))


def convert_to_csv(parser_klass, input_path, input_filenames, output_path, args):
    row_count = None
    for input_filename in input_filenames:
        output_filename = input_filename + '.csv'
        print "Converting", output_filename
        CSVConverter(input_path, input_filename, parser_klass(), output_path, output_filename, args).run()

        count = CSVReader(output_path, output_filename).total_lines()
        if row_count is None:
            row_count = count
        elif row_count != count:
            print "#### ERROR: row_count != count ### row_count=", row_count, "| count=", count
        else:
            print "SIZES MATCH!! count=", count


def irkis():
    input_path = "/Users/pablocerve/Documents/FING/Proyecto/datasets/irkis"
    input_filenames = ["vwc_222.smet", "vwc_333.smet", "vwc_1202.dat", "vwc_1203.dat", "vwc_1204.dat", "vwc_1205.dat", "vwc_SLF2.smet"]
    output_path = current_path + '/irkis'

    args = {
        'dataset': 'IRKIS',
        'first_timestamp': "2010-10-01 00:00:00",
        'last_timestamp': "2013-10-01 00:00:00",
        'delta': "00:10:00"
    }
    convert_to_csv(ParserVWC, input_path, input_filenames, output_path, args)

def noaa():
    input_path = "/Users/pablocerve/Documents/FING/Proyecto/datasets/noaa/2-d10-949.tar"
    input_filenames = os.listdir(input_path)
    output_path = current_path + '/noaa'

    args = {
        'dataset': 'NOAA-2016',
        'first_timestamp': "2016-01-01 00:00:00",
        'last_timestamp': "2016-12-31 23:50:00",
        'delta': "00:10:00"
    }
    convert_to_csv(ParserNOAA, input_path, input_filenames, output_path, args)

noaa()

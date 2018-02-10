import sys
sys.path.append('.')

from csv_converter.csv_converter import CSVConverter
from dataset_utils.irkis_utils import IRKISUtils
from dataset_utils.noaa_utils import NOAAUtils
from file_utils.csv_utils.csv_reader import CSVReader
from parsers.irkis.parser_vwc import ParserVWC
from parsers.noaa.parser_noaa import ParserNOAA

import os
current_path = os.path.dirname(os.path.abspath(__file__))
datasets_path = "/Users/pablocerve/Documents/FING/Proyecto/datasets/"


def convert_to_csv(parser_klass, input_path, input_filenames, output_path, dataset_utils):
    row_count = None
    for input_filename in input_filenames:
        output_filename = input_filename + '.csv'
        print "\nConverting", output_filename
        csv_converter = CSVConverter(input_path, input_filename, parser_klass(), output_path, output_filename, dataset_utils)
        csv_converter.run()
        csv_converter.print_stats()
        csv_converter.plot()
        csv_converter.close()

        count = CSVReader(output_path, output_filename).total_lines()
        if row_count is None:
            row_count = count
        elif row_count != count:
            print "#### ERROR: row_count != count ### row_count=", row_count, "| count=", count
        else:
            print "SIZES MATCH!! count=", count


def irkis():
    input_path = datasets_path + "[1]irkis/vwc"
    input_filenames = os.listdir(input_path)
    output_path = current_path + '/irkis'
    convert_to_csv(ParserVWC, input_path, input_filenames, output_path, IRKISUtils())


def noaa():
    input_path = datasets_path + "[2]noaa/2016"
    input_filenames = os.listdir(input_path)
    output_path = current_path + '/noaa'
    convert_to_csv(ParserNOAA, input_path, input_filenames, output_path, NOAAUtils())

irkis()
# noaa()

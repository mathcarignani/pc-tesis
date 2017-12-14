import sys
sys.path.append('.')

from csv_converter.csv_converter import CSVConverter
from parsers.irkis.parser_vwc import ParserVWC



input_path = "/Users/pablocerve/Documents/FING/Proyecto/datasets/irkis"
input_filenames = ["vwc_222.smet", "vwc_333.smet", "vwc_1202.dat", "vwc_1203.dat", "vwc_1204.dat", "vwc_1205.dat", "vwc_SLF2.smet"]

import os
output_path = os.path.dirname(os.path.abspath(__file__)) + '/irkis'

args = {
    'dataset': 'IRKIS',
    'first_timestamp': "2010-10-01 00:00:00",
    'last_timestamp': "2013-10-01 00:00:00",
    'delta': "01:00:00"
}

for input_filename in input_filenames:
    outputh_filename = input_filename + '.csv'
    parser_vwc = ParserVWC()
    csv_converter = CSVConverter(input_path, input_filename, parser_vwc, output_path, outputh_filename, args)
    csv_converter.close()



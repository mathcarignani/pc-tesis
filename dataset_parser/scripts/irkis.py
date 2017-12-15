import sys
sys.path.append('.')

from csv_converter.csv_converter import CSVConverter
from file_utils.csv_utils.csv_reader import CSVReader
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

row_count = None
for input_filename in input_filenames:
    output_filename = input_filename + '.csv'
    parser_vwc = ParserVWC()
    print "Converting", output_filename
    CSVConverter(input_path, input_filename, parser_vwc, output_path, output_filename, args).run()

    count = CSVReader(output_path, output_filename).total_lines()

    if row_count is None:
        row_count = count
    elif row_count != count:
        print "#### ERROR: row_count != count ### row_count=", row_count, "| count=", count
    else:
        print "SIZES MATCH!! count=", count




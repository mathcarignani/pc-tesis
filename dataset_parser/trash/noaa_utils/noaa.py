import os

from file_utils.text_utils.text_file_reader import TextFileReader
from parsers.noaa.parser_noaa import ParserNOAA

folder = "/Users/pablocerve/Documents/FING/Proyecto/datasets/noaa/2-d10-949.tar"


def _parse_and_process(folder, filename):
    text_file_reader = TextFileReader(folder, filename)
    parser = ParserNOAA()
    text_file_reader.parse_file(parser)
    parser.process_data()
    parser.plot(filename)

for filename in os.listdir(folder)[41:]:
    if filename in ['TAO_T2N110W_R_SST_10min.ascii', 'TAO_T8N110W_R_SST_10min.ascii']:  # only nan values
        continue
    _parse_and_process(folder, filename)



from file_reader import FileReader
from parsers.noaa.parser_noaa import ParserNOAA
import os

folder = "/Users/pablocerve/Documents/FING/Proyecto/datasets/noaa/2-d10-949.tar"


def _parse_and_process(folder, filename):
    file_reader = FileReader(folder, filename)
    parser = ParserNOAA()
    file_reader.parse_file(parser)
    parser.process_data()
    parser.plot(filename)

for filename in os.listdir(folder)[41:]:
    if filename in ['TAO_T2N110W_R_SST_10min.ascii', 'TAO_T8N110W_R_SST_10min.ascii']:  # only nan values
        continue
    _parse_and_process(folder, filename)

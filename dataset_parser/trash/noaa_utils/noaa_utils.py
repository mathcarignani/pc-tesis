import os

import sys

import pandas as pd

sys.path.append('../')

from parsers.noaa.parser_noaa import ParserNOAA
from file_utils.text_utils.utils import Scripts as FileScripts


def create_df(path, filename):
    parser = ParserNOAA()
    FileScripts.parse_file(path, filename, parser)

    custom_range = pd.date_range('2016-01-01', '2017-01-01', freq='10min')
    df = parser.df
    df = df.reindex(custom_range)
    df = df[:-1]
    return df


path = "/Users/pablocerve/Documents/FING/Proyecto/datasets/noaa/2-d10-949.tar"
output_path = "/Users/pablocerve/Documents/FING/Proyecto/datasets/noaa/2-d10-949.tar.csv"

for filename in os.listdir(path):
    if filename in ['TAO_T2N110W_R_SST_10min.ascii', 'TAO_T8N110W_R_SST_10min.ascii']:  # only nan values
        continue
    df = create_df(path, filename)
    df.to_csv(output_path + '/' + filename + '.csv', encoding='utf-8')

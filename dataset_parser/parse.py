from file_utils.scripts import Scripts as FileScripts
from parsers.irkis.parser_vwc import ParserVWC


parser = ParserVWC()
path, filename = "/Users/pablocerve/Documents/FING/Proyecto/datasets/irkis", "vwc_1202.dat"
FileScripts.parse_file(path, filename, parser)

df = parser.df

import numpy as np
a = np.array([])
for column_name in df.dtypes.index:
    print len(a)
    values = df[column_name].values
    array = values[~np.isnan(values)]
    array = np.array(array)
    print len(array)
    print '1'
    a = a + array

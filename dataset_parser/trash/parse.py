from file_utils.text_utils.utils import Scripts as FileScripts
from parsers.irkis.parser_vwc import ParserVWC


parser = ParserVWC()
path, filename = "/Users/pablocerve/Documents/FING/Proyecto/datasets/irkis", "vwc_1202.dat"
FileScripts.parse_file(path, filename, parser)

df = parser.df

import numpy as np
res = []
for column_name in df.dtypes.index:
    values = df[column_name].values
    array = values[~np.isnan(values)]
    array = np.array(array)
    for i in array:
        res.append(i)

sorted = np.sort(res)

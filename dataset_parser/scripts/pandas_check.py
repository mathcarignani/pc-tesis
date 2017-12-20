import sys
sys.path.append('.')

from csv_converter.csv_converter import CSVConverter
from pandas_tools.pandas_tools import PandasTools

# import os
# current_path = os.path.dirname(os.path.abspath(__file__))

input_path = '/Users/pablocerve/Documents/FING/Proyecto/pc-tesis/dataset_parser/scripts/irkis_'
input_filename = 'vwc_222.smet.csv'

p_tools = PandasTools(input_path, input_filename)
p_tools.create_df()
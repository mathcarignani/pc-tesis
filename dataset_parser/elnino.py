from file_reader import FileReader
from parsers.elnino.parser_elnino import ParserElNino

folder = "/Users/pablocerve/Documents/FING/Proyecto/datasets/el-nino/large"
filename = 'tao-all2.dat'

file_reader = FileReader(folder, filename)
parser = ParserElNino()
file_reader.parse_file(parser)
parser.process_data()
parser.df.groupby(['lat','long']).size().reset_index().rename(columns={0:'count'})
# parser.plot(filename)

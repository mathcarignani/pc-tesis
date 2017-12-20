from file_utils.text_utils.text_file_reader import TextFileReader
from parsers.elnino.parser_elnino import ParserElNino

folder = "/Users/pablocerve/Documents/FING/Proyecto/datasets/el-nino/large"
filename = 'tao-all2.dat'

text_file_reader = TextFileReader(folder, filename)
parser = ParserElNino()
text_file_reader.parse_file(parser)
parser.process_data()
parser.df.groupby(['lat','long']).size().reset_index().rename(columns={0:'count'})
# parser.plot(filename)

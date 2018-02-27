from aux.date_range import DateRange
from csv_converter import CSVConverter
from file_utils.csv_utils.csv_writer import CSVWriter
from pandas_tools.pandas_tools import PandasTools
from parsers.noaa.parser_noaa import ParserNOAA


class CSVConverterNOAA(CSVConverter):
    def __init__(self):
        self.parser = ParserNOAA()
        self.pandas_tools = PandasTools(self.parser)

    def input_csv_to_df(self, input_file, date_range=DateRange()):
        csv_converter = CSVConverter(ParserNOAA())
        # "TAO_T5N140W_D_SST_10min.ascii" => "T5N140W"
        column = input_file.filename.split("_")[1]
        csv_converter.input_csv_to_df(input_file, date_range, [column])
        self.pandas_tools.concat_df(csv_converter.pandas_tools.df)

    def df_to_output_csv(self, output_path, output_filename):
        output_file = CSVWriter(output_path, output_filename)
        output_file.write_row(['DATASET:', self.parser.NAME])
        print "AAA"
        print self.pandas_tools.df.columns
        columns = ['Timestamp']
        columns.extend(self.pandas_tools.df.columns)
        output_file.write_row(columns)
        self.pandas_tools.df_to_csv(output_file)
        output_file.close()
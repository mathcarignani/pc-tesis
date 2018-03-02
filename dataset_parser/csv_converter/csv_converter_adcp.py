from aux.date_range import DateRange
from csv_converter import CSVConverter
from file_utils.csv_utils.csv_writer import CSVWriter
from pandas_tools.pandas_tools import PandasTools
from parsers.adcp.parser_adcp import ParserADCP


class CSVConverterADCP(CSVConverter):
    def __init__(self):
        self.parser = ParserADCP()
        self.pandas_tools = PandasTools(self.parser)

    def input_csv_to_df(self, input_file, date_range=DateRange()):
        csv_converter = CSVConverter(ParserADCP())
        # "TAO_T0N110W_D_ADCP.ascii" => "T0N110W"
        column_str = input_file.filename.split("_")[1]
        columns = ['UCUR', 'VCUR', 'WCUR']
        columns = [column_str + "_" + column for column in columns]
        csv_converter.input_csv_to_df(input_file, date_range, columns, 'DEPTH')
        self.pandas_tools.concat_df(csv_converter.pandas_tools.df)

    def df_to_output_csv(self, output_path, output_filename):
        output_file = CSVWriter(output_path, output_filename)
        output_file.write_row(['DATASET:', self.parser.NAME])
        columns = ['Timestamp', 'Depth']
        columns.extend(self.pandas_tools.df.columns)
        output_file.write_row(columns)
        self.pandas_tools.df_to_csv(output_file)
        output_file.close()

    def print_stats(self):
        self.pandas_tools.print_stats()
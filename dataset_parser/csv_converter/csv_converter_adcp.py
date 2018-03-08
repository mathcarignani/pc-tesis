from csv_converter import CSVConverter
from file_utils.csv_utils.csv_writer import CSVWriter
from pandas_tools.pandas_tools import PandasTools
from parsers.adcp.parser_adcp import ParserADCP


class CSVConverterADCP(CSVConverter):
    def __init__(self, logger):
        self.logger = logger
        self.parser = ParserADCP(self.logger)
        self.pandas_tools = PandasTools(self.parser, self.logger)

    def input_csv_to_df(self, input_file, date_range):
        csv_converter = CSVConverter(self.parser, self.logger)
        # "TAO_T0N110W_D_ADCP.ascii" => "T0N110W"
        column_str = input_file.filename.split("_")[1]
        columns = self.columns(column_str)
        csv_converter.input_csv_to_df(input_file, date_range, columns, column_str)
        self.pandas_tools.concat_df(csv_converter.pandas_tools.df)

    @classmethod
    def columns(cls, column_str):
        cols = []
        for depth in range(10, 321, 5):  # [10, 15, 20, ..., 310, 315, 320]
            for component in ['UCUR', 'VCUR', 'WCUR']:
                col = column_str + "_" + str(int(depth)) + "_" + component
                cols.append(col)
        return cols

    def df_to_output_csv(self, output_path, output_filename):
        output_file = CSVWriter(output_path, output_filename)
        output_file.write_row(['DATASET:', self.parser.NAME])
        columns = ['Timestamp']
        columns.extend(self.pandas_tools.df.columns)
        output_file.write_row(columns)
        self.pandas_tools.df_to_csv(output_file)
        output_file.close()

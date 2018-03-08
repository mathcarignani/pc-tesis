from csv_converter import CSVConverter
from file_utils.csv_utils.csv_writer import CSVWriter
from pandas_tools.pandas_tools import PandasTools
from parsers.solar_anywhere.parser_solar_anywhere import ParserSolarAnywhere


class CSVConverterSolarAnywhere(CSVConverter):
    def __init__(self, logger):
        self.logger = logger
        self.parser = ParserSolarAnywhere(self.logger)
        self.pandas_tools = PandasTools(self.parser, self.logger)

    def input_csv_to_df(self, input_file, date_range, plot_output_path):
        csv_converter = CSVConverter(self.parser, self.logger)
        # "0_0.csv" => "0_0"
        column_str = input_file.filename.split(".")[0]
        columns = [column_str + '_' + column for column in ['GHI', 'DNI', 'DHI']]
        csv_converter.input_csv_to_df(input_file, date_range, columns)
        df = csv_converter.pandas_tools.df.copy()
        ParserSolarAnywhere.plot(plot_output_path, input_file.filename, df)
        self.pandas_tools.concat_df(csv_converter.pandas_tools.df)

    def df_to_output_csv(self, output_path, output_filename):
        output_file = CSVWriter(output_path, output_filename)
        output_file.write_row(['DATASET:', self.parser.NAME])
        columns = ['Timestamp']
        columns.extend(self.pandas_tools.df.columns)
        output_file.write_row(columns)
        self.pandas_tools.df_to_csv(output_file)
        output_file.close()

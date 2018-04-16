from aux.date_range import DateRange
from file_utils.csv_utils.csv_writer import CSVWriter
from pandas_tools.pandas_tools import PandasTools


class CSVConverter:
    def __init__(self, parser, logger):
        self.parser = parser
        self.logger = logger
        self.pandas_tools = PandasTools(self.parser, self.logger)
        # initialized in the input_csv_to_df method
        self.input_file = None
        self.date_range = None
        self.adcp = None
        self.repeat_timestamp = None

    #
    # repeat_timestamp is True if it is expected that the same timestamp can be repeated
    #
    def input_csv_to_df(self, input_file, date_range=None, columns=None, adcp=False, repeat_timestamp=False):
        self.input_file = input_file
        self.date_range = date_range
        self.adcp = adcp
        self.repeat_timestamp = repeat_timestamp
        while self.parser.parsing_header:
            line = self.input_file.read_line()
            self.parser.parse_header(line)
        cols = self.parser.columns if columns is None else columns
        self.pandas_tools.new_df(cols, repeat_timestamp)
        self._write_data()
        self.input_file.close()

    def print_stats(self):
        self.pandas_tools.print_stats()

    def df_to_output_csv(self, output_path, output_filename):
        if self.pandas_tools.is_empty_df():
            return
        output_file = CSVWriter(output_path, output_filename)
        output_file.write_row(['DATASET:', self.parser.name])
        output_file.write_row(['TIME UNIT:', self.parser.time_unit])
        output_file.write_row(['FIRST TIMESTAMP:', self.pandas_tools.first_timestamp()])
        output_file.write_row(['Time Delta'] + self.parser.columns)
        self.pandas_tools.df_to_csv(output_file, self.parser.time_unit)
        output_file.close()

    def plot(self, output_path):
        if self.pandas_tools.is_empty_df():
            return
        self.parser.plot(output_path, self.input_file.filename, self.pandas_tools.df)

    ####################################################################################################################
    ####################################################################################################################
    ####################################################################################################################

    def _write_data(self):
        self.previous_timestamp, self.previous_values = None, None
        while self.input_file.continue_reading:
            self._process_line()

    def _process_line(self):
        row = None
        while row is None:
            line = self.input_file.read_line()
            row = self.parser.parse_data(line)  # { 'timestamp': datetime object, 'values': values array }
        self.timestamp, self.values = row['timestamp'], row['values']
        if self.date_range and not self.date_range.inside_range(self.timestamp):
            return
        if self.adcp is False:
            if not self.repeat_timestamp:
                self.print_warning()
            self.pandas_tools.add_row(self.timestamp, self.values)
        else:
            if self.previous_timestamp and self.previous_timestamp.day != self.timestamp.day:
                print self.timestamp
            self.pandas_tools.add_row(self.timestamp, self.values, self.adcp)

        self.previous_timestamp, self.previous_values = self.timestamp, self.values

    def print_warning(self):
        # first row OR positive timestamp delta
        if self.previous_timestamp is None or self.timestamp > self.previous_timestamp:
            return
        elif self.timestamp < self.previous_timestamp:
            self._print_state("WARNING: timestamp < previous_timestamp")
        else:  # self.timestamp == self.previous_timestamp:
            if self.values == self.previous_values:
                self._print_state("WARNING: timestamp == previous_timestamp => duplicate row")
            else:
                self._print_state("WARNING: timestamp == previous_timestamp => different row")

    def _print_state(self, message=None):
        if message is not None:
            self.logger.info(message)
        self.logger.info('previous_timestamp =%s', self.previous_timestamp)
        self.logger.info('timestamp =%s', self.timestamp)
        self.logger.info('previous_values =%s', self.previous_values)
        self.logger.info('values =%s', self.values)
        self.logger.info('')

    # def _raise_error(self, message):
    #     self._print_state()
    #     raise StandardError(message)

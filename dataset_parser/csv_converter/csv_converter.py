from file_utils.csv_utils.csv_writer import CSVWriter
from pandas_tools.pandas_tools import PandasTools
import logging


class CSVConverter:
    def __init__(self, parser):
        self.parser = parser
        self.pandas_tools = PandasTools(parser)

    #
    # If year=2013, then we only consider dates in which year>=2013
    #
    def input_csv_to_df(self, input_file, year=None):
        self.input_file = input_file
        self.year = year
        while self.parser.parsing_header:
            line = self.input_file.read_line()
            self.parser.parse_header(line)
        self.pandas_tools.new_df(self.parser.columns)
        self._write_data()
        self.input_file.close()

    def print_stats(self):
        self.pandas_tools.print_stats()

    def df_to_output_csv(self, output_path, output_filename):
        if self.pandas_tools.is_empty_df():
            return
        output_file = CSVWriter(output_path, output_filename)
        output_file.write_row(['DATASET:', self.parser.NAME])
        output_file.write_row(['FILENAME:', self.input_file.filename])
        output_file.write_row(['Timestamp'] + self.parser.columns)
        self.pandas_tools.df_to_csv(output_file)
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
        self.inside_range = True if self.year is None else False
        while self.input_file.continue_reading:
            self._process_line()

    def _process_line(self):
        row = None
        while row is None:
            line = self.input_file.read_line()
            row = self.parser.parse_data(line)  # { 'timestamp': datetime object, 'values': values array }
        self.timestamp, self.values = row['timestamp'], row['values']
        if not self.timestamp_inside_range():
            return
        self.print_warning()
        self.pandas_tools.add_row(self.timestamp, self.values)
        self.previous_timestamp, self.previous_values = self.timestamp, self.values

    def timestamp_inside_range(self):
        if self.inside_range:
            return True
        else:
            self.inside_range = self.timestamp.year >= self.year
            if self.inside_range:
                self.input_file.new_progress_bar()
            return self.inside_range

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
            logging.info(message)
        logging.info('previous_timestamp =%s', self.previous_timestamp)
        logging.info('timestamp =%s', self.timestamp)
        logging.info('previous_values =%s', self.previous_values)
        logging.info('values =%s', self.values)
        logging.info('')

    # def _raise_error(self, message):
    #     self._print_state()
    #     raise StandardError(message)

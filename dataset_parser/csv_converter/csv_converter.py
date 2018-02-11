from file_utils.text_utils.text_file_reader import TextFileReader
from file_utils.csv_utils.csv_writer import CSVWriter
from pandas_tools.pandas_tools import PandasTools
import converter_utils
import logging


class CSVConverter:
    def __init__(self, input_path, input_filename, parser, output_path, output_filename):
        self.output_path = output_path
        self.input_file = TextFileReader(input_path, input_filename, True)
        self.parser = parser
        self.output_file = CSVWriter(output_path, output_filename)
        self.pandas_tools = PandasTools()

    def run(self):
        self._write_metadata()
        self._write_columns()
        self._write_data()

    def print_stats(self):
        self.pandas_tools.print_stats()

    def plot(self):
        self.parser.plot(self.output_path, self.input_file.filename, self.pandas_tools.df)

    def close(self):
        self.input_file.close()
        self.output_file.close()

    ####################################################################################################################
    ####################################################################################################################
    ####################################################################################################################

    def _write_metadata(self):
        metadata = {
            'DATASET:': self.parser.NAME,
            'FILENAME:': self.input_file.filename
        }
        for key, value in metadata.items():
            self.output_file.write_row([key, value])

    def _write_columns(self):
        while self.parser.parsing_header:
            line = self.input_file.read_line()
            self.parser.parse_header(line)
        self.output_file.write_row(['Timestamp'] + self.parser.columns)
        self.pandas_tools.new_df(self.parser.columns)

    def _write_data(self):
        self.previous_timestamp = None
        self.previous_values = None
        while self.input_file.continue_reading:
            self._process_line()

    def _process_line(self):
        row = None
        while row is None:
            line = self.input_file.read_line()
            row = self.parser.parse_data(line)  # { 'timestamp': datetime, 'values' = [] }

        self.timestamp = row['timestamp']  # datetime
        self.values = row['values']

        if self.previous_timestamp is None:  # first row, print timestamp
            timestamp_str = self.timestamp.strftime(converter_utils.DATE_FORMAT)
            self._add_row(timestamp_str, self.values)

        elif self.timestamp < self.previous_timestamp:
            self._raise_error("timestamp < previous_timestamp")  # stop

        elif self.timestamp == self.previous_timestamp:
            if self.values == self.last_values:
                self._print_state("ERROR: duplicate row")  # print error and continue
            else:
                self._raise_error("timestamp < previous_timestamp")  # stop

        else:  # self.timestamp > self.previous_timestamp
            delta = self.timestamp - self.previous_timestamp  # always positive
            delta = converter_utils.format_timedelta(delta)
            self._add_row(delta, self.values)

        self.previous_timestamp = self.timestamp
        self.previous_values = self.values

    def _add_row(self, timestamp, values):
        self.last_values = values
        self.output_file.write_row([timestamp] + values)
        self.pandas_tools.add_row(self.timestamp, values)

    def _print_state(self, message=None):
        if message is not None:
            logging.info(message)
        logging.info('previous_timestamp =%s', self.previous_timestamp)
        logging.info('timestamp =%s', self.timestamp)
        logging.info('previous_values =%s', self.previous_values)
        logging.info('values =%s', self.values)
        logging.info('')

    def _raise_error(self, message):
        self._print_state()
        raise StandardError(message)

from file_utils.csv_utils.csv_writer import CSVWriter
from pandas_tools.pandas_tools import PandasTools
import converter_utils
import logging


class CSVConverter:
    def __init__(self, input_file, parser, output_path, output_filename):
        self.output_path = output_path
        self.input_file = input_file
        self.parser = parser
        self.output_file = CSVWriter(output_path, output_filename)
        self.pandas_tools = PandasTools(parser)

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
        self.output_file.write_row(['DATASET:', self.parser.NAME])
        self.output_file.write_row(['FILENAME:', self.input_file.filename])

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
            row = self.parser.parse_data(line)  # { 'timestamp': datetime object, 'values': values array }

        self.timestamp, self.values = row['timestamp'], row['values']
        self._process_line_aux()
        self.previous_timestamp, self.previous_values = self.timestamp, self.values

    def _process_line_aux(self):
        if self.previous_timestamp is None:  # first row, print timestamp
            self._add_row_raw_date()

        elif self.timestamp < self.previous_timestamp:
            if self.parser.asc_timestamp:
                self._raise_error("timestamp < previous_timestamp")  # stop
            else:
                self._add_row_raw_date()  # print timestamp

        elif self.timestamp == self.previous_timestamp:
            if self.values == self.last_values:
                self._print_state("ERROR: duplicate row")  # print error and continue
            elif self.parser.asc_timestamp:
                self._raise_error("timestamp == previous_timestamp")  # stop
            else:
                self._add_row_raw_date()  # print timestamp

        else:  # self.timestamp > self.previous_timestamp
            self._add_row_delta()

    def _add_row_raw_date(self):
        timestamp_str = self.timestamp.strftime(converter_utils.DATE_FORMAT)
        self._add_row(timestamp_str, self.values)

    #
    # PRE: self.timestamp > self.previous_timestamp
    #
    def _add_row_delta(self):
        delta = self.timestamp - self.previous_timestamp  # always positive
        delta = converter_utils.format_timedelta(delta)
        self._add_row(delta, self.values)

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

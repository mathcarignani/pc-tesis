from file_utils.text_utils.text_file_reader import TextFileReader
from file_utils.csv_utils.csv_writer import CSVWriter
import converter_utils


class CSVConverter:
    # args = {
    #     'dataset': 'IRKIS'
    # }
    def __init__(self, input_path, input_filename, parser, output_path, output_filename, args):
        self.input_file = TextFileReader(input_path, input_filename)
        self.parser = parser
        self.output_file = CSVWriter(output_path, output_filename)
        self.args = args

    def run(self):
        self._write_metadata()
        self._write_columns()
        self._write_data()

        self.input_file.close()
        self.output_file.close()

    ####################################################################################################################

    def _write_metadata(self):
        metadata = {
            'DATASET:': self.args['dataset'],
            'FILENAME:': self.input_file.filename
        }
        for key, value in metadata.items():
            self.output_file.write_row([key, value])

    def _write_columns(self):
        while self.parser.parsing_header:
            line = self.input_file.read_line()
            self.parser.parse_header(line)
        self.output_file.write_row(['Timestamp'] + self.parser.columns)

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
            if row['values'] == self.last_values:
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
        if self.args['dataset'] == 'IRKIS':
            values = self._map_values_irkis(values)
        self.output_file.write_row([timestamp] + values)

    def _map_values_irkis(self, values):
        new_values = []
        for value in values:
            new_value = 'N' if value == 'N' else round(float(value)*1000, 0)
            new_values.append(new_value)
        return new_values

    def _print_state(self, message=None):
        if message is not None:
            print message
        print 'previous_timestamp =', self.previous_timestamp
        print 'timestamp =', self.timestamp
        print 'previous_values =', self.previous_values
        print 'values =', self.values
        print

    def _raise_error(self, message):
        self._print_state()
        raise StandardError(message)

from datetime import datetime, timedelta

from file_utils.text_utils.file_reader import FileReader
from file_utils.csv_utils.csv_writer import CSVWriter


class CSVConverter:
    DATE_FORMAT = "%Y-%m-%d %H:%M:%S"  # "2010-10-01 00:00:00"
    DELTA_FORMAT = "%H:%M:%S"  # "01:00:00"

    # args = {
    #     'dataset': 'IRKIS',
    #     'first_timestamp': "2010-10-01 00:00:00",
    #     'last_timestamp': "2013-10-01 00:00:00",
    #     'delta': "01:00:00",
    # }
    def __init__(self, input_path, input_filename, parser, output_path, output_filename, args):
        self.input_file = FileReader(input_path, input_filename)
        self.parser = parser
        self.output_file = CSVWriter(output_path, output_filename)

        self.args = args
        self.first_timestamp = datetime.strptime(args['first_timestamp'], self.DATE_FORMAT)
        self.last_timestamp = datetime.strptime(args['last_timestamp'], self.DATE_FORMAT)
        self.delta = self._parse_delta()

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
            'FILENAME:': self.input_file.filename,
            'FIRST_TIMESTAMP:': self.args['first_timestamp'],
            'LAST_TIMESTAMP:': self.args['last_timestamp'],
            'DELTA:': self.args['delta']
        }
        for key, value in metadata.items():
            self.output_file.write_row([key, value])

    def _write_columns(self):
        while self.parser.parsing_header:
            line = self.input_file.read_line()
            self.parser.parse_header(line)
        self.output_file.write_row(['Timestamp', 'Missing'] + self.parser.columns)

    def _write_data(self):
        self.last_values = []
        self.expected_timestamp = self.first_timestamp
        self.expected_timestamp_count = 0

        while self.input_file.continue_reading:
            self._process_line()
        self.expected_timestamp = self.timestamp
        while self.expected_timestamp < self.last_timestamp:
            self._add_row_missing()

    def _process_line(self):
        line = self.input_file.read_line()
        row = self.parser.parse_data(line)  # { 'timestamp': datetime, 'values' = [] }

        self.timestamp = row['timestamp']  # datetime
        if self.timestamp > self.last_timestamp:
            self._raise_error("timestamp > last_timestamp")
        elif self.timestamp < self.expected_timestamp:
            if self.timestamp == self.expected_timestamp - self.delta and row['values'] == self.last_values:
                self._print_state("ERROR: duplicate row")
            else:
                self._raise_error("timestamp < expected_timestamp")
        else:
            while self.timestamp > self.expected_timestamp:
                self._add_row_missing()
            if self.timestamp < self.expected_timestamp:  # both timestamps should match
                self._raise_error("timestamp < expected_timestamp")
            self._add_row(row['values'])

    def _add_row(self, values):
        self.output_file.write_row([self.expected_timestamp_count, '0'] + values)
        self._update_expected_timestamp()
        self.last_values = values

    def _add_row_missing(self):
        self.output_file.write_row([self.expected_timestamp_count, '1'])
        self._update_expected_timestamp()

    def _update_expected_timestamp(self):
        self.expected_timestamp += self.delta
        self.expected_timestamp_count += 1

    def _print_state(self, message=None):
        if message is not None:
            print message
        print 'expected_timestamp_count =', self.expected_timestamp_count
        print 'expected_timestamp =', self.expected_timestamp
        print 'timestamp =', self.timestamp
        print 'last_timestamp =', self.last_timestamp
        print

    def _raise_error(self, message):
        self._print_state()
        raise StandardError(message)

    def _parse_delta(self):
        t = datetime.strptime(self.args['delta'], self.DELTA_FORMAT)
        return timedelta(hours=t.hour, minutes=t.minute, seconds=t.second)

    # def _string_timestamp(self):
    #     return self.expected_timestamp.strftime(self.DATE_FORMAT)

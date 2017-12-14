from datetime import datetime, timedelta

from file_utils.aux import full_path
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
    def __init__(self, input_path, input_filename, parser, output_path, outputh_filename, args):
        self.input_file = FileReader(input_path, input_filename, True)
        self.parser = parser
        self.output_file = CSVWriter(output_path, outputh_filename)

        # parse args
        self.args = args
        self.expected_timestamp = self.first_timestamp = datetime.strptime(args['first_timestamp'], self.DATE_FORMAT)
        self.expected_timestamp_count = 0
        self.last_timestamp = datetime.strptime(args['last_timestamp'], self.DATE_FORMAT)
        t = datetime.strptime(args['delta'], self.DELTA_FORMAT)
        self.delta = timedelta(hours=t.hour, minutes=t.minute, seconds=t.second)

        # run
        self._write_metadata(input_path, input_filename)
        self._write_columns()
        self._write_data()
    
    def close(self):
        self.input_file.close()
        self.output_file.close()

    def _write_metadata(self, input_path, input_filename):
        self.output_file.write_row(['DATASET:', self.args['dataset']])
        self.output_file.write_row(['FILENAME:', input_filename])
        self.output_file.write_row(['FIRST_TIMESTAMP:', self.args['first_timestamp']])
        self.output_file.write_row(['LAST_TIMESTAMP:', self.args['last_timestamp']])
        self.output_file.write_row(['DELTA:', self.args['delta']])

    def _write_columns(self):
        while self.parser.parsing_header:
            line = self.input_file.read_line()
            self.parser.parse_header(line)
        self.output_file.write_row(['Timestamp', 'Missing'] + self.parser.columns)

    def _write_data(self):
        while self.input_file.continue_reading:
            line = self.input_file.read_line()
            row = self.parser.parse_data(line)  # { 'timestamp': datetime, 'values' = [] }

            self.timestamp = row['timestamp']

            if self.timestamp > self.last_timestamp:
                self._raise_error("timestamp > last_timestamp")
            elif self.timestamp < self.expected_timestamp:
                # add invalid row, possible duplicate
                pass
            else:
                if self.timestamp > self.expected_timestamp:
                    self._complete_missing_rows()
                if self.timestamp < self.expected_timestamp:
                    self._raise_error("timestamp > expected_timestamp")
                self._add_row(row['values'])

    def _complete_missing_rows(self):
        while self.timestamp > self.expected_timestamp:
            self._add_row_missing()

    def _add_row(self, values):
        self.output_file.write_row([self.expected_timestamp_count, '0'] + values)
        self._update_expected_timestamp()

    def _add_row_missing(self):
        self.output_file.write_row([self.expected_timestamp_count, '1'])
        self._update_expected_timestamp()

    def _update_expected_timestamp(self):
        self.expected_timestamp += self.delta
        self.expected_timestamp_count += 1

    def _raise_error(self, message):
        print 'timestamp =', self.timestamp
        print 'expected_timestamp = ', self.expected_timestamp
        print 'first_timestamp = ', self.first_timestamp
        print 'last_timestamp = ', self.last_timestamp
        raise StandardError(message)




from datetime import datetime, timedelta

import sys
sys.path.append('../')

from aux.dataset_utils import DatasetUtils


class HeaderUtils:
    DATE_FORMAT = "%Y-%m-%d %H:%M:%S"  # "2010-10-01 00:00:00"
    START_DATE = datetime.strptime("1900-01-01 00:00:00", DATE_FORMAT)
    END_DATE = datetime.strptime("2036-02-07 06:28:16", DATE_FORMAT)

    @classmethod
    def code_header(cls, input_csv, output_file):
        dataset_utils = DatasetUtils('code')

        # DATASET:|NOAA-SST
        dataset = input_csv.read_line()[1]
        output_file.write_int(dataset_utils.dataset_value(dataset), 4)  # 4 bits for the dataset name

        # TIME UNIT:|seconds
        time_unit = input_csv.read_line()[1]
        output_file.write_int(dataset_utils.time_unit_value(time_unit), 4)  # 4 bits for the time unit

        # FIRST TIMESTAMP:|2017-01-01 00:00:00
        timestamp = input_csv.read_line()[1]
        seconds = cls.date_str_to_seconds(timestamp)
        output_file.write_int(seconds, 32)  # 32 bits for the timestamp

        # Time Delta|T0N110W|T0N125W|T0N155W|...|T9N140W
        column_names_array = input_csv.read_line()[1:]
        cls.code_column_names(column_names_array, output_file)

        return dataset_utils.alphabet_values(dataset)  # {'min': min_value, 'max': max_value, 'bits': bits}

    @classmethod
    def decode_header(cls, input_file, output_csv):
        dataset_utils = DatasetUtils('decode')

        coded_dataset = input_file.read_int(4)  # 4 bits for the dataset name
        dataset = dataset_utils.dataset_value(coded_dataset)
        output_csv.write_row(['DATASET:', dataset])

        coded_time_unit = input_file.read_int(4)  # 4 bits for the time unit
        time_unit = dataset_utils.time_unit_value(coded_time_unit)
        output_csv.write_row(['TIME UNIT:', time_unit])

        seconds = input_file.read_int(32)  # 32 bits for the timestamp
        timestamp = cls.seconds_to_date_str(seconds)
        output_csv.write_row(['FIRST TIMESTAMP:', timestamp])

        column_names_array = cls.decode_column_names(input_file)
        output_csv.write_row(['Time Delta'] + column_names_array)

        columns_count = len(column_names_array)
        return dataset_utils.alphabet_values(dataset), columns_count  # {'min': min_value, 'max': max_value, 'bits': bits}

    @classmethod
    def code_column_names(cls, column_names_array, output_file):
        column_names_str = ",".join(column_names_array)
        number_of_bytes = len(column_names_str)

        # code the number of bytes in unary code
        for _ in xrange(number_of_bytes):
            output_file.write_bit(1)
        zeros_count = number_of_bytes % 8 + 8
        for _ in xrange(zeros_count):
            output_file.write_bit(0)
        # code the chars (each char uses 1 byte)
        for char in column_names_str:
            output_file.write_int(ord(char), 8)

    @classmethod
    def decode_column_names(cls, input_file):
        number_of_bytes = 0
        while input_file.read_bit() > 0:
            number_of_bytes += 1
        zeros_count = number_of_bytes % 8 + 8
        for _ in xrange(zeros_count - 1):
            input_file.read_bit()  # 0 bit
        column_names = ""
        for _ in xrange(number_of_bytes):
            char = input_file.read_int(8)
            column_names += chr(char)
        column_names_array = column_names.split(",")
        return column_names_array

    #
    # See: https://stackoverflow.com/a/7852969/4547232
    #
    # EXAMPLES:
    # HeaderUtils.date_str_to_seconds("1899-12-31 23:59:59") => ValueError: ERROR: Date outside range.
    # HeaderUtils.date_str_to_seconds("1900-01-01 00:00:00") => 0
    # HeaderUtils.date_str_to_seconds("2000-01-01 00:00:00") => 3155673600
    # HeaderUtils.date_str_to_seconds("2036-02-07 06:28:16") => 4294967296
    # HeaderUtils.date_str_to_seconds("2036-02-07 06:28:17") => ValueError: ERROR: Date outside range.
    #
    @classmethod
    def date_str_to_seconds(cls, date_str):
        date = datetime.strptime(date_str, cls.DATE_FORMAT)
        if date < cls.START_DATE or date > cls.END_DATE:
            raise ValueError("ERROR: Date outside range.")
        t_diff = date - cls.START_DATE
        seconds = int(t_diff.total_seconds())  # >= 0
        return seconds

    #
    # EXAMPLES:
    # HeaderUtils.seconds_to_date_str(-1) => ValueError: ERROR: seconds must be between 0 and 2**32.
    # HeaderUtils.seconds_to_date_str(0) => '1900-01-01 00:00:00'
    # HeaderUtils.seconds_to_date_str(3155673600) => '2000-01-01 00:00:00'
    # HeaderUtils.seconds_to_date_str(4294967296) => '2036-02-07 06:28:16'
    # HeaderUtils.seconds_to_date_str(4294967297) => ValueError: ERROR: seconds must be between 0 and 2**32.
    #
    @classmethod
    def seconds_to_date_str(cls, seconds):
        if seconds < 0 or seconds > 2**32:
            raise ValueError("ERROR: seconds must be between 0 and 2**32.")
        date = cls.START_DATE + timedelta(seconds=seconds)
        date_str = date.strftime(cls.DATE_FORMAT)
        return date_str

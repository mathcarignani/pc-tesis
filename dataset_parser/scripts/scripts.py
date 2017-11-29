import sys
sys.path.append('../')

from file_utils.file_reader import FileReader
from file_utils.file_writer import FileWriter
from parsers.irkis.parser_vwc import ParserVWC


def clean_file(input_path, input_filename, output_path, output_filename):
    input_file = FileReader(input_path, input_filename)
    output_file = FileWriter(output_path, output_filename)
    parser = ParserVWC()

    while input_file.continue_reading:
        line = input_file.read_line()
        parsing_header = parser.parsing_header
        data = parser.parse_line(line)
        if not parsing_header:
            value = get_value(parser, data)
            output_file.write_line(value)

    input_file.close()
    output_file.close()


def get_value(parser, data):
    value = data[0]
    if value == parser.nodata:
        return "nodata"
    else:
        return str(int(float(value) * 1000000))

from bit_stream.bit_stream_reader import BitStreamReader
from bit_stream.bit_stream_writer import BitStreamWriter
from parsers.irkis.parser_vwc import ParserVWC


folder = "/Users/pablocerve/Documents/FING/Proyecto/datasets/irkis/"
filename = "vwc_1202.dat"
full_filename = folder + filename

parser = ParserVWC()
bsw = BitStreamWriter('vwc_1202.dat.coded')

counter = 0
with open(full_filename, "r") as open_file:
    for line in open_file:
        parsing_header = parser.parsing_header
        data = parser.parse_line(line)
        if not parsing_header and data[0] != '-999.000000':
            value = float(data[0]) * 1000000
            value = int(value)
            bsw.write_int(value, 24)
            print value
            counter += 1
            print counter
            if counter == 10:
                break

bsw.close()

bsr = BitStreamReader('vwc_1202.dat.coded')
for _ in range(counter):
    decoded_val = bsr.read_int(24)
    print decoded_val

bsr.close()


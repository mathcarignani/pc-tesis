import sys
sys.path.append('.')

from file_utils.text_utils.text_file_reader import TextFileReader


# line = "[18=3] 1"
# returns [18, 3]
def decode_bytes_bits(line):
    value = line.split(" ")[0]  # "[18=3]"
    value = value.replace("[", "").replace("]", "")
    value_split = value.split("=")
    return int(value_split[0]), int(value_split[1])


def bytes_bits_to_str(bytes, bits):
    string = "[" + str(bytes) + "=" + str(bits) + "]"
    return string


def script():
    path = "/Users/pablocerve/Documents/FING/Proyecto/results/avances-12/2-final-bits"
    filename = "full-output-AC.txt"

    plus_pending_mode = False
    plus_pending_counter = -1
    bytes_count = 0
    bits_count = 0

    call_decompress_mode = False
    call_count = -1
    last_bytes_count = 0
    last_bits_count = 0

    count = 0

    text_file = TextFileReader(path, filename)
    while text_file.continue_reading:
        line = text_file.read_line()
        print str(count) + " " + line.replace("\n","")
        if "put_bit_plus_pending" in line:  # "put_bit_plus_pending(0, 1)"
            plus_pending_mode = True
            plus_pending_counter = 2
        elif plus_pending_mode:
            plus_pending_counter -= 1
            if plus_pending_counter == 1:  # "[18=2] 0"
                pass
            elif plus_pending_counter == 0:  # "[18=3] 1"
                bytes_count, bits_count = decode_bytes_bits(line)
                plus_pending_mode = False
        elif "callDecompress" in line:  # "callDecompress"
            call_decompress_mode = True
            call_count = 0
        elif call_decompress_mode:
            call_count += 1
            if "EOF" in line:
                if call_count > 1:
                    string = bytes_bits_to_str(bytes_count, bits_count)
                    string += " VS "
                    string += bytes_bits_to_str(last_bytes_count, last_bits_count)
                    print string
                    call_decompress_mode = False
            else:
                last_bytes_count, last_bits_count = decode_bytes_bits(line)
        count += 1

    text_file.close()



script()

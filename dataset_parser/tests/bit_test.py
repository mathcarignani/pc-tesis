import sys
sys.path.append('.')

from file_utils.bit_stream.bit_stream_writer import BitStreamWriter
from file_utils.bit_stream.bit_stream_reader import BitStreamReader

import os
path = os.path.dirname(os.path.abspath(__file__))
filename = 'test.bin'


def code(integers_array, figures_array):
    bsw = BitStreamWriter(path, filename)
    for idx, val in enumerate(integers_array):
        bsw.write_int(val, figures_array[idx])
    bsw.close()


def decode(integers_array, figures_array):
    bsr = BitStreamReader(path, filename)
    for idx, val in enumerate(integers_array):
        decoded_val = bsr.read_int(figures_array[idx])
        if decoded_val != val:
            print 'decoded_val', decoded_val, 'val', val
            raise AssertionError('ERROR.')
    bsr.close()


def test(integers_array, figures_array):
    print '.',
    code(integers_array, figures_array)
    decode(integers_array, figures_array)


test([0, 0], [256, 256])
test([114, 203], [8, 8])
test([286], [16])
test([8, 8], [4, 4])
test([114, 203, 286, 8, 8], [8, 8, 16, 4, 4])
test([114, 203, 8, 286, 8], [8, 8, 4, 16, 4])
os.remove(path + "/" + filename)
print 'SUCCESS!'


from bit_stream.bit_stream_writer import BitStreamWriter
from bit_stream.bit_stream_reader import BitStreamReader


def test(integers_array, figures_array):
    print '###################################################'
    bsw = BitStreamWriter('test.bin')
    for idx, val in enumerate(integers_array):
        bsw.write_int(val, figures_array[idx])
    bsw.close()

    bsr = BitStreamReader('test.bin')
    for idx, val in enumerate(integers_array):
        decoded_val = bsr.read_int(figures_array[idx])
        if decoded_val != val:
            print 'decoded_val', decoded_val, 'val', val
            raise AssertionError('ERROR.')
    bsr.close()


test([114, 203], [8, 8])
test([286], [16])
test([8, 8], [4, 4])
test([114, 203, 286, 8, 8], [8, 8, 16, 4, 4])
test([114, 203, 8, 286, 8], [8, 8, 4, 16, 4])

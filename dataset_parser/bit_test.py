from bit_stream.bit_stream_writer import BitStreamWriter
from bit_stream.bit_stream_reader import BitStreamReader

bsw = BitStreamWriter('test_file.bin')
for i in [0,1,0,0,1,1,1,0,1,1,0,1,0,0,1,1]:
    bsw.write_bit(i)
bsw.close()

bsr = BitStreamReader('test_file.bin')
for i in range(16):
    bit = bsr.read_bit()
bsr.close()

print '###################################################'

bsw = BitStreamWriter('test_file2.bin')
bsw.write_int(114, 8)
bsw.write_int(203, 8)
bsw.close()

bsr = BitStreamReader('test_file2.bin')
bsr.read_int(8)
bsr.read_int(8)
bsr.close()
from bit_stream.bit_stream_writer import BitStreamWriter
from bit_stream.bit_stream_reader import BitStreamReader

bsw = BitStreamWriter('test_file.bin')
# print bsw.current, bsw.offset

for i in [0,1,0,0,1,1,1,0,1,1,0,1,0,0,1,1]:
    bsw.write_bit(i)

bsw.close()

bsr = BitStreamReader('test_file.bin')
# print bsr.current, bsr.offset

for i in range(16):
    bit = bsr.read_bit()
    # print bit

bsr.close()


from utils import Utils


class BitStreamReader(object):
    def __init__(self, filename):
        self.file = open(filename, 'rb')
        self.current = self._read_byte()
        self.offset = 0

    def read_bit(self):
        ans = self.current & (1 << self.offset)
        self.offset = (self.offset + 1) & 7

        if self.offset == 0:
            self.current = self._read_byte()

        return 0 if ans == 0 else 1

    # k is the number of bits we want to read
    def read_int(self, k):
        ans = 0
        for i in xrange(k-1, -1, -1):
            ans |= self.read_bit() << i
        return ans

    def close(self):
        self.file.close()

    def _read_byte(self):
        byte = self.file.read(1)
        if byte != '':  # EOF
            return Utils.decode_byte(byte)
        else:
            print 'EOF'

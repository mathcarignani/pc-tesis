from aux import code_byte


class BitStreamWriter(object):
    def __init__(self, path, filename):
        self.file = open(path + "/" + filename, 'wb')
        self.current = 0
        self.offset = 0

    def write_bit(self, bit):
        if bit > 0:
            self.current |= 1 << self.offset
        self.offset = (self.offset + 1) & 7

        if self.offset == 0:
            self._write_byte(self.current)
            self.current = 0

    # x is the integer to be transformed to binary using k figures
    def write_int(self, x, k):
        for i in xrange(k-1, -1, -1):
            self.write_bit(x & (1 << i))

    def _write_byte(self, byte):
        self.file.write(code_byte(byte))

    def close(self):
        self.file.close()

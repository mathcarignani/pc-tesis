import struct


class BitStreamWriter(object):
    def __init__(self, filename):
        self.file = open(filename, 'wb')
        self.current = 0
        self.offset = 0

    def write_bit(self, bit):
        if bit > 0:
            self.current |= 1 << self.offset
        self.offset = (self.offset + 1) & 7

        if self.offset == 0:
            print 'code'
            print self.current
            self.file.write(struct.pack('B', self.current))
            self.current = 0

    def close(self):
        self.file.close()

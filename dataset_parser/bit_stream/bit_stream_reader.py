from utils import Utils


class BitStreamReader(object):
    def __init__(self, filename):
        self.file = open(filename, 'rb')
        self.current = 0
        self.offset = 0

    def read_bit(self):
        ans = self.current & (1 << self.offset)
        self.offset = (self.offset + 1) & 7

        if self.offset == 0:
            print 'decode'
            self.current = Utils.decode_byte(self.file.read(1))
            print self.current

        return ans

    def close(self):
        self.file.close()

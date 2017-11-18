import struct


class Utils(object):
    @staticmethod
    def code_byte(byte):
        return struct.pack('B', byte)

    @staticmethod
    def decode_byte(byte):
        return struct.unpack('B', byte)[0]

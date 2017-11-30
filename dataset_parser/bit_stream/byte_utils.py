import struct


def code_byte(byte):
    return struct.pack('B', byte)


def decode_byte(byte):
    return struct.unpack('B', byte)[0]

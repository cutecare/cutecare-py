
HANDLE_READ_SENSOR_DATA = 0x35
HANDLE_WRITE_MODE_CHANGE = 0x33
DATA_MODE_CHANGE = bytes([0xA0, 0x1F])

TEST_MAC = '11:22:33:44:55'

INVALID_DATA = b'\xaa\xbb\xcc\xdd\xee\xff\x99\x88\x77\x66\x00\x00\x00\x00\x00\x00'

import unittest
import pytest

from test import HANDLE_WRITE_MODE_CHANGE, DATA_MODE_CHANGE
from cutecare.backends import BluetoothBackendException
from cutecare.backends.gatttool import GatttoolBackend


class TestGatttoolBackend(unittest.TestCase):

    def setUp(self):
        self.backend = GatttoolBackend(retries=0, timeout=20)

    @pytest.mark.usefixtures("mac")
    def test_read(self):
        self.backend.connect(self.mac)
        result = self.backend.read_handle(0)
        self.assertIsNotNone(result)
        self.backend.disconnect()

    @pytest.mark.usefixtures("mac")
    def test_write(self):
        self.backend.connect(self.mac)
        result = self.backend.write_handle(HANDLE_WRITE_MODE_CHANGE, DATA_MODE_CHANGE)
        self.assertIsNotNone(result)
        self.backend.disconnect()

    def test_read_not_connected(self):
        try:
            self.backend.read_handle(0)
            self.fail('should have thrown an exception')
        except ValueError:
            pass
        except BluetoothBackendException:
            pass

    def test_check_backend(self):
        self.backend.check_backend()

    def test_parse_bytes(self):
        result = """
        value: 01 02 03 04
        value: 05 06 07 08 
        value: 09
        """
        bytes = self.backend.parseBytes(result)
        self.assertEqual(bytes[0], 5)

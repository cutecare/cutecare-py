from cutecare.poller import CuteCarePollerCC41A as CuteCarePoller

import unittest
from test.unit_tests import MockBackend
from test import HANDLE_WRITE_MODE_CHANGE, HANDLE_READ_SENSOR_DATA, INVALID_DATA


class TestCuteCarePoller(unittest.TestCase):
    TEST_MAC = '11:22:33:44:55:66'

    def test_format_bytes(self):
        """Test conversion of bytes to string."""
        self.assertEqual('AA BB 00', CuteCarePoller._format_bytes([0xAA, 0xBB, 0x00]))

    def test_read_measurements(self):
        poller = CuteCarePoller(self.TEST_MAC, MockBackend)
        backend = self._get_backend(poller)

        backend.value = 567
        backend.expected_write_handles.add(HANDLE_WRITE_MODE_CHANGE)

        self.assertAlmostEqual(backend.value, poller.parameter_value(), delta=0.11)
        self.assertEqual(1, len(backend.written_handles))
        self.assertEqual((HANDLE_WRITE_MODE_CHANGE, b'\xA0\x1F'), backend.written_handles[0])

    def test_invalid_data_old(self):
        """Check if reading of the data fails, when invalid data is received.

        Try this with an old version number.
        """
        poller = CuteCarePoller(self.TEST_MAC, MockBackend)
        backend = self._get_backend(poller)

        backend.override_read_handles[HANDLE_READ_SENSOR_DATA] = INVALID_DATA
        self.assertRaises(OSError, poller.parameter_value)

    def test_invalid_data_new(self):
        """Check if reading of the data fails, when invalid data is received.

        Try this with a new version number.
        """
        poller = CuteCarePoller(self.TEST_MAC, MockBackend)
        backend = self._get_backend(poller)

        backend.override_read_handles[HANDLE_READ_SENSOR_DATA] = INVALID_DATA
        self.assertRaises(OSError, poller.parameter_value)

    @staticmethod
    def _get_backend(poller):
        return poller._bt_interface.backend

from datetime import datetime, timedelta
from threading import Lock
from cutecare.backends import BluetoothInterface
import logging

_HANDLE_READ_SENSOR_DATA = 0x35
_HANDLE_WRITE_MODE_CHANGE = 0x33
_DATA_MODE_CHANGE = bytes([0xA0, 0x1F])
_LOGGER = logging.getLogger(__name__)


class CuteCarePoller(object):

    def __init__(self, mac, backend, cache_timeout=600, retries=3, adapter='hci0'):
        self._mac = mac
        self._bt_interface = BluetoothInterface(backend, adapter)
        self._cache = None
        self._cache_timeout = timedelta(seconds=cache_timeout)
        self._last_read = None
        self._fw_last_read = datetime.now()
        self.retries = retries
        self.ble_timeout = 10
        self.lock = Lock()

    def name(self):
        return 'CuteCare DIY sensor'

    def fill_cache(self):
        _LOGGER.debug('Filling cache with new sensor data.')
        with self._bt_interface.connect(self._mac) as connection:
            if not connection.write_handle(_HANDLE_WRITE_MODE_CHANGE, _DATA_MODE_CHANGE):
                # If a sensor doesn't work, wait 5 minutes before retrying
                self._last_read = datetime.now() - self._cache_timeout + timedelta(seconds=300)
                return
            self._cache = connection.read_handle(_HANDLE_READ_SENSOR_DATA)
            _LOGGER.debug('Received result for handle %s: %s', \
                          _HANDLE_READ_SENSOR_DATA, self._format_bytes(self._cache))
            if self._cache is not None:
                self._last_read = datetime.now()
            else:
                # If a sensor doesn't work, wait 5 minutes before retrying
                self._last_read = datetime.now() - self._cache_timeout + timedelta(seconds=300)

    def parameter_value(self, read_cached=True):
        """Return a value of one of the monitored paramaters.
        This method will try to retrieve the data from cache and only
        request it by bluetooth if no cached value is stored or the cache is
        expired.
        This behaviour can be overwritten by the "read_cached" parameter.
        """
        # Use the lock to make sure the cache isn't updated multiple times
        with self.lock:
            if (read_cached is False) or \
                    (self._last_read is None) or \
                    (datetime.now() - self._cache_timeout > self._last_read):
                self.fill_cache()
            else:
                _LOGGER.debug("Using cache (%s < %s)",
                              datetime.now() - self._last_read,
                              self._cache_timeout)

        if self._cache:
            return self._parse_data()
        else:
            raise IOError("Could not read data from CuteCase sensor %s" % self._mac)

    def _parse_data(self):
        return self._cache[1] * 256 + self._cache[0]

    @staticmethod
    def _format_bytes(raw_data):
        """Prettyprint a byte array."""
        return ' '.join([format(c, "02x") for c in raw_data]).upper()

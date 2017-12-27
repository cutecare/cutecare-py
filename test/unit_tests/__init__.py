from cutecare.backends import AbstractBackend


class MockBackend(AbstractBackend):
    """Mockup of a Backend and Sensor.

    The behaviour of this Sensors is based on the knowledge there
    is so far on the behaviour of the sensor. So if our knowledge
    is wrong, so is the behaviour of this sensor! Thus is always
    makes sensor to also test against a real sensor.
    """

    def __init__(self, adapter='hci0'):
        super(self.__class__, self).__init__(adapter)
        self._version = (0, 0, 0)
        self.name = ''
        self.value = 0
        self.written_handles = []
        self.expected_write_handles = set()
        self.override_read_handles = dict()
        self.is_available = True

    def check_backend(self):
        """This backend is available when the field is set accordingly."""
        return self.is_available

    def set_version(self, major, minor, patch):
        """Sets the version number to be returned."""
        self._version = (major, minor, patch)

    @property
    def version(self):
        """Get the stored version number as string."""
        return '{}.{}.{}'.format(*self._version)

    def read_handle(self, handle):
        """Read one of the handles that are implemented."""
        return self._read_sensor_data()

    def read_handle_listen(self, handle):
        """Read one of the handles that are implemented."""
        return self._read_sensor_data()

    def write_handle(self, handle, value):
        """Writing handles just stores the results in a list."""
        self.written_handles.append((handle, value))
        return handle in self.expected_write_handles

    def _read_sensor_data(self):
        """Recreate sensor data from the fields of this class."""
        result = [0xFE]*2
        temp = int(self.value)
        result[1] = int(temp % 256)
        result[0] = int(temp / 256)
        return bytes(result)

    def _read_name(self):
        """Convert the name into a byte array and return it."""
        return [ord(c) for c in self.name]

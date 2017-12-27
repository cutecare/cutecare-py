import unittest
import pytest
from cutecare.poller import CuteCarePollerCC41A as CuteCarePoller
from cutecare.backends.gatttool import GatttoolBackend
from cutecare.backends.bluepy import BluepyBackend


class TestEverythingGatt(unittest.TestCase):
    def setUp(self):
        self.backend_type = GatttoolBackend

    @pytest.mark.usefixtures("mac")
    def test_everything(self):
        assert hasattr(self, "mac")
        poller = CuteCarePoller(self.mac, self.backend_type)
        self.assertIsNotNone(poller.name())
        self.assertIsNotNone(poller.parameter_value())


class TestEverythingBluepy(TestEverythingGatt):
    def setUp(self):
        self.backend_type = BluepyBackend

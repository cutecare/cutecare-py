from cutecare.backends.bluepy import BluepyBackend
from test.integration_tests.test_gatttool_backend import TestGatttoolBackend

class TestBluepyBackend(TestGatttoolBackend):

    def setUp(self):
        self.backend = BluepyBackend()

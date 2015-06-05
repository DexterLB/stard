import unittest
import os
import inspect

os.environ['XDG_CONFIG_HOME'] = os.path.join(os.getcwd(),
                                             'test_samples/config_home')
import service
from test_samples.config_home.stard import empty

class TestLoadingServices(unittest.TestCase):
    def assertSameClass(self, a, b):
        self.assertEqual(inspect.getsource(a), inspect.getsource(b))

    def test_load_empty_service(self):
        sample = service.service('empty')
        self.assertSameClass(sample.__class__, empty.Service)


if __name__ == '__main__':
    unittest.main()

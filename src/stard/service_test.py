import unittest
import os
import inspect

from service import Manager
from test_samples import empty

class TestManager(unittest.TestCase):
    def assertSameClass(self, a, b):
        self.assertEqual(inspect.getsource(a), inspect.getsource(b))

    def test_load_empty_service_from_given_config_dir(self):
        manager = Manager(config_dirs=['test_samples'])
        sample = manager.service('empty')
        self.assertSameClass(sample.__class__, empty.Service)

    def test_load_service_twice_gives_same_object(self):
        manager = Manager(config_dirs=['test_samples'])
        sample1 = manager.service('empty')
        sample2 = manager.service('empty')
        self.assertIs(sample1, sample2)


if __name__ == '__main__':
    unittest.main()

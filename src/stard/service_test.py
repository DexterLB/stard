import unittest
import os
import inspect

from service import Manager
from test_samples import empty

class TestManager(unittest.TestCase):
    def assertSameClass(self, a, b):
        self.assertEqual(inspect.getsource(a), inspect.getsource(b))

    def setUp(self):
        self.manager = Manager(config_dirs=['test_samples'])

    def test_load_empty_service_from_given_config_dir(self):
        sample = self.manager.service('empty')
        self.assertSameClass(sample.__class__, empty.Service)

    def test_load_service_twice_gives_same_object(self):
        sample1 = self.manager.service('empty')
        sample2 = self.manager.service('empty')
        self.assertIs(sample1, sample2)

    def test_populate_relatives(self):
        father = self.manager.service('father')
        child = self.manager.service('child')
        self.manager.populate_relatives()
        self.assertIn(father, child.parents)
        self.assertIn(child, father.children)


if __name__ == '__main__':
    unittest.main()

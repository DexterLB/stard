import unittest
import os
import inspect

from stard.loader import Loader
from .test_samples import empty

class TestLoader(unittest.TestCase):
    def assertSameClass(self, a, b):
        self.assertEqual(inspect.getsource(a), inspect.getsource(b))

    def setUp(self):
        self.loader = Loader(config_dirs=['test_samples'])

    def test_load_empty_service_from_given_config_dir(self):
        sample = self.loader.service('empty')
        self.assertSameClass(sample.__class__, empty.Service)

    def test_load_service_twice_gives_same_object(self):
        sample1 = self.loader.service('empty')
        sample2 = self.loader.service('empty')
        self.assertIs(sample1, sample2)

    def test_populate_relatives(self):
        father = self.loader.service('father')
        child = self.loader.service('child')
        self.loader.populate_relatives()
        self.assertIn(father, child.parents)
        self.assertIn(child, father.children)


if __name__ == '__main__':
    unittest.main()

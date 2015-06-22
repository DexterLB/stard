import unittest
from service_queue import ServiceQueue

class Vertex:
    def __init__(self, name=None):
        self.parents = set()
        self.children = set()
        self.name = name

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return str(self.name) + ' -> (' + ', '.join(
            str(child.name) for child in self.children
        ) + ')'

class TestServiceQueue(unittest.TestCase):
    def make_graph(self, relations):
        vertices = {}
        for vertex_name in relations.keys():
            vertices[vertex_name] = Vertex(vertex_name)
        
        for parent_name, children_names in relations.items():
            for child_name in children_names:
                vertices[parent_name].children.add(vertices[child_name])
                vertices[child_name].parents.add(vertices[parent_name])

        return vertices

    def setUp(self):
        self.services = self.make_graph({
            1: [2, 3],
            2: [3],
            3: []
        })

    def test_top_start(self):
        for service in self.services.values():
            service.is_running = False

        queue = ServiceQueue(self.services[3], 'start')
        self.assertIs(queue.top(), self.services[1])

    def test_top_stop(self):
        for service in self.services.values():
            service.is_running = True

        queue = ServiceQueue(self.services[1], 'stop')
        self.assertIs(queue.top(), self.services[3])

    def test_to_do_start(self):
        self.services[1].is_running = True
        self.services[2].is_running = False
        self.services[3].is_running = True

        queue = ServiceQueue(self.services[3], 'start')

        self.assertEqual(queue.to_do, {self.services[2]})
        self.assertEqual(queue.done, {self.services[1], self.services[3]})

    def test_to_do_stop(self):
        self.services[1].is_running = True
        self.services[2].is_running = False
        self.services[3].is_running = True

        queue = ServiceQueue(self.services[1], 'stop')

        self.assertEqual(queue.done, {self.services[2]})
        self.assertEqual(queue.to_do, {self.services[1], self.services[3]})

    def test_pop_finalize_start(self):
        for service in self.services.values():
            service.is_running = False

        queue = ServiceQueue(self.services[3], 'start')

        self.assertIs(queue.pop(), self.services[1])
        self.assertEqual(queue.current, {self.services[1]})
        self.assertEqual(queue.to_do, {self.services[3], self.services[2]})
        self.assertEqual(queue.done, set())

        queue.finalize(self.services[1])

        self.assertEqual(queue.current, set())
        self.assertEqual(queue.to_do, {self.services[3], self.services[2]})
        self.assertEqual(queue.done, {self.services[1]})

    def test_pop_finalize_stop(self):
        for service in self.services.values():
            service.is_running = True

        queue = ServiceQueue(self.services[1], 'stop')

        self.assertIs(queue.pop(), self.services[3])
        self.assertEqual(queue.current, {self.services[3]})
        self.assertEqual(queue.to_do, {self.services[1], self.services[2]})
        self.assertEqual(queue.done, set())

        queue.finalize(self.services[3])

        self.assertEqual(queue.current, set())
        self.assertEqual(queue.to_do, {self.services[1], self.services[2]})
        self.assertEqual(queue.done, {self.services[3]})


if __name__ == '__main__':
    unittest.main()

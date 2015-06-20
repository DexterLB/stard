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
    
    def test_top_start(self):
        services = self.make_graph({
            1: [2, 3],
            2: [3],
            3: []
        })
        for service in services.values():
            service.is_running = False

        queue = ServiceQueue(services[3], 'start')
        self.assertIs(queue.top(), services[1])

    def test_top_stop(self):
        services = self.make_graph({
            1: [2, 3],
            2: [3],
            3: []
        })
        for service in services.values():
            service.is_running = True

        queue = ServiceQueue(services[1], 'stop')
        self.assertIs(queue.top(), services[3])

if __name__ == '__main__':
    unittest.main()

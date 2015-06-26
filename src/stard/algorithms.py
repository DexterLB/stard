
# dfs
def walk_parents(vertex):
    return sum(
        (walk_parents(parent) for parent in vertex.parents),
        []
    ) + [vertex]

def walk_children(vertex):
    return sum(
        (walk_children(child) for child in vertex.children),
        []
    ) + [vertex]

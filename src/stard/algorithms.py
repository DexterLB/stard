
# dfs
def walk_parents(vertex):
    return [vertex] + sum(
        (walk_parents(parent) for parent in vertex.parents),
        []
    )

def walk_children(vertex):
    return [vertex] + sum(
        (walk_children(child) for child in vertex.children),
        []
    )

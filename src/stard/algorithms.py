
# dfs
def walk_parents(vertex):
    return vertex.parents + sum(
        (walk_parents(parent) for parent in vertex.parents),
        []
    )

def walk_children(vertex):
    return vertex.children + sum(
        (walk_children(child) for child in vertex.children),
        []
    )

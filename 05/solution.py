from collections import deque
from typing import Dict, Set


def parse(filename):
    graph = {}
    orderings = []
    graph_done = False
    for line in open(filename):
        if line.isspace():
            graph_done = True
            continue
        if not graph_done:
            src, dest = [int(node) for node in line.strip().split("|")]
            if src not in graph:
                graph[src] = set()
            if dest not in graph:
                graph[dest] = set()
            graph[src].add(dest)
        else:
            orderings.append([int(node) for node in line.strip().split(",")])
    return graph, orderings


def kahn(graph):
    indegrees = {node: 0 for node in graph}
    toposort = []
    sources = deque([])
    for node in graph:
        for neighbor in graph[node]:
            indegrees[neighbor] += 1
    for node in indegrees:
        if indegrees[node] == 0:
            sources.append(node)
    while len(sources) > 0:
        source = sources.popleft()
        toposort.append(source)
        for neighbor in graph[source]:
            indegrees[neighbor] -= 1
            if indegrees[neighbor] == 0:
                sources.append(neighbor)
    return toposort


def part1(filename):
    graph, orderings = parse(filename)

    def ordering_valid(graph: Dict[int, Set[int]], ordering):
        ordering_nodes = set(ordering)
        induced_subgraph = {
            node: set(ordering_nodes & graph[node]) for node in ordering_nodes
        }
        topological_ordering = kahn(induced_subgraph)
        return topological_ordering == ordering

    answer = 0
    for ordering in orderings:
        if ordering_valid(graph, ordering):
            middle = ordering[len(ordering) // 2]
            answer += middle
    return answer


def part2(filename):
    graph, orderings = parse(filename)

    def toposort_if_not_valid(graph: Dict[int, Set[int]], ordering):
        ordering_nodes = set(ordering)
        induced_subgraph = {
            node: set(ordering_nodes & graph[node]) for node in ordering_nodes
        }
        topological_ordering = kahn(induced_subgraph)
        return topological_ordering if topological_ordering != ordering else None

    answer = 0
    for ordering in orderings:
        toposort = toposort_if_not_valid(graph, ordering)
        if toposort is not None:
            middle = toposort[len(ordering) // 2]
            answer += middle
    return answer


if __name__ == "__main__":
    print(part1("example.txt"))
    print(part1("input.txt"))
    print(part2("example.txt"))
    print(part2("input.txt"))

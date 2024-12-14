from collections import deque


def parse(filename):
    coord_to_height = {}
    zeros = []
    for row, line in enumerate(open(filename)):
        for col, height in enumerate(line.strip()):
            height = int(height)
            if height == 0:
                zeros.append(complex(row, col))
            coord_to_height[complex(row, col)] = height
    graph = {coord: [] for coord in coord_to_height}
    for coord, height in coord_to_height.items():
        direction = 1j
        for _ in range(4):
            neighbor = coord + direction
            if neighbor in graph and coord_to_height[neighbor] == height + 1:
                graph[coord].append(neighbor)
            direction *= 1j
    return graph, coord_to_height, zeros


def bfs(graph, coord_to_height, start):
    parent = {}
    discovered = set()
    count_of_nines = 0
    queue = deque([start])
    while len(queue) > 0:
        curr = queue.popleft()
        for neighbor in graph[curr]:
            if neighbor not in discovered:
                discovered.add(neighbor)
                parent[neighbor] = curr
                queue.append(neighbor)
                if coord_to_height[neighbor] == 9:
                    count_of_nines += 1
    return count_of_nines


def num_paths_to_nines(graph, coord_to_height, zero):
    paths_to_coord = {coord: 0 for coord in graph}
    paths_to_coord[zero] = 1
    queue = {zero}
    for _ in range(0, 9):
        next_queue = set()
        for coord in queue:
            for neighbor in graph[coord]:
                paths_to_coord[neighbor] += paths_to_coord[coord]
                next_queue.add(neighbor)
        queue = next_queue
    return sum(paths_to_coord[nine] for nine in queue)


if __name__ == "__main__":
    graph, coord_to_height, zeros = parse("example_small.txt")
    print(bfs(graph, coord_to_height, zeros[0]))
    graph, coord_to_height, zeros = parse("example_large.txt")
    print(sum(bfs(graph, coord_to_height, zero) for zero in zeros))
    graph, coord_to_height, zeros = parse("input.txt")
    print(sum(bfs(graph, coord_to_height, zero) for zero in zeros))
    graph, coord_to_height, zeros = parse("example_large.txt")
    print(sum(num_paths_to_nines(graph, coord_to_height, zero) for zero in zeros))
    graph, coord_to_height, zeros = parse("input.txt")
    print(sum(num_paths_to_nines(graph, coord_to_height, zero) for zero in zeros))

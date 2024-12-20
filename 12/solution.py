from collections import deque, defaultdict
from typing import List, Dict, Set, Optional, Tuple
from itertools import combinations


def parse(filename):
    grid = []
    for line in open(filename):
        grid.append(list(line.strip()))
    return grid


def grid_at_complex(grid, c: complex):
    return grid[int(c.real)][int(c.imag)]


def in_bounds(c: complex, *, height, width):
    return 0 <= c.real < height and 0 <= c.imag < width


def neighbors_of_complex(node: complex):
    neighbor_offset = 1j
    for _ in range(4):
        neighbor = neighbor_offset + node
        neighbor_offset *= 1j
        yield neighbor


def graph_of(grid: List[List[str]]) -> Tuple[Dict[complex, List[complex]], int, int]:
    height = len(grid)
    width = len(grid[0])
    graph: Dict[complex, list[complex]] = {
        complex(r, c): [] for c in range(width) for r in range(height)
    }
    for row_idx, row in enumerate(grid):
        for col_idx, c in enumerate(row):
            coord = complex(row_idx, col_idx)
            for neighbor in neighbors_of_complex(coord):
                if in_bounds(
                    neighbor, height=height, width=width
                ) and c == grid_at_complex(grid, neighbor):
                    graph[coord].append(neighbor)
    return dict(graph), height, width


def find_regions(graph: Dict[complex, List[complex]]) -> List[Set[complex]]:
    # idea: bfs to find region, smash that into perimeter function

    # shared discovered set
    discovered = set()

    def bfs(graph, start) -> Optional[Set[complex]]:
        if start in discovered:
            return None
        queue = deque([start])
        region = {start}
        discovered.add(start)
        while len(queue) > 0:
            node = queue.popleft()
            for neighbor in graph[node]:
                if neighbor not in discovered:
                    discovered.add(neighbor)
                    queue.append(neighbor)
                    region.add(neighbor)
        return region

    regions = []
    for node in graph:
        region_opt = bfs(graph, node)
        if region_opt is not None:
            regions.append(region_opt)
    return regions


def area_of(region) -> int:
    return len(region)


def perimeter_of(graph: Dict[complex, List[complex]], region: Set[complex]) -> int:
    # genius stolen idea: the perimeter that a given sq contributes =
    # 4 - (num matching neighbors)
    def perimeter_for_node(node):
        return 4 - len(graph[node])

    perimeter = sum(perimeter_for_node(node) for node in region)
    return perimeter


def sides_of(grid, graph, region, height, width, *, debug) -> int:
    def sides_of(node):
        c = grid_at_complex(grid, node)
        neighbors = graph[node]
        num_neighbors = len(neighbors)
        if num_neighbors == 0:
            return 4
        elif num_neighbors == 1:
            return 2
        elif num_neighbors == 2:
            diff1, diff2 = [neighbor - node for neighbor in graph[node]]  # len 2
            corner = node + diff1 + diff2
            if node == corner:
                return 0
            answer = 1  # there's always a vertex if perp neighbors, might be 2 if opposite corner also doesn't match
            if c != grid_at_complex(grid, corner):
                answer += 1
            return answer
        else:
            # scan the corners
            num_corners_not_matching = 0
            diffs = [neighbor - node for neighbor in graph[node]]
            for diff1, diff2 in combinations(diffs, 2):
                corner = node + diff1 + diff2
                if node == corner:
                    continue
                if debug:
                    print(node, diff1, diff2, corner)
                if not in_bounds(
                    corner, height=height, width=width
                ) or c != grid_at_complex(grid, corner):
                    num_corners_not_matching += 1
            return num_corners_not_matching

    answer = sum(sides_of(node) for node in region)
    if debug:
        print(answer)
    return answer


def part1(grid):
    graph, height, width = graph_of(grid)
    regions = find_regions(graph)
    return sum(area_of(region) * perimeter_of(graph, region) for region in regions)


def part2(grid, *, debug=False):
    graph, height, width = graph_of(grid)
    regions = find_regions(graph)
    return sum(
        area_of(region) * sides_of(grid, graph, region, height, width, debug=debug)
        for region in regions
    )


if __name__ == "__main__":
    print(part1(parse("example1.txt")))
    print(part1(parse("example2.txt")))
    print(part1(parse("example3.txt")))
    print(part1(parse("input.txt")))
    print("--------part2-------")
    print(part2(parse("example1.txt"), debug=False))  # 80
    print(part2(parse("example2.txt")))  # 436
    print(part2(parse("examplee.txt")))  # 236
    print(part2(parse("exampleabba.txt"), debug=False))  # 368
    print(part2(parse("example3.txt")))  # 1206
    print(part2(parse("input.txt")))

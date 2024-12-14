from collections import defaultdict
from itertools import combinations
from typing import Dict, List, Tuple
import math


def parse(filename):
    grid = []
    for line in open(filename):
        grid.append(list(line.strip()))
    return grid, len(grid[0]), len(grid)


def in_bounds(row, col, height, width):
    return 0 <= row < height and 0 <= col < width


def get_symbol_to_nodes(grid) -> Dict[str, List[Tuple[int, int]]]:
    symbol_to_nodes = defaultdict(list)
    for y, row in enumerate(grid):
        for x, symbol in enumerate(row):
            if symbol != ".":
                symbol_to_nodes[symbol].append((x, y))
    return symbol_to_nodes


def part1(grid, height, width):
    symbol_to_nodes = get_symbol_to_nodes(grid)
    antinode_locations = set()
    for locations in symbol_to_nodes.values():
        for (row1, col1), (row2, col2) in combinations(locations, 2):
            row_diff, col_diff = (row2 - row1, col2 - col1)
            antinode1 = (row1 - row_diff, col1 - col_diff)
            antinode2 = (row2 + row_diff, col2 + col_diff)
            for antinode in [antinode1, antinode2]:
                if in_bounds(*antinode, height, width):
                    antinode_locations.add(antinode)
    return len(antinode_locations)


def part2(grid, height, width):
    symbol_to_nodes = get_symbol_to_nodes(grid)
    antinode_locations = set()

    def add_until_out_of_bounds(row, col, row_diff, col_diff, *, positive=True):
        while in_bounds(row, col, height, width):
            antinode = (row, col)
            antinode_locations.add(antinode)
            multiplier = 1 if positive else -1
            row += multiplier * row_diff
            col += multiplier * col_diff

    for locations in symbol_to_nodes.values():
        for (row1, col1), (row2, col2) in combinations(locations, 2):
            # antinode along the entire line, as long as its inbounds
            row_diff, col_diff = (row2 - row1, col2 - col1)
            gcd = math.gcd(row_diff, col_diff)
            normalized_row_diff, normalized_col_diff = row_diff // gcd, col_diff // gcd
            row, col = row1, col1
            add_until_out_of_bounds(
                row, col, normalized_row_diff, normalized_col_diff, positive=True
            )
            add_until_out_of_bounds(
                row, col, normalized_row_diff, normalized_col_diff, positive=False
            )
    return len(antinode_locations)


if __name__ == "__main__":
    grid, height, width = parse("example.txt")
    print(part1(grid, height, width))
    print(part1(*parse("input.txt")))
    print(part2(*parse("example.txt")))
    print(part2(*parse("input.txt")))

from typing import List


def parse(filename):
    input = []
    for line in open(filename):
        input.append(list(line.strip()))
    return input


def part1(grid: List[List[str]], search_string, directions):
    search_string_len = len(search_string)
    width = len(grid[0])
    height = len(grid)

    def in_bounds(row, col):
        return 0 <= row < height and 0 <= col < width

    occurrences = 0
    for row_idx in range(height):
        for col_idx in range(width):
            for row_diff, col_diff in directions:
                for i in range(search_string_len):
                    row = row_idx + i * row_diff
                    col = col_idx + i * col_diff
                    if not (in_bounds(row, col) and grid[row][col] == search_string[i]):
                        break
                    else:
                        if i == search_string_len - 1:
                            occurrences += 1
    return occurrences


def part2(grid: List[List[str]]):
    width = len(grid[0])
    height = len(grid)
    subgrid_side = len("MAS")
    directions = {(1, 1), (-1, 1), (-1, -1), (1, -1)}
    occurrences = 0
    for row_idx in range(height - subgrid_side + 1):
        for col_idx in range(width - subgrid_side + 1):
            subgrid = [
                grid[row_idx + i][col_idx : col_idx + subgrid_side]
                for i in range(subgrid_side)
            ]
            if part1(subgrid, "MAS", directions) == 2:

                occurrences += 1
    return occurrences


if __name__ == "__main__":
    directions_part1 = {
        (1, 0),
        (0, 1),
        (1, 1),
        (-1, 1),
        (-1, 0),
        (0, -1),
        (-1, -1),
        (1, -1),
    }
    print(part1(parse("example.txt"), "XMAS", directions_part1))
    print(part1(parse("input.txt"), "XMAS", directions_part1))
    print(part2(parse("example.txt")))
    print(part2(parse("input.txt")))

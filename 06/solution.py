from collections import defaultdict
from typing import Set, Tuple


def parse(filename: str):
    squares = set()
    for row_idx, line in enumerate(open(filename)):
        height = row_idx
        for col_idx, char in enumerate(line.strip()):
            width = col_idx
            if char == "#":
                squares.add((row_idx, col_idx))
            elif char == "^":
                guard_pos = (row_idx, col_idx)
    obstacle_rows = defaultdict(set)
    obstacle_cols = defaultdict(set)
    for row, col in squares:
        obstacle_rows[row].add(col)
        obstacle_cols[col].add(row)
    return squares, obstacle_rows, obstacle_cols, guard_pos, height + 1, width + 1


def draw_grid(obstacle_squares, positions, width, height):
    grid = []
    for row in range(height):
        row_rep = []
        for col in range(width):
            if (row, col) in obstacle_squares:
                row_rep.append("#")
            elif (row, col) in positions:
                row_rep.append("X")
            else:
                row_rep.append(".")
        grid.append("".join(row_rep))
    return grid


def part1(
    squares,
    obstacle_rows: defaultdict[int, Set[int]],
    obstacle_cols: defaultdict[int, Set[int]],
    guard_pos: Tuple[int, int],
    height,
    width,
):
    """
    squares: all (row, col) pairs of obstacles
    obstacle_rows[i]: set of columns for which there is an obstacle in row i
    obstacle_cols[j]: set of rows for which there is an obstacle in column j

    returns None if its a loop
    """
    positions = set()
    guard_row, guard_col = guard_pos
    direction = "up"
    while True:
        if direction == "up":
            # first one less than
            for obstacle_row in sorted(obstacle_cols[guard_col], reverse=True):
                if obstacle_row < guard_row:
                    len_before = len(positions)
                    squares_to_add = set(
                        (row, guard_col, direction)
                        for row in range(guard_row, obstacle_row, -1)
                    )
                    positions.update(squares_to_add)
                    direction = "right"
                    guard_row = obstacle_row + 1
                    break
            else:
                # exit grid
                positions.update(
                    set((row, guard_col, direction) for row in range(guard_row, 0, -1))
                )
                return positions

        elif direction == "down":
            for obstacle_row in sorted(obstacle_cols[guard_col]):
                if guard_row < obstacle_row:
                    len_before = len(positions)
                    squares_to_add = set(
                        (row, guard_col, direction)
                        for row in range(guard_row, obstacle_row)
                    )
                    positions.update(squares_to_add)
                    direction = "left"
                    guard_row = obstacle_row - 1
                    break
            else:
                positions.update(
                    set((row, guard_col, direction) for row in range(guard_row, height))
                )
                return positions

        elif direction == "left":
            for obstacle_col in sorted(obstacle_rows[guard_row], reverse=True):
                if guard_col > obstacle_col:
                    len_before = len(positions)
                    squares_to_add = set(
                        (guard_row, col) for col in range(guard_col, obstacle_col, -1)
                    )
                    positions.update(squares_to_add)
                    direction = "up"
                    if len(positions) == len_before and len(squares_to_add) > 1:
                        return None
                    guard_col = obstacle_col + 1
                    break
            else:
                positions.update(
                    set((guard_row, col, direction) for col in range(guard_col, 0, -1))
                )
                return positions
        elif direction == "right":
            for obstacle_col in sorted(obstacle_rows[guard_row]):
                if guard_col < obstacle_col:
                    len_before = len(positions)
                    squares_to_add = set(
                        (guard_row, col) for col in range(guard_col, obstacle_col)
                    )
                    positions.update(squares_to_add)
                    if len(positions) == len_before and len(squares_to_add) > 1:
                        return None
                    direction = "down"
                    guard_col = obstacle_col - 1
                    break
            else:
                positions.update(
                    set((guard_row, col, direction) for col in range(guard_col, width))
                )
                return positions


def part1_walk(squares, obstacle_rows, obstacle_cols, guard_pos, height, width):
    positions = set()
    direction = complex(-1)
    guard_pos = complex(*guard_pos)

    def next_position(direction, guard_pos):
        return guard_pos + direction

    while True:
        if (guard_pos, direction) in positions:
            return None
        positions.add((guard_pos, direction))
        next_pos = next_position(direction, guard_pos)
        if (
            next_pos.real < 0
            or next_pos.real >= height
            or next_pos.imag < 0
            or next_pos.imag >= width
        ):
            return positions
        if (next_pos.real, next_pos.imag) in squares:
            next_direction = direction * -1j
            direction = next_direction
        else:
            guard_pos = next_pos


def part2(
    squares,
    obstacle_rows: defaultdict[int, Set[int]],
    obstacle_cols: defaultdict[int, Set[int]],
    guard_pos: Tuple[int, int],
    height,
    width,
):
    answer = 0
    for row in range(height):
        for col in range(width):
            if (row, col) == guard_pos or (row, col) in squares:
                continue
            # try
            squares.add((row, col))
            if (
                part1_walk(
                    squares, obstacle_rows, obstacle_cols, guard_pos, height, width
                )
                is None
            ):
                answer += 1
            squares.remove((row, col))
    return answer


if __name__ == "__main__":
    # print(len(positions))
    # positions = part1(*parse("input.txt"))
    # print(len(positions))

    squares, obstacle_rows, obstacle_cols, guard_pos, height, width = parse(
        "example.txt"
    )
    positions = part1_walk(
        squares, obstacle_rows, obstacle_cols, guard_pos, height, width
    )
    positions_no_direction = {pos for pos, dir in positions}
    print(len(positions_no_direction))
    squares, obstacle_rows, obstacle_cols, guard_pos, height, width = parse("input.txt")
    positions = part1_walk(*parse("input.txt"))
    positions_no_direction = {pos for pos, dir in positions}
    print(len(positions_no_direction))

    print(part2(*parse("example.txt")))
    print(part2(*parse("input.txt")))

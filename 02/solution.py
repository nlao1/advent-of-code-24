from itertools import pairwise


def parse(filename):
    levels = []
    with open(filename) as f:
        for line in f:
            levels.append([int(x.strip()) for x in line.split()])
        return levels


MIN_DIFFERENCE = 1
MAX_DIFFERENCE = 3


def level_is_safe(level):
    level_is_increasing = level == sorted(level)
    level_is_decreasing = level == sorted(level, reverse=True)
    if not level_is_increasing and not level_is_decreasing:
        return 0
    for curr, next in pairwise(level):
        if level_is_increasing:
            diff = next - curr
            if diff > MAX_DIFFERENCE or diff < MIN_DIFFERENCE:
                return 0
        elif level_is_decreasing:
            diff = curr - next
            if diff > MAX_DIFFERENCE or diff < MIN_DIFFERENCE:
                return 0
    return 1


def part1(levels):
    return sum(level_is_safe(level) for level in levels)


def part2(levels):
    # initial solution, quadratic time complexity for each level so O(n^3)
    def level_with_dampener_is_safe(level):
        return any(level_is_safe(level[:i] + level[i + 1 :]) for i in range(len(level)))

    return sum(1 if level_with_dampener_is_safe(level) else 0 for level in levels)


if __name__ == "__main__":
    print(part1(parse("example.txt")))
    print(part1(parse("input.txt")))
    print(part2(parse("example.txt")))
    print(part2(parse("input.txt")))

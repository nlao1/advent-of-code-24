import re


def parse(filename) -> str:
    input = []
    for line in open(filename):
        input.append(line)
    return "".join(input)


def part1(input: str) -> int:
    pattern = re.compile(r"mul\((\d+),(\d+)\)")
    return sum(
        num1 * num2
        for num1, num2 in map(lambda x: map(int, x), re.findall(pattern, input))
    )


def part2(input: str) -> int:
    mul_pattern = r"mul\((\d+),(\d+)\)"
    do_pattern = r"do\(\)"
    dont_pattern = r"don't\(\)"
    pattern = re.compile(rf"({do_pattern})|{mul_pattern}|({dont_pattern})")
    enabled = True
    answer = 0
    for do, num1, num2, dont in re.findall(pattern, input):
        if do:
            enabled = True
        elif dont:
            enabled = False
        elif num1 and num2:
            if enabled:
                answer += int(num1) * int(num2)
    return answer


if __name__ == "__main__":
    print(part1(parse("example.txt")))
    print(part1(parse("input.txt")))
    print(part2(parse("example2.txt")))
    print(part2(parse("input.txt")))

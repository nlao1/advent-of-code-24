from typing import List
from collections import defaultdict


def parse(filename):
    return list(map(int, open(filename).readline().strip().split()))


def part1(nums: List[int], num_blinks: int):
    # not optimal but good enough
    nums_dict = defaultdict(int)
    for num in nums:
        nums_dict[num] += 1

    def output(num: int) -> List[int]:
        num_str = str(num)
        num_digits = len(num_str)
        if num == 0:
            return [1]
        elif num_digits % 2 == 0:
            num1, num2 = num_str[: num_digits // 2], num_str[num_digits // 2 :]
            return [int(x) for x in [num1, num2]]
        else:
            return [num * 2024]

    def blink(nums):
        new_nums_dict = defaultdict(int)
        for num, count in nums_dict.items():
            for output_num in output(num):
                new_nums_dict[output_num] += count
        return new_nums_dict

    for _ in range(num_blinks):
        nums_dict = blink(nums)
    return sum(nums_dict.values())


if __name__ == "__main__":
    print(part1(parse("example.txt"), 1))
    print(part1(parse("example_large.txt"), 6))
    print(part1(parse("input.txt"), 25))
    print(part1(parse("input.txt"), 75))

from typing import List, Tuple


def parse(filename):
    nums = []
    for line in open(filename):
        line = line.strip()
        goal, rest = line.split(":")
        nums.append((int(goal), list(map(int, rest.split()))))
    return nums


def part1(input: List[Tuple[int, List[int]]]) -> int:
    answer = 0

    def test(goal, nums: List[int]):
        if len(nums) == 1:
            return goal == nums[0]
        last_num = nums.pop()
        add = test(goal - last_num, nums[:])
        multiply = False
        if goal % last_num == 0:
            multiply = test(goal // last_num, nums[:])
        return add or multiply

    for goal, nums in input:
        if test(goal, nums):
            answer += goal
    return answer


def part2(input: List[Tuple[int, List[int]]]) -> int:
    answer = 0

    def test(goal, nums: List[int]):
        if len(nums) == 1:
            return goal == nums[0]
        last_num = nums.pop()
        add = test(goal - last_num, nums[:])
        multiply = False
        if goal % last_num == 0:
            multiply = test(goal // last_num, nums[:])
        concat = False
        num_digits_concated = len(str(last_num))
        order_of_magnitude = 10**num_digits_concated
        if goal % order_of_magnitude == last_num:
            concat = test(goal // order_of_magnitude, nums[:])
        return add or multiply or concat

    assert test(7290, [6, 8, 6, 15])

    for goal, nums in input:
        if test(goal, nums):
            answer += goal
    return answer


if __name__ == "__main__":
    print(part1(parse("example.txt")))
    print(part1(parse("input.txt")))
    print(part2(parse("example.txt")))
    print(part2(parse("input.txt")))

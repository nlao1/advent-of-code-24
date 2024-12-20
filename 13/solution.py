from typing import Tuple, List
import re, math


def parse(filename):
    games = []
    a = None
    b = None
    goal = None
    for line in open(filename):
        line = line.strip()

        def button_parse(s: str):
            pattern = re.compile(r"X\+(\d+)\, Y\+(\d+)")
            return tuple(map(int, re.findall(pattern, s)[0]))

        if line.startswith("Button A:"):
            a = button_parse(line)
        if line.startswith("Button B:"):
            b = button_parse(line)
        if line.startswith("Prize:"):
            pattern = re.compile(r"X=(\d+), Y=(\d+)")
            goal = tuple(map(int, re.findall(pattern, line)[0]))
            games.append(Game(goal, a, b))
    return games


class Game:
    COST_A = 3
    COST_B = 1
    MAX_PRESSES_PER_BUTTON = 100

    @staticmethod
    def cost(num_a, num_b):
        return Game.COST_A * num_a + Game.COST_B * num_b

    def __init__(self, goal: Tuple[int, int], a: Tuple[int, int], b: Tuple[int, int]):
        self.goal = goal
        self.a = a
        self.b = b
        self.cost_a = Game.COST_A
        self.cost_b = Game.COST_B

    def determine_cheapest_solution(self):
        # a is always steeper
        if self.a[1] / self.a[0] < self.b[1] / self.b[0]:
            self.a, self.b = self.b, self.a
            self.cost_a, self.cost_b = self.cost_b, self.cost_a
        lo, hi = 0, 10**18
        while lo < hi:
            mid = (lo + hi) // 2
            count_b = (self.goal[0] - self.a[0] * mid) / self.b[0]
            if count_b * self.b[1] + mid * self.a[1] >= self.goal[1]:
                hi = mid
            else:
                lo = mid + 1
        count_a = lo
        count_b = (self.goal[0] - self.a[0] * count_a) // self.b[0]
        if count_a * self.a[1] + count_b * self.b[1] == self.goal[1]:
            return self.cost_a * count_a + self.cost_b * count_b
        return float("inf")

    def __repr__(self) -> str:
        return f"goal: {self.goal}; a: {self.a}; b: {self.b}"


def part1(games: List[Game]):
    answer = 0
    for game in games:
        cheapest = game.determine_cheapest_solution()
        if cheapest < float("inf"):
            answer += cheapest
    return answer


def part2(games: List[Game]):
    # modify games
    # stole an idea off of reddit because I got stuck, but implementing it myself
    # ends up not working somehow
    NEW_GOAL_OFFSET = 10_000_000_000_000
    answer = 0
    for game in games:
        game.goal = game.goal[0] + NEW_GOAL_OFFSET, game.goal[1] + NEW_GOAL_OFFSET
        cheapest = game.determine_cheapest_solution()
        if cheapest < float("inf"):
            answer += cheapest
    return answer


if __name__ == "__main__":
    print(part1(parse("example.txt")))
    print(part1(parse("input.txt")))
    # print(part2(parse("example.txt")))
    # print(part2(parse("input.txt")))

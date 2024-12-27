import re
from typing import List
from functools import reduce
from PIL import Image
import numpy as np


class Robot:
    def __init__(self, p_x, p_y, v_x, v_y):
        self.p_x = p_x
        self.p_y = p_y
        self.v_x = v_x
        self.v_y = v_y

    def __repr__(self) -> str:
        return f"(p_x:{self.p_x}, p_y:{self.p_y}); (v_x:{self.v_x}, v_y:{self.v_y})"


def parse(filename):
    robots = []
    for line in open(filename):
        position_str, velocity_str = line.strip().split()
        position_pattern = r"p=(\d+),(\d+)"
        p_x, p_y = map(int, re.findall(position_pattern, position_str)[0])
        v_x, v_y = map(int, velocity_str.strip().split("=")[1].strip().split(","))
        robots.append(Robot(p_x, p_y, v_x, v_y))
    return robots


def robot_final_position(robot: Robot, width, height, seconds_elapsed):
    x, y = robot.p_x, robot.p_y
    x = (x + seconds_elapsed * robot.v_x) % width
    y = (y + seconds_elapsed * robot.v_y) % height
    return x, y


def find_quadrant(x, y, width, height):
    # 1 2
    # 3 4
    middle_x = width // 2
    middle_y = height // 2
    if 0 <= x < middle_x:
        if 0 <= y < middle_y:
            return 1
        elif middle_y < y < height:
            return 3
        else:
            return -1
    elif middle_x < x < width:
        if 0 <= y < middle_y:
            return 2
        elif middle_y < y < height:
            return 4
        else:
            return -1
    else:
        return -1


def part1(robots: List[Robot], *, width, height, seconds_elapsed):
    final_positions = [
        robot_final_position(robot, width, height, seconds_elapsed) for robot in robots
    ]
    quadrant_counts = {x: 0 for x in range(1, 5)}
    for x, y in final_positions:
        quadrant = find_quadrant(x, y, width, height)
        if quadrant != -1:
            quadrant_counts[quadrant] += 1
    return reduce(lambda x, y: x * y, quadrant_counts.values())


def save_image(robots, *, width, height, num_seconds_elapsed):
    image = np.zeros((101, 103))
    for robot in robots:
        x, y = robot_final_position(
            robot, width, height, seconds_elapsed=num_seconds_elapsed
        )
        image[x, y] += 1
    print(image)
    im = Image.fromarray(image, mode="I")
    im.save(f"images/{num_seconds_elapsed}.png")


def part2(
    robots: List[Robot],
    *,
    width,
    height,
    min_seconds_elapsed=1000,
    max_seconds_elapsed=10000,
):
    for x in range(min_seconds_elapsed, max_seconds_elapsed):
        save_image(robots, width=width, height=height, num_seconds_elapsed=x)


if __name__ == "__main__":
    # print(*parse("example.txt"), sep="\n")
    print(part1(parse("example.txt"), width=11, height=7, seconds_elapsed=100))
    print(part1(parse("input.txt"), width=101, height=103, seconds_elapsed=100))
    # part2(parse("input.txt"), width=101, height=103)
    save_image(parse("input.txt"), width=101, height=103, num_seconds_elapsed=100002)

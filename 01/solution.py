from collections import defaultdict

filename = "example.txt"

def parse(filename):
    list1, list2 = [], []
    with open(filename) as f:
        for line in f:
            num1, num2 = line.split()
            num1 = num1.strip()
            num2 = num2.strip()
            list1.append(int(num1))
            list2.append(int(num2))
        return list1, list2


def part1(list1, list2):
    answer = 0
    for num1, num2 in zip(sorted(list1), sorted(list2)):
        answer += abs(num1 - num2)
    return answer

def part2(list1, list2):
    counts = defaultdict(int)
    for num in list2:
        counts[num] += 1
    return(sum(counts[num] * num for num in list1))

if __name__ == "__main__":
    print(part1(*parse("example.txt")))
    print(part1(*parse("input.txt")))
    print(part2(*parse("example.txt")))
    print(part2(*parse("input.txt")))

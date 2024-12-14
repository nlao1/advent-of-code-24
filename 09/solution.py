def parse(filename, *, output_as_ranges=False):
    line = open(filename).readline().strip()
    tape = []
    index = 0
    space_indices = []
    space_ranges = []
    data_ranges = []
    total_data = 0
    for i, amount in enumerate(line):
        amount = int(amount)
        c = str(i // 2) if i % 2 == 0 else "."
        if c == ".":
            space_indices.extend(range(index, index + amount))
            space_ranges.append((index, amount))
        else:
            data_ranges.append((index, amount))
            total_data += amount
        tape.extend([c] * amount)
        index += amount
    return (
        tape,
        space_ranges if output_as_ranges else space_indices,
        data_ranges if output_as_ranges else total_data,
    )


def calculate_checksum(tape):
    return sum(i * int(tape[i]) if tape[i].isdigit() else 0 for i in range(len(tape)))


def part1(tape, space_locs, total_data):
    curr_space_loc_idx = 0
    i = len(tape) - 1
    while i > total_data - 1:
        if tape[i] != ".":
            space_loc = space_locs[curr_space_loc_idx]
            tape[space_loc], tape[i] = (
                tape[i],
                tape[space_loc],
            )
            curr_space_loc_idx += 1
        i -= 1
    return calculate_checksum(tape)


def part2(tape, space_ranges, data_ranges):
    for data_range in reversed(data_ranges):
        data_start, data_size = data_range
        for i in range(len(space_ranges)):
            space_start, space_size = space_ranges[i]
            if space_start > data_start:
                break
            remaining_space = space_size - data_size
            if remaining_space >= 0:
                tape[space_start : space_start + data_size] = tape[
                    data_start : data_start + data_size
                ]
                tape[data_start : data_start + data_size] = ["."] * data_size
                space_ranges[i] = (
                    space_start + data_size,
                    remaining_space,
                )
                break
        # move
    return calculate_checksum(tape)


if __name__ == "__main__":
    tape, space_indices, total_data = parse("example.txt")
    print(part1(tape, space_indices, total_data))
    print(part1(*parse("input.txt")))
    tape, space_ranges, data_ranges = parse("example.txt", output_as_ranges=True)
    print(part2(tape, space_ranges, data_ranges))
    print(part2(*parse("input.txt", output_as_ranges=True)))

from pathlib import Path
from time import perf_counter
from aocd import get_data


def get_test_data():
    input_path = Path(__file__).parent / "input.txt"
    with open(input_path, "r") as f:
        return f.read().splitlines()


def part1(data):
    pos = 50
    counts = 0
    for line in data:
        dir = line[0]
        steps = int(line[1:])

        if dir == "R":
            pos += steps
        elif dir == "L":
            pos -= steps

        pos = pos % 100  # Wrap around at 100

        if pos == 0:
            counts += 1

    return counts


def part2(data):
    pos = 50
    counts = 0
    for line in data:
        dir = line[0]
        steps = int(line[1:])

        old_pos = pos

        if dir == "R":
            new_pos = old_pos + steps
            counts += new_pos // 100
            pos = new_pos % 100

        elif dir == "L":
            new_pos = old_pos - steps
            counts += (old_pos - 1) // 100 - (new_pos - 1) // 100
            pos = new_pos % 100

    return counts


if __name__ == "__main__":
    test_data = get_test_data()
    data = get_data(year=2025, day=1, block=True).splitlines()
    # print(test_data)
    # print(data)

    start = perf_counter()

    # result = part1(test_data)
    # print(part1(data))
    result = part2(test_data)
    # result = part2(data)

    elapsed = perf_counter() - start

    print(f"Result: {result}")
    print(f"Time: {elapsed*1000:.3f}ms")

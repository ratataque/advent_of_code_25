from pathlib import Path
from time import perf_counter
from aocd import get_data


def get_test_data():
    input_path = Path(__file__).parent / "input.txt"
    with open(input_path, "r") as f:
        return f.read().strip()


def part1(data):
    parts = data.split("\n\n")
    ranges_section = parts[0].strip().split("\n")
    ids_section = parts[1].strip().split("\n")

    ranges = []
    for line in ranges_section:
        start, end = map(int, line.split("-"))
        ranges.append((start, end))

    ingredient_ids = [int(line) for line in ids_section]

    fresh_count = 0
    for ingredient_id in ingredient_ids:
        for start, end in ranges:
            if start <= ingredient_id <= end:
                fresh_count += 1
                break

    return fresh_count


def part2(data):
    parts = data.split("\n\n")
    ranges_section = parts[0].strip().split("\n")

    ranges = []
    for line in ranges_section:
        start, end = map(int, line.split("-"))
        ranges.append((start, end))

    ranges.sort()
    merged = []
    for start, end in ranges:
        if merged and start <= merged[-1][1] + 1:
            merged[-1] = (merged[-1][0], max(merged[-1][1], end))
        else:
            merged.append((start, end))

    total = 0
    for start, end in merged:
        total += end - start + 1

    return total


if __name__ == "__main__":
    test_data = get_test_data()
    data = get_data(year=2025, day=5, block=True)
    # print(test_data)
    # print(data)

    start = perf_counter()

    # result = part1(test_data)
    # result = part1(data)
    # result = part2(test_data)
    result = part2(data)

    elapsed = perf_counter() - start

    print(f"\n\nResult: {result}")
    print(f"Time: {elapsed*1000:.3f}ms")

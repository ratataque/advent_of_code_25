from pathlib import Path
from time import perf_counter
from aocd import get_data


def get_test_data():
    input_path = Path(__file__).parent / "input.txt"
    with open(input_path, "r") as f:
        return f.read().splitlines()


def part1(data):
    data = data[0].split(",")

    result = 0
    for range_id in data:
        start, end = range_id.split("-")

        # no invalid numbers in odd length ranges
        if len(start) % 2 != 0 and len(end) % 2 != 0 and len(start) == len(end):
            continue

        # adjust start to even lengths
        if len(start) % 2 != 0:
            start = "1" + "0" * len(start)

        # adjust end to even lengths
        if len(end) % 2 != 0:
            end = "9" * (len(end) - 1)

        # build first and last invalid numbers
        half_start = start[: len(start) // 2]
        half_end = end[: len(end) // 2]
        first_invalid = int(half_start * 2)
        last_invalid = int(half_end * 2)

        # check if invalid numbers are out of range
        if last_invalid < int(start) or first_invalid > int(end):
            continue

        # adjust result for out of range invalid numbers
        if first_invalid < int(start):
            result -= first_invalid
        if last_invalid > int(end):
            result -= last_invalid

        # sum all invalid numbers in range
        for i in range(int(half_start), int(half_end) + 1):
            result += int(str(i) * 2)

    return result


def part2(data):
    data = data[0].split(",")
    invalid_set = set()

    for range_id in data:
        start, end = map(int, range_id.split("-"))

        min_len = len(str(start))
        max_len = len(str(end))

        for total_len in range(min_len, max_len + 1):
            for pattern_len in range(1, total_len):
                if total_len % pattern_len == 0:
                    repetitions = total_len // pattern_len
                    if repetitions >= 2:
                        pattern_start = 10 ** (pattern_len - 1)
                        pattern_end = 10**pattern_len

                        for pattern in range(pattern_start, pattern_end):
                            repeated = int(str(pattern) * repetitions)
                            print(repeated, pattern_start, pattern_end)

                            if start <= repeated <= end:
                                invalid_set.add(repeated)
                                # break

    return sum(invalid_set)


if __name__ == "__main__":
    test_data = get_test_data()
    data = get_data(year=2025, day=2, block=True).splitlines()
    # print(test_data)
    # print(data)

    start = perf_counter()

    # result = part1(test_data)
    # result = part1(data)
    result = part2(test_data)
    # result = part2(data)

    elapsed = perf_counter() - start

    print(f"\n\nResult: {result}")
    print(f"Time: {elapsed*1000:.3f}ms")

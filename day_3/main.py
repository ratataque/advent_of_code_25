from pathlib import Path
from time import perf_counter
from aocd import get_data


def get_test_data():
    input_path = Path(__file__).parent / "input.txt"
    with open(input_path, "r") as f:
        return f.read().splitlines()


def part1(data):
    result = 0

    for bank in data:
        max_num = 0
        second_max = 0
        for i in range(len(bank)):
            num = int(bank[i])
            if num > max_num:
                if i < len(bank) - 1:
                    max_num = num
                    second_max = 0
                else:
                    second_max = num

            elif num > second_max:
                second_max = num

        result += int(str(max_num) + str(second_max))

    return result


def part2(data):
    result = 0

    for bank in data:
        max_num = []
        k = 12
        skip_autorised = len(bank) - k

        start = 0

        # select k digits
        for i in range(k):
            max_digit = "0"
            max_pos = start
            end = skip_autorised + i + 1

            # find max digit in the allowed range (from last highest digit pos to + skipping autorised + 1)
            for j in range(start, end):
                if bank[j] > max_digit:
                    max_digit = bank[j]
                    max_pos = j
                    # print(f"  Checking {bank[j]} (pos {j}) {i}")

            start = max_pos + 1
            max_num.append(max_digit)
            # print(f"{len(''.join(max_num))} Max so far: {''.join(max_num)}")

        result += int("".join(max_num))

    return result


if __name__ == "__main__":
    test_data = get_test_data()
    data = get_data(year=2025, day=3, block=True).splitlines()
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

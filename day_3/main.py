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
        skip_autorised = len(bank) - 12
        print(f"Bank {len(bank)}, Skip autorised: {skip_autorised}")
        skip = []
        streak = []

        for i in range(1, len(bank)):
            num = bank[i]
            prev_num = bank[i - 1]

            if len(skip) + len(streak) >= skip_autorised:
                skip += streak
                break

            if num > prev_num:
                streak.append(i - 1)
                skip += streak
                streak = []
            if num == prev_num:
                streak.append(i - 1)

        # remove indexes in reverse order to not mess up positions
        # print(f"bank {bank}, Skip: {skip}")
        for n in range(len(skip), 0, -1):
            bank = bank[: skip[n - 1]] + bank[skip[n - 1] + 1 :]
        print(len(bank), bank)

        result += int(bank)

    return result


if __name__ == "__main__":
    test_data = get_test_data()
    data = get_data(year=2025, day=3, block=True).splitlines()
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

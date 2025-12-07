from pathlib import Path
from time import perf_counter
from aocd import get_data


def get_test_data():
    input_path = Path(__file__).parent / "input.txt"
    with open(input_path, "r") as f:
        return f.read()


def part1(data):
    data = [line.split() for line in data.split("\n")]

    table = list(zip(*data))

    result = 0
    for col in table:
        total = int(col[0])
        if col[-1] == "*":
            for num in col[1:-1]:
                total *= int(num)
        else:
            for num in col[1:-1]:
                total += int(num)

        result += total

    return result


def part2(data):
    data = data.split("\n")

    if not data[-1]:
        data = data[:-1]

    table = []
    last = 0
    for i in range(len(data[0]) - 1, -1, -1):
        last += 1
        if data[-1][i] in ["+", "*"]:
            table.append([""] * last + [data[-1][i]])
            last = -1

    # print(table)

    skip = 0
    for i in range(len(table)):
        for j in range(len(table[i]) - 1):
            for k in range(len(data)):
                # print(j, skip)
                num = data[k][-1 - (j + skip)]
                if num not in ["+", "*", " "]:
                    table[i][j] += num
                    # break
                    # print(num)
        skip += len(table[i])

    # print(table)

    result = 0
    for col in table:
        total = int(col[0])
        if col[-1] == "*":
            for num in col[1:-1]:
                total *= int(num)
        else:
            for num in col[1:-1]:
                total += int(num)

        result += total

    return result


if __name__ == "__main__":
    test_data = get_test_data()
    data = get_data(year=2025, day=6, block=True)
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

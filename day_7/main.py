from pathlib import Path
from time import perf_counter
from typing import Deque
from aocd import get_data


def get_test_data():
    input_path = Path(__file__).parent / "input.txt"
    with open(input_path, "r") as f:
        return f.read()


def part1(data):
    lines = data.strip().split("\n")
    # for line in lines:
    #     print(line)

    start_pos = 0
    for i in range(len(lines[0])):
        if lines[0][i] == "S":
            start_pos = i
            break

    deque = Deque()
    deque.append((start_pos, 0))
    visited = set()
    visited.add((start_pos, 0))
    split_count = 0

    while deque:
        curr_x, curr_y = deque.popleft()

        next_x, next_y = curr_x, curr_y + 1
        if next_y >= len(lines) or (next_x, next_y) in visited:
            continue

        if lines[next_y][next_x] == "^":
            deque.append((next_x + 1, next_y))
            deque.append((next_x - 1, next_y))
            visited.add((next_x + 1, next_y))
            visited.add((next_x - 1, next_y))
            split_count += 1
        else:
            deque.append((next_x, next_y))
            visited.add((next_x, next_y))

    return split_count


def part2(data):
    data = [list(line) for line in data.strip().split("\n")]
    # for line in data:
    #     print("".join(line))

    dp = []
    for i in range(len(data[0])):
        if data[0][i] == "S":
            dp.append(1)
        else:
            dp.append(0)

    for y in range(len(data)):
        for x in range(len(data[y])):
            if data[y][x] == "^":
                dp[x - 1] += dp[x]
                dp[x + 1] += dp[x]
                dp[x] = 0

    # print(dp)
    return sum(dp)


if __name__ == "__main__":
    test_data = get_test_data()
    data = get_data(year=2025, day=7, block=True)
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

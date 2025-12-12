from pathlib import Path
from time import perf_counter
from aocd import submit, get_data
from fractions import Fraction
from itertools import product


def get_test_data():
    input_path = Path(__file__).parent / "input.txt"
    with open(input_path, "r") as f:
        return f.read()


def part1(data):
    # Parse the input to build a graph
    graph = {}
    for line in data.strip().split("\n"):
        if ":" not in line:
            continue
        device, outputs = line.split(": ")
        graph[device] = outputs.split()

    # For DAG, use memoization without visited tracking
    memo = {}
    
    def count_paths(current, target):
        if current == target:
            return 1
        
        if current in memo:
            return memo[current]
        
        if current not in graph:
            memo[current] = 0
            return 0
        
        total = 0
        for next_device in graph[current]:
            total += count_paths(next_device, target)
        
        memo[current] = total
        return total
    
    return count_paths("you", "out")


def part2(data):
    # Parse the input to build a graph
    graph = {}
    for line in data.strip().split("\n"):
        if ":" not in line:
            continue
        device, outputs = line.split(": ")
        graph[device] = outputs.split()

    # For DAG, use DP with state (node, seen_dac, seen_fft)
    memo = {}
    
    def count_paths_with_req(current, target, seen_dac, seen_fft):
        # Update seen flags for current node
        if current == "dac":
            seen_dac = True
        if current == "fft":
            seen_fft = True

        if current == target:
            return 1 if (seen_dac and seen_fft) else 0

        cache_key = (current, seen_dac, seen_fft)
        if cache_key in memo:
            return memo[cache_key]

        if current not in graph:
            memo[cache_key] = 0
            return 0

        total = 0
        for next_device in graph[current]:
            total += count_paths_with_req(next_device, target, seen_dac, seen_fft)

        memo[cache_key] = total
        return total

    return count_paths_with_req("svr", "out", False, False)


if __name__ == "__main__":
    test_data = get_test_data()
    data = get_data(year=2025, day=11, block=True)

    start = perf_counter()

    # result = part1(test_data)
    # result = part1(data)
    # result = part2(test_data)
    result = part2(data)
    submit(result, year=2025, day=11)

    elapsed = perf_counter() - start

    print(f"\n\nResult: {result}")
    print(f"Time: {elapsed*1000:.3f}ms")

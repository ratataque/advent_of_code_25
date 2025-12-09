from pathlib import Path
import numpy as np
from time import perf_counter
from aocd import submit, get_data
from itertools import combinations
import heapq


def get_test_data():
    input_path = Path(__file__).parent / "input.txt"
    with open(input_path, "r") as f:
        return f.read()


def part1(data, num_edges=10):
    data = [[int(n) for n in line.split(",")] for line in data.strip().split("\n")]

    points = np.array(data)
    n = len(points)

    # track which points are in the MST
    in_mst = np.zeros(n, dtype=bool)
    in_mst[0] = True

    heap = []

    # add all edges from point 0
    for j in range(1, n):
        dist = np.sum((points[0] - points[j]) ** 2)
        heapq.heappush(heap, (dist, 0, j))

    edges = []

    # Prim's algorithm to find the MST
    while len(edges) < num_edges and heap:
        dist, u, v = heapq.heappop(heap)

        if in_mst[v]:
            continue

        # add edge to MST
        edges.append((dist, u, v))
        in_mst[v] = True

        # add all edges from newly added point v
        for j in range(n):
            if not in_mst[j]:
                new_dist = np.sum((points[v] - points[j]) ** 2)
                heapq.heappush(heap, (new_dist, v, j))

    return edges


def part2(data):
    return 0


if __name__ == "__main__":
    test_data = get_test_data()
    data = get_data(year=2025, day=8, block=True)
    # print(test_data)
    # print(data)

    start = perf_counter()

    result = part1(test_data)
    # result = part1(data)
    # result = part2(test_data)
    # result = part2(data)
    # submit(result, year=2025, day=8)

    elapsed = perf_counter() - start

    print(f"\n\nResult: {result}")
    print(f"Time: {elapsed*1000:.3f}ms")

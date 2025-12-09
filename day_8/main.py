from pathlib import Path
from time import perf_counter
from aocd import get_data


def get_test_data():
    input_path = Path(__file__).parent / "input.txt"
    with open(input_path, "r") as f:
        return f.read()


def part1(data, num_connections=1000):
    lines = data.strip().split("\n")
    boxes = []
    for line in lines:
        coords = line.split(",")
        x, y, z = int(coords[0]), int(coords[1]), int(coords[2])
        boxes.append((x, y, z))

    n = len(boxes)

    # Union-Find data structure
    parent = list(range(n))

    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]

    def union(x, y):
        px, py = find(x), find(y)
        if px != py:
            parent[px] = py
            return True
        return False

    # Calculate all pairwise distances
    distances = []
    for i in range(n):
        for j in range(i + 1, n):
            x1, y1, z1 = boxes[i]
            x2, y2, z2 = boxes[j]
            dist = ((x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2) ** 0.5
            distances.append((dist, i, j))

    # Sort by distance
    distances.sort()

    # Connect pairs
    connections = 0
    for dist, i, j in distances:
        if connections >= num_connections:
            break
        union(i, j)
        connections += 1

    # Count circuit sizes
    circuit_sizes = {}
    for i in range(n):
        root = find(i)
        circuit_sizes[root] = circuit_sizes.get(root, 0) + 1

    # Get the three largest circuits
    sizes = sorted(circuit_sizes.values(), reverse=True)
    if len(sizes) >= 3:
        result = sizes[0] * sizes[1] * sizes[2]
    else:
        result = 0

    return result


def part2(data):
    lines = data.strip().split("\n")
    boxes = []
    for line in lines:
        coords = line.split(",")
        x, y, z = int(coords[0]), int(coords[1]), int(coords[2])
        boxes.append((x, y, z))

    n = len(boxes)

    # Union-Find data structure
    parent = list(range(n))

    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]

    def union(x, y):
        px, py = find(x), find(y)
        if px != py:
            parent[px] = py
            return True
        return False

    def count_circuits():
        roots = set()
        for i in range(n):
            roots.add(find(i))
        return len(roots)

    # Calculate all pairwise distances
    distances = []
    for i in range(n):
        for j in range(i + 1, n):
            x1, y1, z1 = boxes[i]
            x2, y2, z2 = boxes[j]
            dist = ((x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2) ** 0.5
            distances.append((dist, i, j))

    # Sort by distance
    distances.sort()

    # Connect pairs until all in one circuit
    last_i, last_j = -1, -1
    for dist, i, j in distances:
        if union(i, j):
            last_i, last_j = i, j
            if count_circuits() == 1:
                break

    # Return product of X coordinates
    x1 = boxes[last_i][0]
    x2 = boxes[last_j][0]
    return x1 * x2


if __name__ == "__main__":
    test_data = get_test_data()
    data = get_data(year=2025, day=8, block=True)
    # print(test_data)
    # print(data)

    start = perf_counter()

    # result = part1(test_data, num_connections=10)
    # result = part1(data, num_connections=1000)
    # result = part2(test_data)
    result = part2(data)

    elapsed = perf_counter() - start

    print(f"\n\nResult: {result}")
    print(f"Time: {elapsed*1000:.3f}ms")

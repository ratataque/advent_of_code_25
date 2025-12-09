from pathlib import Path
from time import perf_counter
from aocd import submit, get_data


def get_test_data():
    input_path = Path(__file__).parent / "input.txt"
    with open(input_path, "r") as f:
        return f.read()


def part1(data):
    lines = data.strip().split("\n")
    points = [tuple(map(int, line.split(","))) for line in lines]

    max_area = 0

    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            p1 = points[i]
            p2 = points[j]

            if len(p1) == 2:
                width = abs(p2[0] - p1[0]) + 1
                height = abs(p2[1] - p1[1]) + 1
                area = width * height
                max_area = max(max_area, area)

    return max_area


def part2(data):
    lines = data.strip().split("\n")
    points = [tuple(map(int, line.split(","))) for line in lines]
    n = len(points)

    # build boundary and segments
    boundary = set()
    v_segments = []

    for i in range(n):
        p1 = points[i]
        p2 = points[(i + 1) % n]

        if p1[0] == p2[0]:
            x = p1[0]
            y1, y2 = min(p1[1], p2[1]), max(p1[1], p2[1])
            v_segments.append((x, y1, y2))
            for y in range(y1, y2 + 1):
                boundary.add((x, y))
        else:
            y = p1[1]
            x1, x2 = min(p1[0], p2[0]), max(p1[0], p2[0])
            for x in range(x1, x2 + 1):
                boundary.add((x, y))

    # point in polygon
    def point_in_polygon(x, y):
        if (x, y) in boundary:
            return True

        crossings = 0
        for seg_x, y1, y2 in v_segments:
            if seg_x > x and y1 < y < y2:
                crossings += 1

        return crossings % 2 == 1

    # check rectangle
    def is_valid_rect(x1, y1, x2, y2):
        w = x2 - x1 + 1
        h = y2 - y1 + 1

        # For smaller rectangles, check all points
        if w * h <= 10000:
            for x in range(x1, x2 + 1):
                for y in range(y1, y2 + 1):
                    if not point_in_polygon(x, y):
                        return False
            return True

        # Check all corners
        for x in [x1, x2]:
            for y in [y1, y2]:
                if not point_in_polygon(x, y):
                    return False

        # check edges
        step = max(1, min(w, h) // 100)

        for x in range(x1, x2 + 1, step):
            if not point_in_polygon(x, y1) or not point_in_polygon(x, y2):
                return False

        for y in range(y1, y2 + 1, step):
            if not point_in_polygon(x1, y) or not point_in_polygon(x2, y):
                return False

        # check interior points
        for i in range(1, 10):
            for j in range(1, 10):
                test_x = x1 + (w * i) // 10
                test_y = y1 + (h * j) // 10
                if not point_in_polygon(test_x, test_y):
                    return False

        return True

    # try all red point pairs
    max_area = 0
    for i in range(n):
        for j in range(i + 1, n):
            p1, p2 = points[i], points[j]
            x1, y1 = min(p1[0], p2[0]), min(p1[1], p2[1])
            x2, y2 = max(p1[0], p2[0]), max(p1[1], p2[1])

            if is_valid_rect(x1, y1, x2, y2):
                area = (x2 - x1 + 1) * (y2 - y1 + 1)
                max_area = max(max_area, area)

    return max_area


if __name__ == "__main__":
    test_data = get_test_data()
    data = get_data(year=2025, day=9, block=True)

    start = perf_counter()

    # result = part1(test_data)
    # result = part1(data)
    result = part2(test_data)
    # result = part2(data)
    # submit(result, year=2025, day=9)

    elapsed = perf_counter() - start

    print(f"\n\nResult: {result}")
    print(f"Time: {elapsed*1000:.3f}ms")

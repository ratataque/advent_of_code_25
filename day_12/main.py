from pathlib import Path
from time import perf_counter
from aocd import submit, get_data


def get_test_data():
    input_path = Path(__file__).parent / "input.txt"
    with open(input_path, "r") as f:
        return f.read()


def parse_input(data):
    lines = data.strip().split('\n')
    shapes = {}
    regions = []
    
    i = 0
    while i < len(lines):
        line = lines[i]
        if ':' in line and line.split(':')[0].strip().isdigit():
            shape_id = int(line.split(':')[0].strip())
            shape_lines = []
            i += 1
            while i < len(lines) and lines[i] and ':' not in lines[i]:
                shape_lines.append(lines[i])
                i += 1
            coords = []
            for r, row in enumerate(shape_lines):
                for c, ch in enumerate(row):
                    if ch == '#':
                        coords.append((r, c))
            shapes[shape_id] = coords
        elif 'x' in line and ':' in line:
            parts = line.split(':')
            dims = parts[0].strip().split('x')
            width, height = int(dims[0]), int(dims[1])
            counts = list(map(int, parts[1].strip().split()))
            regions.append((width, height, counts))
            i += 1
        else:
            i += 1
    
    return shapes, regions


def get_all_orientations(shape):
    orientations = []
    coords = shape[:]
    
    def normalize(coords):
        if not coords:
            return coords
        min_r = min(r for r, c in coords)
        min_c = min(c for r, c in coords)
        return tuple(sorted((r - min_r, c - min_c) for r, c in coords))
    
    orientations.append(normalize(coords))
    
    for _ in range(3):
        coords = [(-c, r) for r, c in coords]
        orientations.append(normalize(coords))
    
    coords = [(r, -c) for r, c in shape]
    orientations.append(normalize(coords))
    for _ in range(3):
        coords = [(-c, r) for r, c in coords]
        orientations.append(normalize(coords))
    
    return list(set(orientations))


def solve_region(width, height, pieces_list, all_orientations, max_attempts=50000):
    if not pieces_list:
        return True
    
    total_area = sum(len(all_orientations[sid][0]) for sid in pieces_list)
    if total_area > width * height:
        return False
    
    grid = [[0] * width for _ in range(height)]
    attempts = [0]
    
    def can_place(shape, row, col):
        for dr, dc in shape:
            r, c = row + dr, col + dc
            if r < 0 or r >= height or c < 0 or c >= width or grid[r][c]:
                return False
        return True
    
    def place(shape, row, col, mark):
        for dr, dc in shape:
            grid[row + dr][col + dc] = mark
    
    def backtrack(piece_idx):
        attempts[0] += 1
        if attempts[0] > max_attempts:
            return False
        
        if piece_idx == len(pieces_list):
            return True
        
        shape_id = pieces_list[piece_idx]
        orientations = all_orientations[shape_id]
        
        for r in range(height):
            for c in range(width):
                for orientation in orientations:
                    if can_place(orientation, r, c):
                        place(orientation, r, c, piece_idx + 1)
                        if backtrack(piece_idx + 1):
                            return True
                        place(orientation, r, c, 0)
        
        return False
    
    return backtrack(0)


def part1(data):
    shapes, regions = parse_input(data)
    
    all_orientations = {}
    for shape_id, coords in shapes.items():
        all_orientations[shape_id] = get_all_orientations(coords)
    
    count = 0
    for i, (width, height, counts) in enumerate(regions):
        pieces_list = []
        for shape_id, qty in enumerate(counts):
            pieces_list.extend([shape_id] * qty)
        
        result = solve_region(width, height, pieces_list, all_orientations)
        if result:
            count += 1
    
    return count


def part2(data):
    return 0


if __name__ == "__main__":
    test_data = get_test_data()
    data = get_data(year=2025, day=12, block=True)

    start = perf_counter()

    # result = part1(test_data)
    result = part1(data)
    # result = part2(test_data)
    # result = part2(data)
    # submit(result, year=2025, day=12)

    elapsed = perf_counter() - start

    print(f"\n\nResult: {result}")
    print(f"Time: {elapsed*1000:.3f}ms")

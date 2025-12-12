from pathlib import Path
from time import perf_counter
from aocd import submit, get_data
from fractions import Fraction
from itertools import product


def get_test_data():
    input_path = Path(__file__).parent / "input.txt"
    with open(input_path, "r") as f:
        return f.read()


def parse_line(line):
    parts = line.strip().split("] ")
    target = parts[0][1:]  # Remove leading '['
    target = [1 if c == "#" else 0 for c in target]

    rest = parts[1]
    buttons_end = rest.rfind("}")
    buttons_part = rest[:buttons_end].split("} ")[0]

    # Parse joltage requirements
    joltage_start = rest.rfind("{")
    joltage_str = rest[joltage_start + 1 : -1]
    joltages = [int(x) for x in joltage_str.split(",")]

    buttons = []
    i = 0
    while i < len(buttons_part):
        if buttons_part[i] == "(":
            j = buttons_part.index(")", i)
            button_str = buttons_part[i + 1 : j]
            button = [int(x) for x in button_str.split(",")]
            buttons.append(button)
            i = j + 1
        else:
            i += 1

    return target, buttons, joltages


def solve_machine(target, buttons):
    n = len(target)
    m = len(buttons)

    # Create augmented matrix [A|b] where A is the button matrix
    # and b is the target vector
    matrix = []
    for i in range(n):
        row = [0] * (m + 1)
        for j, button in enumerate(buttons):
            if i in button:
                row[j] = 1
        row[m] = target[i]
        matrix.append(row)

    # Gaussian elimination over GF(2)
    pivot_col = []
    current_row = 0

    for col in range(m):
        # Find pivot
        pivot_row = None
        for row in range(current_row, n):
            if matrix[row][col] == 1:
                pivot_row = row
                break

        if pivot_row is None:
            continue

        # Swap rows
        matrix[current_row], matrix[pivot_row] = matrix[pivot_row], matrix[current_row]
        pivot_col.append(col)

        # Eliminate
        for row in range(n):
            if row != current_row and matrix[row][col] == 1:
                for c in range(m + 1):
                    matrix[row][c] ^= matrix[current_row][c]

        current_row += 1

    # Check for inconsistency
    for row in range(current_row, n):
        if matrix[row][m] == 1:
            return float("inf")  # No solution

    # Find minimum solution by trying all combinations of free variables
    free_vars = [i for i in range(m) if i not in pivot_col]

    if not free_vars:
        # Unique solution
        solution = [0] * m
        for i, col in enumerate(pivot_col):
            solution[col] = matrix[i][m]
        return sum(solution)

    # Try all combinations of free variables
    min_presses = float("inf")
    for mask in range(1 << len(free_vars)):
        solution = [0] * m
        for i, var in enumerate(free_vars):
            solution[var] = (mask >> i) & 1

        # Back substitute
        for i in range(len(pivot_col) - 1, -1, -1):
            col = pivot_col[i]
            val = matrix[i][m]
            for j in range(col + 1, m):
                val ^= matrix[i][j] * solution[j]
            solution[col] = val

        min_presses = min(min_presses, sum(solution))

    return min_presses


def solve_joltage(joltages, buttons):
    """
    Solve Ax = b where we want to minimize sum(x), x >= 0, x integer
    Use Gaussian elimination to find basis solution
    """
    n = len(joltages)
    m = len(buttons)

    # Build coefficient matrix
    A = [[0] * m for _ in range(n)]
    for j, button in enumerate(buttons):
        for i in button:
            A[i][j] = 1

    # Use fractions for exact arithmetic
    matrix = []
    for i in range(n):
        row = [Fraction(A[i][j]) for j in range(m)] + [Fraction(joltages[i])]
        matrix.append(row)

    # Reduced row echelon form
    pivot_cols = []
    row_idx = 0

    for col in range(m):
        pivot_row = None
        for row in range(row_idx, n):
            if matrix[row][col] != 0:
                pivot_row = row
                break

        if pivot_row is None:
            continue

        matrix[row_idx], matrix[pivot_row] = matrix[pivot_row], matrix[row_idx]
        pivot_cols.append(col)

        pivot_val = matrix[row_idx][col]
        for c in range(m + 1):
            matrix[row_idx][c] /= pivot_val

        for row in range(n):
            if row != row_idx and matrix[row][col] != 0:
                factor = matrix[row][col]
                for c in range(m + 1):
                    matrix[row][c] -= factor * matrix[row_idx][c]

        row_idx += 1

    # Check for no solution
    for row in range(row_idx, n):
        if matrix[row][m] != 0:
            return float("inf")

    free_vars = [i for i in range(m) if i not in pivot_cols]

    if not free_vars:
        solution = [Fraction(0)] * m
        for i, col in enumerate(pivot_cols):
            solution[col] = matrix[i][m]

        if all(s >= 0 and s.denominator == 1 for s in solution):
            return sum(int(s) for s in solution)
        return float("inf")

    # For free variables: exhaustive search with bounds
    def eval_solution(free_vals):
        solution = [Fraction(0)] * m
        for i, var_idx in enumerate(free_vars):
            solution[var_idx] = Fraction(free_vals[i])

        for i in range(len(pivot_cols) - 1, -1, -1):
            col = pivot_cols[i]
            val = matrix[i][m]
            for j in range(col + 1, m):
                val -= matrix[i][j] * solution[j]

            if val < 0 or val.denominator != 1:
                return None
            solution[col] = val

        return sum(int(s) for s in solution)

    # Use branch and bound with iterative deepening
    min_presses = float('inf')
    max_bound = max(joltages) * 2 if joltages else 100
    
    def search(idx, current, current_sum):
        nonlocal min_presses
        
        if current_sum >= min_presses:
            return
        
        if idx == len(free_vars):
            result = eval_solution(current)
            if result is not None:
                min_presses = min(min_presses, result)
            return
        
        for val in range(min(max_bound, min_presses - current_sum)):
            search(idx + 1, current + [val], current_sum + val)
    
    search(0, [], 0)
    return min_presses if min_presses != float('inf') else 0


def part1(data):
    lines = data.strip().split("\n")
    total = 0

    for line in lines:
        target, buttons, _ = parse_line(line)
        presses = solve_machine(target, buttons)
        total += presses

    return total


def part2(data):
    lines = data.strip().split("\n")
    total = 0

    for line in lines:
        _, buttons, joltages = parse_line(line)
        presses = solve_joltage(joltages, buttons)
        total += presses

    return total


if __name__ == "__main__":
    test_data = get_test_data()
    data = get_data(year=2025, day=10, block=True)

    start = perf_counter()

    # result = part1(test_data)
    # result = part1(data)
    # result = part2(test_data)
    result = part2(data)
    # submit(result, year=2025, day=10)

    elapsed = perf_counter() - start

    print(f"\n\nResult: {result}")
    print(f"Time: {elapsed*1000:.3f}ms")

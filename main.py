from solver import solve_sudoku

# ============================================================
# Edit the puzzle below to solve a different Sudoku.
# Use 0 for empty cells.
# ============================================================
PUZZLE = [
    [0, 0, 0, 0, 0, 0, 6, 8, 0],
    [2, 0, 7, 0, 0, 0, 0, 0, 0],
    [8, 6, 0, 1, 0, 0, 0, 0, 4],
    [0, 0, 0, 0, 0, 8, 0, 7, 9],
    [9, 0, 0, 7, 0, 0, 1, 0, 2],
    [6, 0, 0, 0, 0, 1, 5, 0, 0],
    [0, 8, 0, 9, 6, 2, 3, 0, 5],
    [0, 3, 0, 0, 1, 0, 0, 0, 0],
    [5, 0, 0, 0, 3, 0, 0, 0, 0]
]

def print_grid(grid):
    """Nicely formats and prints a 9x9 Sudoku grid."""
    for r in range(9):
        if r > 0 and r % 3 == 0:
            print("-" * 21)
        row_str = []
        for c in range(9):
            if c > 0 and c % 3 == 0:
                row_str.append("|")
            val = grid[r][c]
            row_str.append(str(val) if val != 0 else ".")
        print(" ".join(row_str))

def main():
    print("Initial Sudoku:")
    print_grid(PUZZLE)
    print("=" * 30)

    result = solve_sudoku(PUZZLE)

    print(f"Sudoku Solved: {'Yes' if result['success'] else 'No'}")
    print(f"Time Taken: {result['time_ms']:.2f} ms")
    print(f"Solving Method: {result['mode']}")
    if not result['success']:
        print(f"Error reason: {result['reason']}")
    else:
        print("\nSolved Grid:")
        print_grid(result['grid'])

if __name__ == "__main__":
    main()

from solver import solve_sudoku
from simulated_annealing import count_conflicts

# ============================================================
# Benchmark Puzzles
# ============================================================

EASY = [
    [0, 0, 0, 2, 6, 0, 7, 0, 1],
    [6, 8, 0, 0, 7, 0, 0, 9, 0],
    [1, 9, 0, 0, 0, 4, 5, 0, 0],
    [8, 2, 0, 1, 0, 0, 0, 4, 0],
    [0, 0, 4, 6, 0, 2, 9, 0, 0],
    [0, 5, 0, 0, 0, 3, 0, 2, 8],
    [0, 0, 9, 3, 0, 0, 0, 7, 4],
    [0, 4, 0, 0, 5, 0, 0, 3, 6],
    [7, 0, 3, 0, 1, 8, 0, 0, 0]
]

MEDIUM = [
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

HARD = [
    [0, 0, 0, 6, 0, 0, 4, 0, 0],
    [7, 0, 0, 0, 0, 3, 6, 0, 0],
    [0, 0, 0, 0, 9, 1, 0, 8, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 5, 0, 1, 8, 0, 0, 0, 3],
    [0, 0, 0, 3, 0, 6, 0, 4, 5],
    [0, 4, 0, 2, 0, 0, 0, 6, 0],
    [9, 0, 3, 0, 0, 0, 0, 0, 0],
    [0, 2, 0, 0, 0, 0, 1, 0, 0]
]

EXTREME = [
    [1, 0, 0, 0, 0, 7, 0, 9, 0],
    [0, 3, 0, 0, 2, 0, 0, 0, 8],
    [0, 0, 9, 6, 0, 0, 5, 0, 0],
    [0, 0, 5, 3, 0, 0, 9, 0, 0],
    [0, 1, 0, 0, 8, 0, 0, 0, 2],
    [6, 0, 0, 0, 0, 4, 0, 0, 0],
    [3, 0, 0, 0, 0, 0, 0, 1, 0],
    [0, 4, 0, 0, 0, 0, 0, 0, 7],
    [0, 0, 7, 0, 0, 0, 3, 0, 0]
]

# ============================================================
# Invalid / Unsolvable Puzzles
# ============================================================

INVALID_ROW = [
    [0, 7, 3, 0, 2, 0, 6, 0, 7],  # Duplicate 7 in row 1
    [9, 0, 0, 3, 0, 5, 0, 0, 1],
    [0, 0, 1, 8, 0, 6, 4, 0, 0],
    [0, 0, 8, 1, 0, 2, 9, 0, 0],
    [7, 0, 0, 0, 0, 0, 0, 0, 8],
    [0, 0, 6, 7, 0, 8, 2, 0, 0],
    [0, 0, 2, 6, 0, 9, 5, 0, 0],
    [8, 0, 0, 2, 0, 7, 0, 0, 9],
    [0, 0, 5, 0, 1, 0, 3, 0, 0]
]

INVALID_COL = [
    [0, 0, 3, 0, 2, 0, 6, 0, 0],
    [9, 0, 0, 3, 0, 5, 0, 0, 1],
    [0, 0, 1, 8, 0, 6, 4, 0, 0],
    [0, 0, 8, 1, 0, 2, 9, 0, 0],
    [9, 0, 0, 0, 0, 0, 0, 0, 8],  # Duplicate 9 in column 1
    [0, 0, 6, 7, 0, 8, 2, 0, 0],
    [0, 0, 2, 6, 0, 9, 5, 0, 0],
    [8, 0, 0, 2, 0, 7, 0, 0, 9],
    [0, 0, 5, 0, 1, 0, 3, 0, 0]
]

INVALID_BOX = [
    [3, 0, 0, 0, 2, 0, 6, 0, 0],
    [9, 3, 0, 0, 0, 5, 0, 0, 1],  # Duplicate 3 in box (1,1)
    [0, 0, 1, 8, 0, 6, 4, 0, 0],
    [0, 0, 8, 1, 0, 2, 9, 0, 0],
    [7, 0, 0, 0, 0, 0, 0, 0, 8],
    [0, 0, 6, 7, 0, 8, 2, 0, 0],
    [0, 0, 2, 6, 0, 9, 5, 0, 0],
    [8, 0, 0, 2, 0, 7, 0, 0, 9],
    [0, 0, 5, 0, 1, 0, 3, 0, 0]
]

UNSOLVABLE = [
    [5, 1, 6, 8, 4, 9, 7, 3, 2],
    [3, 0, 7, 6, 0, 5, 0, 0, 0],
    [8, 0, 9, 7, 0, 0, 0, 6, 5],
    [1, 3, 5, 0, 6, 0, 9, 0, 7],
    [4, 7, 2, 5, 9, 1, 0, 0, 6],
    [9, 6, 8, 3, 7, 0, 5, 0, 1],
    [2, 5, 0, 1, 0, 0, 6, 0, 0],
    [0, 0, 0, 9, 0, 0, 0, 5, 3],
    [0, 0, 0, 2, 0, 0, 0, 9, 8]
]

# ============================================================
# Test Helpers
# ============================================================

def verify_solution(initial: list, solved: list) -> bool:
    """Verifies that the solved grid respects the initial clues and has zero conflicts."""
    if count_conflicts(solved) != 0:
        return False
    
    # Check boxes
    for b in range(9):
        box_r = (b // 3) * 3
        box_c = (b % 3) * 3
        box_vals = []
        for r in range(box_r, box_r + 3):
            for c in range(box_c, box_c + 3):
                box_vals.append(solved[r][c])
        if len(set(box_vals)) != 9:
            return False
            
    # Check initial clues
    for r in range(9):
        for c in range(9):
            if initial[r][c] != 0 and initial[r][c] != solved[r][c]:
                return False
                
    return True

def run_test_case(name: str, puzzle: list, expect_success: bool, expected_reason_subset: str = None):
    print("=" * 40)
    print(f"Testing puzzle: {name}")
    print("=" * 40)
    
    result = solve_sudoku(puzzle)
    
    print(f"Sudoku Solved: {'Yes' if result['success'] else 'No'}")
    print(f"Time Taken: {result['time_ms']:.2f} ms")
    print(f"Solving Method: {result['mode']}")
    if not result['success']:
        print(f"Error reason: {result['reason']}")
    
    # Assertions
    assert result['success'] == expect_success, f"Expected success={expect_success}, but got success={result['success']}"
    
    if expect_success:
        assert verify_solution(puzzle, result['grid']), f"Solved grid is invalid for {name}!"
    else:
        assert expected_reason_subset in result['reason'], f"Expected error reason containing '{expected_reason_subset}', but got '{result['reason']}'"
    print("Test: PASSED\n")

# ============================================================
# Test Suite
# ============================================================

def main():
    # Valid Puzzles
    run_test_case("Easy", EASY, True)
    run_test_case("Medium", MEDIUM, True)
    run_test_case("Hard", HARD, True)
    run_test_case("Extreme (AI Escargot)", EXTREME, True)
    
    # Invalid Clues Validation Puzzles
    run_test_case("Invalid Row Duplicate", INVALID_ROW, False, "duplicate 7 in row 1")
    run_test_case("Invalid Col Duplicate", INVALID_COL, False, "duplicate 9 in column 1")
    run_test_case("Invalid Box Duplicate", INVALID_BOX, False, "duplicate 3 in box (1,1)")
    
    # Unsolvable puzzle
    run_test_case("Unsolvable Puzzle", UNSOLVABLE, False, "contradiction encountered")
    
    print("=" * 40)
    print("All automated verification tests PASSED successfully!")
    print("=" * 40)

if __name__ == "__main__":
    main()

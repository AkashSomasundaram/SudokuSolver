from typing import List, Tuple, Set, Dict, Optional

Grid = List[List[int]]

class SudokuBoard:
    """Manages the grid state and active candidates for each cell, including clue validation."""
    def __init__(self, grid: Grid):
        self.grid = [row[:] for row in grid]
        self.candidates = [[set(range(1, 10)) for _ in range(9)] for _ in range(9)]
        
        # Prune candidates using initial grid clues
        for r in range(9):
            for c in range(9):
                val = self.grid[r][c]
                if val != 0:
                    self.candidates[r][c] = set()
                    self._remove_candidate_from_peers(r, c, val)

    def _remove_candidate_from_peers(self, r: int, c: int, val: int):
        # Row peers
        for idx in range(9):
            if idx != c:
                self.candidates[r][idx].discard(val)
        # Column peers
        for idx in range(9):
            if idx != r:
                self.candidates[idx][c].discard(val)
        # Box peers
        box_r, box_c = (r // 3) * 3, (c // 3) * 3
        for i in range(box_r, box_r + 3):
            for j in range(box_c, box_c + 3):
                if i != r or j != c:
                    self.candidates[i][j].discard(val)

    def set_cell(self, r: int, c: int, val: int) -> bool:
        """Sets the grid cell value and updates candidates. Returns True if valid, False if contradiction occurs."""
        self.grid[r][c] = val
        self.candidates[r][c] = set()
        self._remove_candidate_from_peers(r, c, val)
        return self.is_valid()

    def is_valid(self) -> bool:
        """Check if any empty cell has no possible candidates."""
        for r in range(9):
            for c in range(9):
                if self.grid[r][c] == 0 and len(self.candidates[r][c]) == 0:
                    return False
        return True

    def validate_clues(self) -> Tuple[bool, str]:
        """Detect duplicate values in rows, columns, and 3x3 boxes. Returns (is_valid, error_reason)."""
        # 1. Check rows
        for r in range(9):
            seen = {}
            for c in range(9):
                val = self.grid[r][c]
                if val != 0:
                    if val in seen:
                        return False, f"Invalid Sudoku: duplicate {val} in row {r + 1}"
                    seen[val] = c

        # 2. Check columns
        for c in range(9):
            seen = {}
            for r in range(9):
                val = self.grid[r][c]
                if val != 0:
                    if val in seen:
                        return False, f"Invalid Sudoku: duplicate {val} in column {c + 1}"
                    seen[val] = r

        # 3. Check boxes
        for b in range(9):
            box_r = (b // 3) * 3
            box_c = (b % 3) * 3
            seen = {}
            for r in range(box_r, box_r + 3):
                for c in range(box_c, box_c + 3):
                    val = self.grid[r][c]
                    if val != 0:
                        if val in seen:
                            return False, f"Invalid Sudoku: duplicate {val} in box ({box_r // 3 + 1},{box_c // 3 + 1})"
                        seen[val] = (r, c)
        
        return True, ""

    def get_empty_cells(self) -> List[Tuple[int, int]]:
        return [(r, c) for r in range(9) for c in range(9) if self.grid[r][c] == 0]

    def copy(self) -> 'SudokuBoard':
        """Bypasses standard constructor for fast copying in backtracking loops."""
        other = SudokuBoard.__new__(SudokuBoard)
        other.grid = [row[:] for row in self.grid]
        other.candidates = [[set(cands) for cands in row] for row in self.candidates]
        other.size = 9
        other.box_size = 3
        return other


def get_all_houses() -> List[List[Tuple[int, int]]]:
    """Helper to retrieve all rows, columns, and 3x3 box coordinates."""
    houses = []
    # Rows
    for r in range(9):
        houses.append([(r, c) for c in range(9)])
    # Columns
    for c in range(9):
        houses.append([(r, c) for r in range(9)])
    # Boxes
    for b in range(9):
        box_r = (b // 3) * 3
        box_c = (b % 3) * 3
        houses.append([(r, c) for r in range(box_r, box_r + 3) for c in range(box_c, box_c + 3)])
    return houses

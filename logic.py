from typing import Tuple, List
from board import SudokuBoard, get_all_houses

def solve_naked_singles(board: SudokuBoard) -> Tuple[bool, bool]:
    changed = False
    for r in range(9):
        for c in range(9):
            if board.grid[r][c] == 0 and len(board.candidates[r][c]) == 1:
                val = next(iter(board.candidates[r][c]))
                if not board.set_cell(r, c, val):
                    return False, False
                changed = True
    return changed, board.is_valid()

def solve_hidden_singles(board: SudokuBoard) -> Tuple[bool, bool]:
    changed = False
    houses = get_all_houses()
    for house in houses:
        cand_to_cells = {val: [] for val in range(1, 10)}
        for r, c in house:
            if board.grid[r][c] == 0:
                for val in board.candidates[r][c]:
                    cand_to_cells[val].append((r, c))
        for val, cells in cand_to_cells.items():
            if len(cells) == 1:
                r, c = cells[0]
                if not board.set_cell(r, c, val):
                    return False, False
                changed = True
    return changed, board.is_valid()

def solve_naked_pairs(board: SudokuBoard) -> Tuple[bool, bool]:
    changed = False
    houses = get_all_houses()
    for house in houses:
        cells_with_two = []
        for r, c in house:
            if board.grid[r][c] == 0 and len(board.candidates[r][c]) == 2:
                cells_with_two.append((r, c, board.candidates[r][c]))
        
        for i in range(len(cells_with_two)):
            r1, c1, cands1 = cells_with_two[i]
            for j in range(i + 1, len(cells_with_two)):
                r2, c2, cands2 = cells_with_two[j]
                if cands1 == cands2:
                    # Eliminate candidates from all other empty cells in the house
                    for r, c in house:
                        if board.grid[r][c] == 0 and (r, c) != (r1, c1) and (r, c) != (r2, c2):
                            old_len = len(board.candidates[r][c])
                            board.candidates[r][c] = board.candidates[r][c] - cands1
                            if len(board.candidates[r][c]) != old_len:
                                changed = True
                                if len(board.candidates[r][c]) == 0:
                                    return False, False
    return changed, board.is_valid()

def solve_hidden_pairs(board: SudokuBoard) -> Tuple[bool, bool]:
    changed = False
    houses = get_all_houses()
    for house in houses:
        cand_to_cells = {val: [] for val in range(1, 10)}
        for r, c in house:
            if board.grid[r][c] == 0:
                for val in board.candidates[r][c]:
                    cand_to_cells[val].append((r, c))
        
        cands_with_two = {val: cells for val, cells in cand_to_cells.items() if len(cells) == 2}
        cand_list = list(cands_with_two.keys())
        
        for i in range(len(cand_list)):
            d1 = cand_list[i]
            cells1 = cands_with_two[d1]
            for j in range(i + 1, len(cand_list)):
                d2 = cand_list[j]
                cells2 = cands_with_two[d2]
                if set(cells1) == set(cells2):
                    pair_cands = {d1, d2}
                    for r, c in cells1:
                        old_cands = board.candidates[r][c]
                        new_cands = old_cands.intersection(pair_cands)
                        if new_cands != old_cands:
                            board.candidates[r][c] = new_cands
                            changed = True
                            if len(board.candidates[r][c]) == 0:
                                return False, False
    return changed, board.is_valid()

def solve_pointing_pairs(board: SudokuBoard) -> Tuple[bool, bool]:
    changed = False
    for b in range(9):
        box_r = (b // 3) * 3
        box_c = (b % 3) * 3
        box_cells = [(r, c) for r in range(box_r, box_r + 3) for c in range(box_c, box_c + 3)]
        
        for val in range(1, 10):
            cells_with_val = [(r, c) for r, c in box_cells if board.grid[r][c] == 0 and val in board.candidates[r][c]]
            if 2 <= len(cells_with_val) <= 3:
                rows = {r for r, c in cells_with_val}
                cols = {c for r, c in cells_with_val}
                
                if len(rows) == 1:
                    r = next(iter(rows))
                    for c in range(9):
                        if (c < box_c or c >= box_c + 3) and board.grid[r][c] == 0:
                            if val in board.candidates[r][c]:
                                board.candidates[r][c].discard(val)
                                changed = True
                                if len(board.candidates[r][c]) == 0:
                                    return False, False
                if len(cols) == 1:
                    c = next(iter(cols))
                    for r in range(9):
                        if (r < box_r or r >= box_r + 3) and board.grid[r][c] == 0:
                            if val in board.candidates[r][c]:
                                board.candidates[r][c].discard(val)
                                changed = True
                                if len(board.candidates[r][c]) == 0:
                                    return False, False
    return changed, board.is_valid()

def solve_box_line_reduction(board: SudokuBoard) -> Tuple[bool, bool]:
    changed = False
    # Check rows
    for r in range(9):
        for val in range(1, 10):
            cells_with_val = [(r, c) for c in range(9) if board.grid[r][c] == 0 and val in board.candidates[r][c]]
            if 2 <= len(cells_with_val) <= 3:
                boxes = {(cell_r // 3) * 3 + (cell_c // 3) for cell_r, cell_c in cells_with_val}
                if len(boxes) == 1:
                    b = next(iter(boxes))
                    box_r = (b // 3) * 3
                    box_c = (b % 3) * 3
                    for br in range(box_r, box_r + 3):
                        for bc in range(box_c, box_c + 3):
                            if br != r and board.grid[br][bc] == 0:
                                if val in board.candidates[br][bc]:
                                    board.candidates[br][bc].discard(val)
                                    changed = True
                                    if len(board.candidates[br][bc]) == 0:
                                        return False, False

    # Check columns
    for c in range(9):
        for val in range(1, 10):
            cells_with_val = [(r, c) for r in range(9) if board.grid[r][c] == 0 and val in board.candidates[r][c]]
            if 2 <= len(cells_with_val) <= 3:
                boxes = {(cell_r // 3) * 3 + (cell_c // 3) for cell_r, cell_c in cells_with_val}
                if len(boxes) == 1:
                    b = next(iter(boxes))
                    box_r = (b // 3) * 3
                    box_c = (b % 3) * 3
                    for br in range(box_r, box_r + 3):
                        for bc in range(box_c, box_c + 3):
                            if bc != c and board.grid[br][bc] == 0:
                                if val in board.candidates[br][bc]:
                                    board.candidates[br][bc].discard(val)
                                    changed = True
                                    if len(board.candidates[br][bc]) == 0:
                                        return False, False
    return changed, board.is_valid()


class LogicalPropagator:
    """Repeatedly applies logical Sudoku constraint propagation techniques."""
    @staticmethod
    def propagate(board: SudokuBoard) -> Tuple[bool, int]:
        initial_empty = len(board.get_empty_cells())
        while True:
            changed = False
            
            # Step 1: Naked Singles
            ch, valid = solve_naked_singles(board)
            if not valid: return False, 0
            if ch: changed = True
            
            # Step 2: Hidden Singles
            ch, valid = solve_hidden_singles(board)
            if not valid: return False, 0
            if ch: changed = True
            
            # Step 3: Naked Pairs
            ch, valid = solve_naked_pairs(board)
            if not valid: return False, 0
            if ch: changed = True
            
            # Step 4: Hidden Pairs
            ch, valid = solve_hidden_pairs(board)
            if not valid: return False, 0
            if ch: changed = True
            
            # Step 5: Pointing Pairs/Triples
            ch, valid = solve_pointing_pairs(board)
            if not valid: return False, 0
            if ch: changed = True
            
            # Step 6: Box-Line Reduction
            ch, valid = solve_box_line_reduction(board)
            if not valid: return False, 0
            if ch: changed = True
            
            if not changed:
                break
        
        final_empty = len(board.get_empty_cells())
        return True, initial_empty - final_empty

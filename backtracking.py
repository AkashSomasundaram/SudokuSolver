from board import SudokuBoard
from logic import LogicalPropagator

class BacktrackingSolver:
    """Deterministic DFS solver using Minimum Remaining Values (MRV) and constraint propagation per step."""
    def __init__(self, board: SudokuBoard):
        self.board = board

    def solve(self) -> bool:
        empty_cells = self.board.get_empty_cells()
        if not empty_cells:
            return True
            
        # Heuristic: MRV (Select empty cell with fewest remaining candidates)
        r, c = min(empty_cells, key=lambda cell: len(self.board.candidates[cell[0]][cell[1]]))
        
        cands = list(self.board.candidates[r][c])
        if not cands:
            return False
            
        for val in cands:
            # Create a copy of the board to attempt this assignment
            temp_board = self.board.copy()
            if temp_board.set_cell(r, c, val):
                # Run logical constraint propagation immediately after assigning the value
                valid, _ = LogicalPropagator.propagate(temp_board)
                if valid:
                    # Recurse on the logically pruned board
                    solver = BacktrackingSolver(temp_board)
                    if solver.solve():
                        # Propagate successful solution back to the parent board
                        self.board.grid = temp_board.grid
                        self.board.candidates = temp_board.candidates
                        return True
        return False

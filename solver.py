import time
from typing import Dict, Tuple, Optional
from board import SudokuBoard, Grid
from logic import LogicalPropagator
from simulated_annealing import SimulatedAnnealingSolver
from backtracking import BacktrackingSolver

def solve_sudoku(grid: Grid) -> Dict[str, any]:
    """
    Solves Sudoku using logical propagation, Simulated Annealing, and Backtracking fallback.
    Returns a dictionary of structured results:
    {
        "success": bool,
        "grid": Optional[Grid],
        "mode": str,
        "time_ms": float,
        "reason": Optional[str]
    }
    """
    start_time = time.perf_counter()
    
    # 1. Initialize Board
    board = SudokuBoard(grid)
    
    # 2. Pre-solve duplicate validation
    is_valid_clues, error_reason = board.validate_clues()
    if not is_valid_clues:
        duration_ms = (time.perf_counter() - start_time) * 1000.0
        return {
            "success": False,
            "grid": None,
            "mode": "N/A",
            "time_ms": duration_ms,
            "reason": error_reason
        }
        
    # 3. Check for early candidate-set contradictions
    if not board.is_valid():
        duration_ms = (time.perf_counter() - start_time) * 1000.0
        return {
            "success": False,
            "grid": None,
            "mode": "N/A",
            "time_ms": duration_ms,
            "reason": "Unsolvable Sudoku: contradiction encountered during candidate initialization"
        }

    # 4. Run logical constraint propagation
    valid_prop, _ = LogicalPropagator.propagate(board)
    if not valid_prop:
        duration_ms = (time.perf_counter() - start_time) * 1000.0
        return {
            "success": False,
            "grid": None,
            "mode": "N/A",
            "time_ms": duration_ms,
            "reason": "Unsolvable Sudoku: contradiction encountered during logical propagation"
        }
        
    # Check if fully solved by logic
    if len(board.get_empty_cells()) == 0:
        duration_ms = (time.perf_counter() - start_time) * 1000.0
        return {
            "success": True,
            "grid": board.grid,
            "mode": "Logical Propagation Only",
            "time_ms": duration_ms,
            "reason": None
        }

    # Save logic board state in case SA fails
    post_logic_board = board.copy()

    # 5. Run Simulated Annealing
    sa_solver = SimulatedAnnealingSolver(board)
    sa_grid, sa_iters = sa_solver.solve()
    
    if sa_grid is not None:
        duration_ms = (time.perf_counter() - start_time) * 1000.0
        return {
            "success": True,
            "grid": sa_grid,
            "mode": "Simulated Annealing",
            "time_ms": duration_ms,
            "reason": None
        }
        
    # 6. Fallback to Backtracking on the post-logic state
    backtracker = BacktrackingSolver(post_logic_board)
    bt_success = backtracker.solve()
    
    duration_ms = (time.perf_counter() - start_time) * 1000.0
    if bt_success:
        # Decide if method should be Backtracking or SA + Backtracking Fallback
        # If SA was not really attempted because boxes didn't have swaps (sa_iters == 0), it is "Backtracking"
        method = "Backtracking" if sa_iters == 0 else "Simulated Annealing + Backtracking Fallback"
        return {
            "success": True,
            "grid": post_logic_board.grid,
            "mode": method,
            "time_ms": duration_ms,
            "reason": None
        }
    else:
        return {
            "success": False,
            "grid": None,
            "mode": "N/A",
            "time_ms": duration_ms,
            "reason": "Unsolvable Sudoku: contradiction encountered during search"
        }

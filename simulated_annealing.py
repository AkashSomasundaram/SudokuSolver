import random
import math
from typing import List, Tuple, Optional
import os
import subprocess
import matplotlib
# Use Agg backend so saving figure is reliable and non-blocking in all environments
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from board import SudokuBoard, Grid

def count_conflicts(grid: Grid) -> int:
    """Computes total row and column conflicts for a fully filled grid."""
    conflicts = 0
    for idx in range(9):
        # Row conflicts
        row_vals = grid[idx]
        conflicts += 9 - len(set(row_vals))
        
        # Column conflicts
        col_vals = [grid[r][idx] for r in range(9)]
        conflicts += 9 - len(set(col_vals))
    return conflicts


class SimulatedAnnealingSolver:
    """Stochastic search solver using box-locked candidate swapping and conflict trace logging."""
    def __init__(self, board: SudokuBoard, max_iters: int = 100000, t0: float = 1.0, alpha: float = 0.9998, epoch: int = 20, stall_limit: int = 30000):
        self.board = board
        self.max_iters = max_iters
        self.t0 = t0
        self.alpha = alpha
        self.epoch = epoch
        self.stall_limit = stall_limit

    def solve(self, seed: Optional[int] = None) -> Tuple[Optional[Grid], int]:
        if seed is not None:
            random.seed(seed)
            
        initial_grid = [row[:] for row in self.board.grid]
        current_grid = [row[:] for row in self.board.grid]
        mutable_cells_by_box = {b: [] for b in range(9)}
        
        # 1. Identify mutable empty coordinates in each box
        for r in range(9):
            for c in range(9):
                if initial_grid[r][c] == 0:
                    b = (r // 3) * 3 + (c // 3)
                    mutable_cells_by_box[b].append((r, c))
                    
        # 2. Fill mutable cells box-by-box with missing digits
        for b in range(9):
            box_r = (b // 3) * 3
            box_c = (b % 3) * 3
            existing = []
            for r in range(box_r, box_r + 3):
                for c in range(box_c, box_c + 3):
                    if initial_grid[r][c] != 0:
                        existing.append(initial_grid[r][c])
            missing = [n for n in range(1, 10) if n not in existing]
            random.shuffle(missing)
            
            for r, c in mutable_cells_by_box[b]:
                current_grid[r][c] = missing.pop()
                
        current_cost = count_conflicts(current_grid)
        
        # Traces for visualization
        current_trace = [current_cost]
        best_trace = [current_cost]
        
        if current_cost == 0:
            self._plot_traces(current_trace, best_trace)
            return current_grid, 0
            
        best_grid = [row[:] for row in current_grid]
        best_cost = current_cost
        
        temp = self.t0
        stagnant_steps = 0
        total_steps = 0
        
        # 3. Main SA Annealing Loop
        for step in range(1, self.max_iters + 1):
            valid_boxes = [b for b, cells in mutable_cells_by_box.items() if len(cells) >= 2]
            if not valid_boxes:
                break
                
            b = random.choice(valid_boxes)
            (r1, c1), (r2, c2) = random.sample(mutable_cells_by_box[b], 2)
            
            # Try swap
            current_grid[r1][c1], current_grid[r2][c2] = current_grid[r2][c2], current_grid[r1][c1]
            new_cost = count_conflicts(current_grid)
            delta = new_cost - current_cost
            
            # Acceptance test
            if delta < 0 or (temp > 0 and random.random() < math.exp(-delta / temp)):
                current_cost = new_cost
                if current_cost < best_cost:
                    best_cost = current_cost
                    best_grid = [row[:] for row in current_grid]
                    stagnant_steps = 0
                else:
                    stagnant_steps += 1
            else:
                # Revert swap
                current_grid[r1][c1], current_grid[r2][c2] = current_grid[r2][c2], current_grid[r1][c1]
                stagnant_steps += 1
                
            current_trace.append(current_cost)
            best_trace.append(best_cost)
            total_steps = step
            
            if best_cost == 0:
                self._plot_traces(current_trace, best_trace)
                return best_grid, total_steps
                
            if stagnant_steps >= self.stall_limit:
                break
                
            if step % self.epoch == 0:
                temp *= self.alpha
                
        self._plot_traces(current_trace, best_trace)
        return None, total_steps

    def _plot_traces(self, current_trace: List[int], best_trace: List[int]):
        """Generates and saves conflicts graph, opening it with OS preview helper."""
        plt.figure(figsize=(8, 4))
        plt.plot(current_trace, label="Current Conflicts", color="#ff7f0e", alpha=0.6, lw=1)
        plt.plot(best_trace, label="Best Conflicts", color="#1f77b4", lw=2)
        plt.title("Simulated Annealing Conflict History")
        plt.xlabel("Iteration")
        plt.ylabel("Conflicts (Row + Col)")
        plt.grid(True, linestyle="--", alpha=0.7)
        plt.legend(loc="upper right")
        plt.tight_layout()
        
        # Save to disk
        dir_path = os.path.dirname(os.path.abspath(__file__))
        plot_path = os.path.join(dir_path, "sa_conflicts.png")
        plt.savefig(plot_path, dpi=150)
        plt.close()
        
        # Display by opening with macOS preview
        try:
            if os.path.exists(plot_path):
                subprocess.Popen(["open", plot_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except Exception:
            pass

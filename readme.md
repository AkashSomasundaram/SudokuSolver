# Sudoku Solver

A Sudoku solver written in Python that combines logical deduction techniques, Simulated Annealing (SA), and deterministic Backtracking.

The solver first attempts to solve as much of the puzzle as possible using human-style logical techniques. If the puzzle remains incomplete, Simulated Annealing is used as a stochastic search method. If SA fails to reach a valid solution, a Backtracking solver with the Minimum Remaining Values (MRV) heuristic is used as a guaranteed fallback.

---

# Developer

Akash Somasundaram


## Features

### Logical Techniques

The solver repeatedly applies:

- Naked Singles
- Hidden Singles
- Naked Pairs
- Hidden Pairs
- Pointing Pairs / Triples
- Box-Line Reduction

These techniques are applied until no further progress can be made.

### Simulated Annealing

When logic is exhausted:

- Empty cells are filled box-by-box.
- Random swaps are performed within boxes.
- A conflict-based cost function is minimized.
- Conflict history is recorded and plotted.
- If SA reaches zero conflicts, the puzzle is solved.

### Backtracking Fallback

If SA stalls or fails:

- MRV (Minimum Remaining Values) selects the most constrained cell.
- Constraint propagation is applied after every assignment.
- Backtracking guarantees a solution if one exists.

---

# Project Structure

## board.py

Defines the `SudokuBoard` class.

Responsibilities:

- Stores the Sudoku grid.
- Maintains candidate sets.
- Updates candidates after assignments.
- Validates rows, columns, and boxes.
- Detects contradictions.
- Creates board copies for search.

---

## logic.py

Contains all logical solving techniques.

Implemented techniques:

- Naked Singles
- Hidden Singles
- Naked Pairs
- Hidden Pairs
- Pointing Pairs / Triples
- Box-Line Reduction

Also contains:

- `LogicalPropagator`

which repeatedly applies all logical techniques until no further progress is possible.

---

## simulated_annealing.py

Contains:

- Conflict calculation
- Simulated Annealing search
- Conflict-history plotting

Outputs:

- Current conflict count
- Best conflict count
- Conflict history graph (`sa_conflicts.png`)

---

## backtracking.py

Contains:

- MRV-based Backtracking solver

Features:

- Chooses the cell with the fewest candidates
- Applies logical propagation after every guess
- Deterministic guaranteed fallback

---

## solver.py

Main orchestration layer.

Pipeline:

```text
Logical Propagation
        ↓
Simulated Annealing
        ↓
Backtracking Fallback
```

Returns:

- Success / Failure
- Solving method used
- Solve time
- Error reason (if applicable)

---

## main.py

Used for solving your own Sudoku.

Edit the `PUZZLE` variable near the top of the file:

```python
PUZZLE = [
    ...
]
```

Run:

```bash
python3 main.py
```

---

## test_solver.py

Automated test suite.

Tests:

- Easy puzzle
- Medium puzzle
- Hard puzzle
- Extreme puzzle
- Invalid row puzzle
- Invalid column puzzle
- Invalid box puzzle
- Unsolvable puzzle

Verifies:

- Solution correctness
- Preservation of original clues
- Invalid puzzle detection
- Error reporting

Run:

```bash
python3 test_solver.py
```

---

# Usage

## Solve a Sudoku

Open `main.py`.

Replace:

```python
PUZZLE = [...]
```

with your own Sudoku.

Use:

- Numbers 1–9 for clues
- 0 for empty cells

Example:

```python
PUZZLE = [
    [0,0,0,2,6,0,7,0,1],
    [6,8,0,0,7,0,0,9,0],
    [1,9,0,0,0,4,5,0,0],
    ...
]
```

Run:

```bash
python3 main.py
```

---

# Output

Successful solve:

```text
Sudoku Solved: Yes
Time Taken: 34.12 ms
Solving Method: Simulated Annealing + Backtracking Fallback
```

Invalid puzzle:

```text
Sudoku Solved: No
Error reason: Invalid Sudoku: duplicate 7 in row 4
```

Unsolvable puzzle:

```text
Sudoku Solved: No
Error reason: Unsolvable Sudoku: contradiction encountered during search
```

---

# Simulated Annealing Visualization

Whenever Simulated Annealing runs, a conflict-history plot is generated.

The graph shows:

- Current Conflicts
- Best Conflicts

against iteration number.

Output:

```text
sa_conflicts.png
```

This helps visualize convergence and tuning performance.

---

# Extending the Solver

## Add New Logical Techniques

Add the implementation to:

```text
logic.py
```

Then register it inside:

```python
LogicalPropagator.propagate(...)
```

---

## Add New Search Algorithms

Create a new module such as:

```text
genetic_algorithm.py
```

and integrate it into:

```text
solver.py
```

---

## Add More Tests

Place new benchmark puzzles inside:

```text
test_solver.py
```

and add verification cases to the test suite.
---

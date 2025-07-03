import copy

class SudokuSolver:
    def __init__(self, grid):
        """
        Initialize the Sudoku solver with a 9x9 grid.
        :param grid: 2D list representing the initial Sudoku puzzle
        """
        self.grid = copy.deepcopy(grid)
        # 3D list to track candidate values for each cell (1 if possible, 0 otherwise)
        self.candidates = [[[1 for _ in range(9)] for _ in range(9)] for _ in range(9)]

    def solve(self):
        """
        Attempts to solve the Sudoku puzzle using constraint propagation.
        Falls back to recursive backtracking if logical methods stall.
        """
        self.initialize_candidates()
        stuck = False
        progress = True

        while progress:
            progress = self.fill_single_candidates()
            self.update_candidates()

            if self.is_solved():
                print("Solved using logic!")
                return

            if not progress:
                stuck = True

        if stuck:
            print("Logic solver stuck. Switching to backtracking...")
            if not self.backtrack_solver():
                print("No solution found.")
            else:
                print("Solved using backtracking!")

    def initialize_candidates(self):
        """
        Initializes the candidate list based on the current grid state.
        Each candidate list marks which digits (1–9) are still valid per cell.
        """
        for i in range(9):
            for j in range(9):
                val = self.grid[i][j]
                if val != 0:
                    # Only keep the known value; others are ruled out
                    self.candidates[i][j] = [0] * 9
                    self.candidates[i][j][val - 1] = 1

    def update_candidates(self):
        """
        Updates the candidate lists by eliminating values that are already
        placed in the same row, column, or 3×3 subgrid.
        """
        for i in range(9):
            for j in range(9):
                val = self.grid[i][j]
                if val != 0:
                    for k in range(9):
                        if k != j:
                            self.candidates[i][k][val - 1] = 0
                        if k != i:
                            self.candidates[k][j][val - 1] = 0

                    box_x, box_y = 3 * (i // 3), 3 * (j // 3)
                    for x in range(box_x, box_x + 3):
                        for y in range(box_y, box_y + 3):
                            if x != i or y != j:
                                self.candidates[x][y][val - 1] = 0

    def fill_single_candidates(self):
        """
        Identifies cells where only a single candidate is valid, and fills them in.
        :return: True if any progress was made; otherwise, False.
        """
        progress = False
        for i in range(9):
            for j in range(9):
                if self.grid[i][j] == 0:
                    possible = [k + 1 for k, val in enumerate(self.candidates[i][j]) if val == 1]
                    if len(possible) == 1:
                        self.grid[i][j] = possible[0]
                        self.candidates[i][j] = [0] * 9
                        self.candidates[i][j][possible[0] - 1] = 1
                        progress = True
        return progress

    def is_solved(self):
        """
        Checks whether the puzzle is completely filled and valid.
        """
        return all(self.grid[i][j] != 0 for i in range(9) for j in range(9)) and self.is_valid_grid()

    def is_valid_grid(self):
        """
        Validates the current grid by ensuring all rows, columns, and 3×3 boxes
        contain unique digits from 1 to 9.
        """
        def is_valid_unit(unit):
            unit = [num for num in unit if num != 0]
            return len(unit) == len(set(unit))

        for i in range(9):
            if not is_valid_unit(self.grid[i]):
                return False
            if not is_valid_unit([self.grid[j][i] for j in range(9)]):
                return False

        for i in range(3):
            for j in range(3):
                block = []
                for x in range(3):
                    for y in range(3):
                        block.append(self.grid[i * 3 + x][j * 3 + y])
                if not is_valid_unit(block):
                    return False

        return True

    def find_empty(self):
        """
        Locates the next empty cell (denoted by 0).
        :return: (row, col) tuple or None if grid is full.
        """
        for i in range(9):
            for j in range(9):
                if self.grid[i][j] == 0:
                    return (i, j)
        return None

    def is_valid(self, num, pos):
        """
        Checks whether a given number is valid at a specified grid position.
        :param num: Digit to place (1–9)
        :param pos: Tuple (row, col)
        """
        row, col = pos
        for i in range(9):
            if self.grid[row][i] == num and i != col:
                return False
            if self.grid[i][col] == num and i != row:
                return False

        box_x = col // 3
        box_y = row // 3
        for i in range(box_y * 3, box_y * 3 + 3):
            for j in range(box_x * 3, box_x * 3 + 3):
                if self.grid[i][j] == num and (i, j) != pos:
                    return False
        return True

    def backtrack_solver(self):
        """
        Recursive backtracking algorithm used when logic-based deduction is insufficient.
        """
        empty = self.find_empty()
        if not empty:
            return self.is_valid_grid()  # Final safety check
        row, col = empty

        for num in range(1, 10):
            if self.is_valid(num, (row, col)):
                self.grid[row][col] = num
                if self.backtrack_solver():
                    return True
                self.grid[row][col] = 0  # Backtrack

        return False

    def print_grid(self):
        """
        Outputs the current state of the Sudoku grid.
        """
        for row in self.grid:
            print(row)


if __name__ == "__main__":
    test_grid = [[0,0,0,0,0,8,0,7,6],
                 [6,0,0,2,0,0,0,0,0],
                 [0,7,1,0,0,0,8,0,3],
                 [8,0,7,0,6,4,2,3,5],
                 [0,0,0,0,9,2,1,0,0],
                 [1,2,4,0,8,5,0,9,7],
                 [7,0,9,5,0,1,0,0,0],
                 [0,0,0,0,0,7,3,0,0],
                 [0,6,2,8,0,0,0,5,0]]

    print("Original Sudoku:")
    for row in test_grid:
        print(" ".join(str(n) for n in row))

    solver = SudokuSolver(test_grid)
    solver.solve()
    print("\nSolved Sudoku:")
    solver.print_grid()

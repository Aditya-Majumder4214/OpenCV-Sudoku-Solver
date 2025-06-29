class SudokuSolver:
    def __init__(self, grid):
        self.grid = grid
        self.prob_val = [[[0 for _ in range(10)] for _ in range(9)] for _ in range(9)]

        # Initialize prob_val
        for i in range(9):
            for j in range(9):
                self.prob_val[i][j][0] = [grid[i][j], 0, 0, 0]
        for i in range(9):
            for j in range(9):
                if self.prob_val[i][j][0][0] == 0:
                    for k in range(1, 10):
                        self.prob_val[i][j][k] = 1

    def solve(self):
        zero_count = sum(
            1 for i in range(9) for j in range(9) if self.prob_val[i][j][0][0] == 0
        )

        while zero_count > 0:
            zero_count = self.method1(zero_count)
            self.method2(zero_count)
            self.method3(zero_count)
            zero_count = self.method4(zero_count)
            zero_count = self.method5(zero_count)
            zero_count = self.method6(zero_count)

    def method1(self, zero_count):
        for i in range(9):
            for j in range(9):
                if self.prob_val[i][j][0][0] == 0:
                    op_count = 0
                    for k in range(1, 10):
                        if self.prob_val[i][j][k] == 1:
                            op_count += 1
                            temp_var = k
                    if op_count == 1:
                        self.prob_val[i][j][k] = 0
                        self.prob_val[i][j][0][0] = k
                        self.grid[i][j] = k
                        zero_count -= 1
        return zero_count

    def method2(self, zero_count):
        for i in range(9):
            for j in range(9):
                if self.prob_val[i][j][0][0] != 0 and self.prob_val[i][j][0][2] == 0:
                    for x in range(9):
                        self.prob_val[i][x][self.prob_val[i][j][0][0]] = 0
                        self.prob_val[x][j][self.prob_val[i][j][0][0]] = 0
                    self.prob_val[i][j][0][2] = 1

    def method3(self, zero_count):
        for i in range(9):
            for j in range(9):
                if self.prob_val[i][j][0][0] != 0 and self.prob_val[i][j][0][3] == 0:
                    for x in range(3):
                        for y in range(3):
                            self.prob_val[(i//3)*3 + x][(j//3)*3 + y][self.prob_val[i][j][0][0]] = 0
                    self.prob_val[i][j][0][3] = 1

    def method4(self, zero_count):
        for i in range(9):
            opt = self.list_subtractor_row([1,2,3,4,5,6,7,8,9], self.grid[i])
            for z in opt:
                cell_count = 0
                for j in range(9):
                    if self.prob_val[i][j][0][0] == 0 and self.prob_val[i][j][z] == 1:
                        cell_count += 1
                        temp_var = j
                if cell_count == 1:
                    self.prob_val[i][temp_var][0][0] = z
                    self.grid[i][temp_var] = z
                    zero_count -= 1
        return zero_count

    def method5(self, zero_count):
        for j in range(9):
            opt = self.list_subtractor_column([1,2,3,4,5,6,7,8,9], j)
            for z in opt:
                cell_count = 0
                for i in range(9):
                    if self.prob_val[i][j][0][0] == 0 and self.prob_val[i][j][z] == 1:
                        cell_count += 1
                        temp_var = i
                if cell_count == 1:
                    self.prob_val[temp_var][j][0][0] = z
                    self.grid[temp_var][j] = z
                    zero_count -= 1
        return zero_count

    def method6(self, zero_count):
        for i in range(3):
            for j in range(3):
                opt = self.list_subtractor_3x3([1,2,3,4,5,6,7,8,9], i*3, j*3)
                for z in opt:
                    cell_count = 0
                    for x in range(3):
                        for y in range(3):
                            if self.prob_val[i*3 + x][j*3 + y][0][0] == 0 and self.prob_val[i*3 + x][j*3 + y][z] == 1:
                                cell_count += 1
                                temp_var1, temp_var2 = i*3 + x, j*3 + y
                    if cell_count == 1:
                        self.prob_val[temp_var1][temp_var2][0][0] = z
                        self.grid[temp_var1][temp_var2] = z
                        zero_count -= 1
        return zero_count

    def list_subtractor_row(self, list1, list2):
        return [x for x in list1 if x not in list2]

    def list_subtractor_column(self, list1, j):
        col = [self.grid[i][j] for i in range(9)]
        return [x for x in list1 if x not in col]

    def list_subtractor_3x3(self, list1, i, j):
        block = [self.grid[i+x][j+y] for x in range(3) for y in range(3)]
        return [x for x in list1 if x not in block]

    def print_grid(self):
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


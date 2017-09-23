sudo = ['4.....8.5','.3.......','...7.....','.2.....6.','....8.4..','....1....','...6.3.7.','5..2.....','1.4......']
sudo1 = ['...4..87.','.47.92.5.','2..6...3.','97.5..2.3','5.8.247.6','6.4..7.85','.9.3.8..7','..324.16.','.12....9.']

def printGrid(grid):
        for line in grid:
                s = ""
                for c in line:
                        s=s[:]+c
                print(s)
        print('\n')

def strSplit(grid):
        for i,line in enumerate(grid):
                arr = []
                for c in line:
                        arr.append(c)
                grid[i] = arr

def possibleNumb(x0,y0,grid):
        numbers = ['1','2','3','4','5','6','7','8','9']
        row = grid[y0]
        col = [grid[y][x0] for y in range(len(grid))]

        cx,cy = 0,0
        if x0 in range(3,6):
                cx = 3
        elif x0 > 5:
                cx = 6
        if y0 in range(3,6):
                cy = 3
        elif y0 > 6:
                cy = 6
        subBox = []
        for y in range(cy,cy+3):
                for x in range(cx,cx+3):
                        subBox.append(grid[y][x])

        for n in row:
                if n in numbers:
                        numbers.remove(n)
        for n in col:
                if n in numbers:
                        numbers.remove(n)
        for n in subBox:
                if n in numbers:
                        numbers.remove(n)
        return numbers
        

def solveSudoku(grid):
        #printGrid(grid)
        # Find first empty box
        x0,y0 = 0,0
        while grid[y0][x0] != '.':
                x0 += 1
                if x0 not in range(len(grid[y0])):
                        x0=0; y0 += 1
                        if y0 not in range(len(grid)): return True

        # Find all possible numbers
        possible = possibleNumb(x0,y0,grid)

        # For each number, solve sudoku
        for n in possible:
                grid[y0][x0] = n
                if solveSudoku(grid):
                        return True

        # Cant solve
        grid[y0][x0] = '.'
        return False

def solveSudoku1(grid):
        # Fill obvious case
        changed = True
        while changed:
                changed = False
                for y in range(len(grid)):
                        for x in range(len(grid[y])):
                                if grid[y][x] == '.':
                                        n = possibleNumb(x,y,grid)
                                        if len(n) == 1:
                                                print(x,y,n)
                                                grid[y][x] = n[0]
                                                changed = True
        '''
        # Find first empty box
        x0,y0 = 0,0
        while grid[y0][x0] != '.':
                x0 += 1
                if x0 not in range(len(grid[y0])):
                        x0=0; y0 += 1
                        if y0 not in range(len(grid)): return True

        # Find all possible numbers
        possible = possibleNumb(x0,y0,grid)

        # For each number, solve sudoku
        for n in possible:
                grid[y0][x0] = n
                if solveSudoku(grid):
                        return True

        # Cant solve
        grid[y0][x0] = '.'
        return False
        '''

strSplit(sudo)
strSplit(sudo1)
printGrid(sudo1)
solveSudoku1(sudo1)
printGrid(sudo1)
                

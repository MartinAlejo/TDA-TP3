import copy
def print_grid(grid, demmand_rows, demmand_cols):

    print(grid)

    print("Demmand rows: ", demmand_rows)
    print("Demmand cols: ", demmand_cols)
    print("----------------------")
    for row in grid:
        for cell in row:
            if cell == None:
                print('-', end=' ')
            else:
                print(cell, end=' ')
        print("")
    print("----------------------")
    print("")
    print("")
    
def parse_input (path):
    with open(path, 'r') as file:
        lines = file.readlines()
        #Remove lines that start with #, and remove the newline character
        lines = [line for line in lines if not line.startswith('#')]
        lines = [line.rstrip() for line in lines]
        rows, cols , ships = [],[],[]
        aux_counter = 0
        for x in lines:
            if x == '':
                aux_counter += 1
                continue
            if aux_counter == 0:
                rows.append(int(x))
            if aux_counter == 1:
                cols.append(int(x))
            if aux_counter == 2:
                ships.append(int(x))
        return rows, cols, ships
    
#A position is valid if it is not occupied by a ship, and it is not adjacent to a ship.
# positions without ships are marked with None    
def verify_position(grid, row, col):

    if row < 0 or row >= len(grid) or col < 0 or col >= len(grid[0]):
        return False
    
    row_start = max(0, row - 1)
    row_end = min(len(grid), row + 2)
    col_start = max(0, col - 1)
    col_end = min(len(grid[0]), col + 2)
    
    for i in range(row_start, row_end):
        for j in range(col_start, col_end):
            if grid[i][j] is not None:
                return False
                
    return True

def calculate_score(grid):
    total = 0
    for row in grid:
        for cell in row:
            if cell is not None:
                total += 2
    return total

#Return a list of list, showing the placement of the ships
def ship_placement(rows, cols, ships):
    grid = [[None] * len(rows) for _ in range(len(cols))]
    better_solution_grid = [[None] * len(rows) for _ in range(len(cols))]
    total_amount = sum(rows) + sum(cols)
    ship_placemente_aux(copy.deepcopy(rows), copy.deepcopy(cols), ships, copy.deepcopy(grid), 0, better_solution_grid)
    print("Gained ammount: ", calculate_score(better_solution_grid))
    print("Total ammount: ", total_amount)
    print_grid(better_solution_grid, rows, cols)

def ship_placemente_aux(rows, cols, ships, grid, current_ship, better_solution_grid):
    
    
    if current_ship == len(ships):
        if calculate_score(grid) > calculate_score(better_solution_grid):
            for i in range(len(grid)):
                for j in range(len(grid[0])):
                    better_solution_grid[i][j] = grid[i][j]

    if current_ship == len(ships):
        return
    
    for i in range(len (rows)):
        for j in range(len (cols)):
            if (rows[i] > 0 and cols[j] > 0) and verify_position(grid, i, j):
                if (cols[j] >= ships[current_ship]) and (i + ships[current_ship] <= len(rows)):
                    can_place = True
                    for k in range(ships[current_ship]):
                        if not verify_position(grid, i + k, j):
                            can_place = False
                            break
                    if can_place:
                        ship_placemente_aux(copy.deepcopy(rows), copy.deepcopy(cols), ships, copy.deepcopy(grid), current_ship + 1, better_solution_grid)
                        for k in range(ships[current_ship]):
                            grid[i + k][j] = current_ship
                            rows[i + k] -= 1
                            cols[j] -= 1
                        ship_placemente_aux(copy.deepcopy(rows), copy.deepcopy(cols), ships, copy.deepcopy(grid), current_ship + 1, better_solution_grid)
                        return

                if (rows[i] >= ships[current_ship]) and (j + ships[current_ship] <= len(cols)):
                    can_place = True
                    for k in range(ships[current_ship]):
                        if not verify_position(grid, i, j + k):
                            can_place = False
                            break
                    if can_place:
                        ship_placemente_aux(copy.deepcopy(rows), copy.deepcopy(cols), ships, copy.deepcopy(grid), current_ship + 1, better_solution_grid)
                        for k in range(ships[current_ship]):
                            grid[i][j + k] = current_ship
                            cols[j + k] -= 1
                            rows[i] -= 1
                        ship_placemente_aux(copy.deepcopy(rows), copy.deepcopy(cols), ships, copy.deepcopy(grid), current_ship + 1, better_solution_grid)
                        return
    ship_placemente_aux(copy.deepcopy(rows), copy.deepcopy(cols), ships, copy.deepcopy(grid), current_ship + 1, better_solution_grid)


    
def run_example(file):
    rows, cols, ships = parse_input("inputs/" + file)
    ship_placement(rows, cols, ships)

def main():
    run_example('3_3_2.txt')
    run_example('5_5_6.txt')
    run_example('8_7_10.txt')
    run_example('10_3_3.txt')
    

if __name__ == '__main__':
    main()
import copy


def print_grid(grid, demmand_rows, demmand_cols):

    print("Demmand rows: ", demmand_rows)
    print("Demmand cols: ", demmand_cols)
    print("----------------------")
    for row in grid:
        for cell in row:
            if cell == None:
                print(' -', end=' ')
            else:
                if cell < 10:
                    print(' ' + str(cell), end=' ')
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
def verify_position(grid, row, col, rows, cols):

    if rows[row] == 0 or cols[col] == 0:
        return False

    if row < 0 or row >= len(grid) or col < 0 or col >= len(grid[0]):
        return False

    # Check if position is already occupied
    if grid[row][col] != None:
        return False
    # Check if position is adjacent to a ship
    for i in range(-1, 2):
        for j in range(-1, 2):
            if row + i >= 0 and row + i < len(grid) and col + j >= 0 and col + j < len(grid[0]):
                if grid[row + i][col + j] != None:
                    return False
    return True

def calculate_score(grid):
    total = 0
    for row in grid:
        for cell in row:
            if cell is not None:
                total += 2
    return total

def calculate_possible_max_ships(ships, current_ship):
    score = 0
    for i in range(current_ship, len(ships)):
        score += 2 * ships[i]
    return score

#Return a list of list, showing the placement of the ships
def ship_placement(rows, cols, ships):
    grid = [[None] * len(cols) for _ in range(len(rows))]
    better_solution_grid = [[None] * len(cols) for _ in range(len(rows))]
    total_amount = sum(rows) + sum(cols)
    ship_placemente_aux(rows, cols, ships, grid, 0, better_solution_grid)
    print("Gained ammount: ", calculate_score(better_solution_grid))
    print("Total ammount: ", total_amount)
    print_grid(better_solution_grid, rows, cols)

def ship_placemente_aux(rows, cols, ships, grid, current_ship, better_solution_grid):
    score_grid = calculate_score(grid)
    score_best = calculate_score(better_solution_grid)

    if current_ship == len(ships):
        if score_grid > score_best:
            for i in range(len(grid)):
                for j in range(len(grid[0])):
                    better_solution_grid[i][j] = grid[i][j]
        return
    
    if score_best > sum(rows) + sum(cols) + score_grid:
        return

    if score_best > score_grid + calculate_possible_max_ships(ships, current_ship):
        return

    for i in range(len (rows)):
        for j in range(len (cols)):
            if verify_position(grid, i, j, rows, cols):
                ship_size = ships[current_ship]

                #Vertical
                if (cols[j] >= ship_size) and (i + ship_size <= len(rows)):
                    can_place = True
                    for k in range(ship_size):
                        if not verify_position(grid, i + k, j, rows, cols):
                            can_place = False
                            break
                    if can_place:
                        for k in range(ship_size):
                            grid[i + k][j] = current_ship
                            rows[i + k] -= 1
                            cols[j] -= 1
                        ship_placemente_aux(rows.copy(), cols.copy(), ships, copy.deepcopy(grid), current_ship + 1, better_solution_grid)
                        return
                
                #Horizontal
                if (rows[i] >= ship_size) and (j + ship_size <= len(cols)):
                    can_place = True
                    for k in range(ship_size):
                        if not verify_position(grid, i, j + k, rows, cols):
                            can_place = False
                            break
                    if can_place:
                        for k in range(ship_size):
                            grid[i][j + k] = current_ship
                            cols[j + k] -= 1
                            rows[i] -= 1
                        ship_placemente_aux(rows.copy(), cols.copy(), ships, copy.deepcopy(grid), current_ship + 1, better_solution_grid)
                        return
    ship_placemente_aux(rows.copy(), cols.copy(), ships, copy.deepcopy(grid), current_ship + 1, better_solution_grid)


    
def run_example(file):
    rows, cols, ships = parse_input("inputs/" + file)
    ship_placement(rows, cols, ships)

def main():
    run_example('3_3_2.txt')
    run_example('5_5_6.txt')
    run_example('8_7_10.txt')
    run_example('10_3_3.txt')
    run_example('10_10_10.txt')
    run_example('12_12_21.txt')
    run_example('15_10_15.txt')
    run_example('20_20_20.txt')
    run_example('20_25_30.txt')
    run_example('30_25_25.txt')

if __name__ == '__main__':
    main()
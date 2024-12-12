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
    

def verify_position(grid, row, col, rows, cols, demand):

    if row < 0 or row >= len(grid) or col < 0 or col >= len(grid[0]):
        return False

    if rows[row] == 0 or cols[col] == 0:
        return False

    if demand == 0: 
        return

    if grid[row][col] != None:
        return False
    
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

def calculate_possible_max_ships(ships, current_index):
    score = 0
    available_ships = ships[current_index:]

    for ship in available_ships:
        score += ship
    score *= 2

    return score


def ship_placement(rows, cols, ships):
    grid = [[None] * len(cols) for _ in range(len(rows))]
    best_solution_grid = [[None] * len(cols) for _ in range(len(rows))]
    total_amount = sum(rows) + sum(cols)
    ships.sort(reverse=True)

    ship_placement_aux(rows[:], cols[:], ships, grid, best_solution_grid,  0)

    print("Gained ammount: ", calculate_score(best_solution_grid))
    print("Total ammount: ", total_amount)
    print_grid(best_solution_grid, rows, cols)

def place_ship_horizontally(grid, row, col, ship_size, rows, cols):
    for k in range(ship_size):
        grid[row][col + k] = 1
        rows[row] -= 1
        cols[col + k] -= 1

def place_ship_vertically(grid, row, col, ship_size, rows, cols):
    for k in range(ship_size):
        grid[row + k][col] = 1
        rows[row + k] -= 1
        cols[col] -= 1

def unplace_ship_horizontally(grid, row, col, ship_size, rows, cols):
    for k in range(ship_size):
        grid[row][col + k] = None
        rows[row] += 1
        cols[col + k] += 1
        
def unplace_ship_vertically(grid, row, col, ship_size, rows, cols):
    for k in range(ship_size):
        grid[row + k][col] = None
        rows[row + k] += 1
        cols[col] += 1

def available_places(grid):
    empty_places = 0

    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == None:
                empty_places += 1
    
    return empty_places


def ship_placement_aux(rows, cols, ships, grid, best_solution_grid, current_idx_ship):
    score_grid = calculate_score(grid) 
    score_best = calculate_score(best_solution_grid)

    if score_grid > score_best:
        for i in range(len(rows)):
            for j in range(len(cols)):
                best_solution_grid[i][j] = grid[i][j]
    
    if (current_idx_ship >= len(ships)): 
        return

    available_spaces = available_places(grid)

    if score_grid <= score_best:    
        max_possible_score_ships = calculate_possible_max_ships(ships, current_idx_ship)
        max_possible_score = score_grid + min(max_possible_score_ships, available_spaces)
        if max_possible_score <= score_best:
            return  

    maximo = max(max(rows), max(cols))
    while (ships[current_idx_ship] > maximo) and (current_idx_ship < len(ships)):
        current_idx_ship += 1
    
    ship_size = ships[current_idx_ship]
    for i in range(len(rows)):
        if rows[i] == 0: 
            continue
        for j in range(len(cols)):
            if cols[j] == 0: 
                continue
            can_place_horizontal = True
            can_place_vertical = True
            demand = 0
        
            for k in range(ship_size):
                if (k == 0):
                    demand = rows[i]
                if (not verify_position(grid, i, j + k, rows, cols, demand)):
                    can_place_horizontal = False
                    break
                demand -= 1

            for k in range(ship_size):
                if (k == 0):
                    demand = cols[j]
                if (not verify_position(grid, i + k, j, rows, cols, demand)):
                    can_place_vertical = False
                    break
                demand -= 1

            if (can_place_horizontal):
                place_ship_horizontally(grid, i, j, ship_size, rows, cols)
                ship_placement_aux(rows, cols, ships, grid, best_solution_grid, current_idx_ship + 1)
                unplace_ship_horizontally(grid, i, j, ship_size, rows, cols)

            if (can_place_vertical):
                place_ship_vertically(grid, i, j, ship_size, rows, cols)
                ship_placement_aux(rows, cols, ships, grid, best_solution_grid, current_idx_ship + 1)
                unplace_ship_vertically(grid, i, j, ship_size, rows, cols)

    ship_placement_aux(rows, cols, ships, grid, best_solution_grid, current_idx_ship + 1)

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
    run_example('30_25_25.txt') # Tarda mucho

if __name__ == '__main__':
    main()
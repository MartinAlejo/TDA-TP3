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
def verify_position(grid, row, col, rows, cols, demand):

    # Que este adentro de la grilla
    if row < 0 or row >= len(grid) or col < 0 or col >= len(grid[0]):
        return False

    # Haya demanda en la fila y columna
    if rows[row] == 0 or cols[col] == 0:
        return False

    if demand == 0: 
        return

    # Que la posicion no este ocupada
    if grid[row][col] != None:
        return False
    
    # Que no hayan naves adyacentes
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

# Return a list of list, showing the placement of the ships
def ship_placement(rows, cols, ships):
    grid = [[None] * len(cols) for _ in range(len(rows))]
    best_solution_grid = [[None] * len(cols) for _ in range(len(rows))]
    total_amount = sum(rows) + sum(cols)
    ships.sort(reverse=True)

    ship_placement_aux(rows[:], cols[:], ships, grid, best_solution_grid,  0)

    print("Gained ammount: ", calculate_score(best_solution_grid))
    print("Total ammount: ", total_amount)
    print_grid(best_solution_grid, rows, cols)

def place_ship_horizontally(grid, row, col, ship_size, rows, cols, current_idx_ship):
    for k in range(ship_size):
        grid[row][col + k] = current_idx_ship
        rows[row] -= 1
        cols[col + k] -= 1

def place_ship_vertically(grid, row, col, ship_size, rows, cols, current_idx_ship):
    for k in range(ship_size):
        grid[row + k][col] = current_idx_ship
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

# Nueva función para verificar espacios libres
# def has_sufficient_space(grid, ship_size, rows, cols):
#     for i in range(len(rows)):
#         free_count_row = 0
#         free_count_col = 0
#         for j in range(len(cols)):
#             # Verifica fila
#             if grid[i][j] is None:
#                 free_count_row += 1
#             else:
#                 free_count_row = 0
#             if free_count_row >= ship_size:
#                 return True

#             # Verifica columna
#             if grid[j][i] is None:
#                 free_count_col += 1
#             else:
#                 free_count_col = 0
#             if free_count_col >= ship_size:
#                 return True
#     return False

def ship_placement_aux(rows, cols, ships, grid, best_solution_grid, current_idx_ship):
    score_grid = calculate_score(grid) # Puntaje actual
    score_best = calculate_score(best_solution_grid) # Puntaje maximo alcanzado

    # Mejora la solucion, reemplazamos
    if score_grid > score_best:
        for i in range(len(rows)):
            for j in range(len(cols)):
                best_solution_grid[i][j] = grid[i][j]
    
    # Caso base
    if (current_idx_ship >= len(ships)): 
        return

    available_spaces = available_places(grid)

    # Poda 1 (no se puede superar el mejor puntaje)
    if score_grid <= score_best:
        # Verificamos si el puntaje podría mejorar después de colocar más barcos
        max_possible_score_ships = calculate_possible_max_ships(ships, current_idx_ship)
        max_possible_score = score_grid + min(max_possible_score_ships, available_spaces)
        # max_possible_score = score_grid + min(max_possible_score_ships, sum(rows) + sum(cols), available_spaces) 
        if max_possible_score <= score_best:
            # print("Entro a la poda buena")
            return  # No mejorará el puntaje, podar
        
    # Poda 2 (no se puede colocar este barco)
    maximo = max(max(rows), max(cols))
    while (ships[current_idx_ship] > maximo) and (current_idx_ship < len(ships)):
        # print("Entro a la poda")
        current_idx_ship += 1 # Posible bug (VER)
    
    #print("score_best: ", score_best)

    # Intento ubicar el barco actual
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
        
            # Vemos si podemos meter el barco horizontalmente
            for k in range(ship_size):
                if (k == 0):
                    demand = rows[i]
                if (not verify_position(grid, i, j + k, rows, cols, demand)):
                    can_place_horizontal = False
                    break
                demand -= 1

            # Vemos si podemos meter el barco verticalmente
            for k in range(ship_size):
                if (k == 0):
                    demand = cols[j]
                if (not verify_position(grid, i + k, j, rows, cols, demand)):
                    can_place_vertical = False
                    break
                demand -= 1

            # Lo intento colocar de forma horizontal
            if (can_place_horizontal):
                place_ship_horizontally(grid, i, j, ship_size, rows, cols, current_idx_ship)
                ship_placement_aux(rows, cols, ships, grid, best_solution_grid, current_idx_ship + 1)
                unplace_ship_horizontally(grid, i, j, ship_size, rows, cols)

            # Lo intento colocar de forma vertical
            if (can_place_vertical):
                place_ship_vertically(grid, i, j, ship_size, rows, cols, current_idx_ship)
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
    run_example('12_12_21.txt') # Tarda mucho
    run_example('15_10_15.txt')
    run_example('20_20_20.txt')
    run_example('20_25_30.txt') # Tarda mucho
    run_example('30_25_25.txt') # Tarda mucho

if __name__ == '__main__':
    main()
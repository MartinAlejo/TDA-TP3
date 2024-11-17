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

#Returns max score for all available ships
def calculate_possible_max_ships(ships, available_ships):
    score = 0
    for ship in available_ships:
        score += ships[ship]
    score *= 2
    return score

#Return a list of list, showing the placement of the ships
def ship_placement(rows, cols, ships):
    grid = [[None] * len(cols) for _ in range(len(rows))]
    best_solution_grid = [[None] * len(cols) for _ in range(len(rows))]
    total_amount = sum(rows) + sum(cols)
    available_ships = list(range(len(ships)))
    ignore_ships = []
    ship_placemente_aux(rows[:], cols[:], ships, grid, ignore_ships, best_solution_grid, available_ships)
    print("Gained ammount: ", calculate_score(best_solution_grid))
    print("Total ammount: ", total_amount)
    print_grid(best_solution_grid, rows, cols)

def ship_placemente_aux(rows, cols, ships, grid, ignore_ships, best_solution_grid, available_ships):
    score_grid = calculate_score(grid)
    score_best = calculate_score(best_solution_grid)

    # Poda 1: Espacio insuficiente para los barcos restantes (eliminada)

    # Poda 2: Verificación más conservadora de filas y columnas
    # for ship in available_ships:
    #     ship_size = ships[ship]
    #     valid_positions_found = False
    #     for i in range(len(rows)):
    #         for j in range(len(cols)):
    #             if verify_position(grid, i, j, rows, cols):
    #                 # Verificar si podemos colocar el barco en esa posición, vertical u horizontalmente
    #                 if cols[j] >= ship_size and i + ship_size <= len(rows):
    #                     valid_positions_found = True
    #                 if rows[i] >= ship_size and j + ship_size <= len(cols):
    #                     valid_positions_found = True
    #     if not valid_positions_found:
    #         # En lugar de podar completamente, simplemente pasamos al siguiente barco si no encontramos posiciones válidas
    #         continue

    # Poda 3: No mejorar el puntaje
    # Ajustar esta poda para ser menos restrictiva
    if score_grid <= score_best:
        # Verificamos si el puntaje podría mejorar después de colocar más barcos
        max_possible_score = score_grid + calculate_possible_max_ships(ships, available_ships)
        if max_possible_score <= score_best:
            #print("Hay poda")
            return  # No mejorará el puntaje, podar

    # Actualizar la mejor solución si hemos encontrado una mejor
    if score_grid > score_best:
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                best_solution_grid[i][j] = grid[i][j]

    # Caso base
    if len(available_ships) == 0:
        return

    for ship in available_ships:
        if ship in ignore_ships:
            continue
        ship_size = ships[ship]
        for i in range(len(rows)):
            for j in range(len(cols)):
                if verify_position(grid, i, j, rows, cols):
                    # Vertical
                    if cols[j] >= ship_size and i + ship_size <= len(rows):
                        can_place = True
                        for k in range(ship_size):
                            if not verify_position(grid, i + k, j, rows, cols):
                                can_place = False
                                break
                        if can_place:
                            # Colocar barco verticalmente
                            ship_placemente_aux(rows[:], cols[:], ships, copy.deepcopy(grid), ignore_ships + [ship], best_solution_grid, available_ships)
                            for k in range(ship_size):
                                grid[i + k][j] = ship
                                rows[i + k] -= 1
                                cols[j] -= 1
                            new_available_ships = available_ships.copy()
                            new_available_ships.remove(ship)
                            ship_placemente_aux(rows[:], cols[:], ships, copy.deepcopy(grid), [ship], best_solution_grid, new_available_ships)
                            return

                    # Horizontal
                    if rows[i] >= ship_size and j + ship_size <= len(cols):
                        can_place = True
                        for k in range(ship_size):
                            if not verify_position(grid, i, j + k, rows, cols):
                                can_place = False
                                break
                        if can_place:
                            # Colocar barco horizontalmente
                            ship_placemente_aux(rows[:], cols[:], ships, copy.deepcopy(grid), ignore_ships + [ship], best_solution_grid, available_ships)
                            for k in range(ship_size):
                                grid[i][j + k] = ship
                                cols[j + k] -= 1
                                rows[i] -= 1
                            new_available_ships = available_ships.copy()
                            new_available_ships.remove(ship)
                            ship_placemente_aux(rows[:], cols[:], ships, copy.deepcopy(grid), [ship], best_solution_grid, new_available_ships)
                            return

    
def run_example(file):
    rows, cols, ships = parse_input("inputs/" + file)
    ship_placement(rows, cols, ships)

def main():
    run_example('3_3_2.txt')
    run_example('5_5_6.txt')
    run_example('8_7_10.txt')
    run_example('10_3_3.txt')
    run_example('10_10_10.txt')
    # run_example('12_12_21.txt')
    run_example('15_10_15.txt')
    # run_example('20_20_20.txt')
    # run_example('20_25_30.txt')
    # run_example('30_25_25.txt')

if __name__ == '__main__':
    main()

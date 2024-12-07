
# Given a list 
def find_index_of_max(list):

    i = 0
    max = list[0]

    for row, idx in list:
        if row > max:
            max = row
            i = idx
        i += 1

    return i

#-----------------------------------------------------------------------------

#A position is valid if it is not occupied by a ship, and it is not adjacent to a ship.
# positions without ships are marked with None
def verify_position(grid, row, col, rows, cols):

    if row < 0 or row >= len(grid) or col < 0 or col >= len(grid[0]):
        return False

    if rows[row] == 0 or cols[col] == 0:
        return False

    # if row < 0 or row >= len(grid) or col < 0 or col >= len(grid[0]):
    #     return False

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


def try_to_put_ship_horizontally_in_row(ship, grid, idx_f, rows, cols):

    row_to_put_ship = grid[idx_f] # Lista de la fila [3, None, None, None]
    for idx_c in range(len(row_to_put_ship)):

        can_place = True
        for k in range(ship):
            if not verify_position(grid, idx_f, idx_c + k, rows, cols): # SI PUEDO PONER EL BARCO EN ESA CELDA
                can_place = False
                break

        if can_place:
            for k in range(ship):
                grid[idx_f][idx_c + k] = ship
                rows[idx_f] -= 1
                cols[idx_c + k] -= 1

def aproximation(rows, cols, ships):
    grid = [[None] * len(cols) for _ in range(len(rows))]
    ships.sort(reverse=True)

    # Por cada barco
    for ship in ships:
        # Buscar indice de la fila maxima demanda
        # Buscar indice de la columna maxima demanda
        indice_fila_max = rows.index(max(rows))
        indice_columna_max = cols.index(max(cols))

        # Si la demanda de la fila de mayor demanda es mayor o igual que la de la columna de mayor demanda:
        if rows[indice_fila_max] >= cols[indice_columna_max]:
            # Intento colocar el barco en la fila
            for j in range(len(cols)):
                if verify_position(grid, indice_fila_max, j, rows, cols):
                    #Horizontal
                    if (cols[j] >= ship) and (indice_fila_max + ship <= len(rows)):
                        can_place = True
                        for k in range(ship):
                            if not verify_position(grid, indice_fila_max, j + k, rows, cols):
                                can_place = False
                                break
                        if can_place:
                            for k in range(ship):
                                grid[indice_fila_max][j + k] = 1 # Se pone el barco
                                rows[indice_fila_max] -= 1
                                cols[j + k] -= 1
                            break
        else:
              for i in range(len(rows)):
                if verify_position(grid, i, indice_columna_max, rows, cols):
                    #Vertical
                    if (rows[i] >= ship) and (indice_columna_max + ship <= len(cols)):
                        can_place = True
                        for k in range(ship):
                            if not verify_position(grid, i + k, indice_columna_max, rows, cols):
                                can_place = False
                                break
                        if can_place:
                            for k in range(ship):
                                grid[i + k][indice_columna_max] =  1 # Se pone el barco
                                rows[i + k] -= 1
                                cols[indice_columna_max] -= 1
                            break

    return grid

#-----------------------------------------------------------------------------

# Ordenar los barcos de forma descendente (segun longitud)

# Iterar por los barcos:
    # Buscar indice de la fila maxima demanda
    # Buscar indice de la columna maxima demanda

    # Si la demanda de la fila de mayor demanda es mayor o igual que la de la columna de mayor demanda:
        # Si puedo colocar el barco en la fila de maxima demanda:
            # Coloco el barco en la fila
            # Le resto la demanda a la fila y columna

        # Si no puedo poner el barco en la fila:
            # Sigo con el siguiete barco

    # Si la demanda de la columna de mayor demanda es mayor que la de la fila de mayor demanda:
        # Si puedo colocar el barco en la columna de maxima demanda:
            # Coloco el barco en la columna
            # Le resto la demanda a la fila y columna

        # Si no puedo poner el barco en la columna:
            # Sigo con el siguiete barco

#-----------------------------------------------------------------------------

# Ejemplo inicial: grid, barcos y demandas


def calculate_score(grid):
    total = 0
    for row in grid:
        for cell in row:
            if cell is not None:
                total += 2
    return total

   
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


def run_example(file):
    rows, cols, ships = parse_input("inputs/" + file)
    max_possible_score = sum(rows) + sum(cols)
    score = calculate_score(aproximation(rows, cols, ships))
    print("demanda total: ", max_possible_score)
    print("Demanda cumplida: ", score)
    print("Demanda sin cumplir: ", max_possible_score - score)

def main():
    #run_example('3_3_2.txt')
    #run_example('5_5_6.txt')
    #run_example('8_7_10.txt')
    #run_example('10_3_3.txt')
    # run_example('10_10_10.txt')
    # run_example('12_12_21.txt')
    # run_example('15_10_15.txt')
    run_example('20_20_20.txt')
    # run_example('20_25_30.txt')
    # run_example('30_25_25.txt')

main()
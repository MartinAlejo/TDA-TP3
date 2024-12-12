def find_index_of_max(list):

    i = 0
    max = list[0]

    for row, idx in list:
        if row > max:
            max = row
            i = idx
        i += 1

    return i

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

    for ship in ships:
        indice_fila_max = rows.index(max(rows))
        indice_columna_max = cols.index(max(cols))

        if rows[indice_fila_max] >= cols[indice_columna_max]:
          
            for j in range(len(cols)):
                if verify_position(grid, indice_fila_max, j, rows, cols):
                   
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


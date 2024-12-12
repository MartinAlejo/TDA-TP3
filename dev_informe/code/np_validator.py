from main import *

# Devuelve true si no hay barcos adyacentes al barco dad, false en caso contrario
def validate_adjacency(grid, row, col, ship):
    # Veo si la posicion es adyacente a un barco
    for i in range(-1, 2):
        for j in range(-1, 2):
            if row + i >= 0 and row + i < len(grid) and col + j >= 0 and col + j < len(grid[0]):
                adjacent_location = grid[row + i][col + j]
                if adjacent_location != None and adjacent_location != ship:
                    return False
    return True

# Devuelve true si la solucion es valida, false en caso contrario
# La solucion debe ser una matriz con el problema resuelto
def validator(solution, row_demands, col_demands, ships):

    # Primero validamos adyacencias
    for i in range(len(row_demands)):
        for j in range(len(col_demands)):
            if solution[i][j] != None:
                ship = solution[i][j]
                valid = validate_adjacency(solution, i, j, ship)
                if valid == False:
                    return False

    # Validamos que las demandas se cumplan
    for i in range(len(row_demands)):
        for j in range(len(col_demands)):
            if solution[i][j] != None:
                row_demands[i] -= 1
                col_demands[j] -= 1

    for i in range(len(row_demands)):
        if row_demands[i] != 0:
            return False

    for j in range(len (col_demands)):
        if col_demands[j] != 0:
            return False
        
    # Validamos que se hayan colocado todos los barcos
    visited_ships = set()
    for i in range(len(row_demands)):
        for j in range(len(col_demands)):
            if solution[i][j] != None:
                visited_ships.add(solution[i][j])
    
    if len(visited_ships) != len(ships):
        return False

    # Si llego hasta aca, la solucion es valida
    return True
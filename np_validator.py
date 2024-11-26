from main import *

# returns true if there is no adjacents ships for the given ship, false otherwise
def validate_adjacency(grid, row, col, ship):
    # Check if position is adjacent to a ship
    for i in range(-1, 2):
        for j in range(-1, 2):
            if row + i >= 0 and row + i < len(grid) and col + j >= 0 and col + j < len(grid[0]):
                adjacent_location = grid[row + i][col + j]
                if adjacent_location != None and adjacent_location != ship:
                    return False
    return True

# returns true if the solution is a valid, false otherwise.
# solution must be a matrix with the problem already solved
# TODO: De momento solo valido adjacencias. Faltan validar que se cumplan exactamente las demandas de filas y columnas
def validator(solution, row_demands, col_demands, ships):

    # First we validate adjacencies
    for i in range(len(row_demands)):
        for j in range(len (col_demands)):
            if solution[i][j] != None:
                ship = solution[i][j]
                valid = validate_adjacency(solution, i, j, ship)
                if valid == False:
                    return False
    
    return True


# TODO: Borrar
def test():

    solution_5_5_6 = [
        [2, None, None, 3, None],
        [2, None, None, 3, None],
        [None, None, None, None, None],
        [None, None, None, None, 4],
        [None, None, None, None, 4]
    ]

    
    rows, cols, ships = parse_input("inputs/5_5_6.txt")

    print(validator(solution_5_5_6, rows, cols, ships)) # Deberia devolver false al validar que las demandas se cumplan exactamente

test()
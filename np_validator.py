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

    # We validate that the demands are being fulfilled
    for i in range(len(row_demands)):
        for j in range(len (col_demands)):
            if solution[i][j] != None:
                row_demands[i] -= 1
                col_demands[j] -= 1

    for i in range(len(row_demands)):
        if row_demands[i] != 0:
            return False

    for j in range(len (col_demands)):
        if col_demands[j] != 0:
            return False
        
    #TODO: Quiza validar que no se esten metiendo todos los barcos y que el tamanio es correcto (no se si es necesario,
    # pero no se esta haciendo ninguna validacion sobre los barcos)
    
    # If it reaches here, then the solution is valid
    return True


# TODO: Borrar
def test1():
    valid_solution = [
        [0, None, None],
        [0, None, 1],
        [0, None, 1]
    ]

    rows = [1, 2, 2]
    cols = [3, 0, 2]
    ships = [3, 2]

    print(validator(valid_solution, rows, cols, ships)) # Deberia devolver true (no hay adyacencias y las demandas se cumplen)

def test2():
    solution = [
        [0, None, None],
        [0, 1, None],
        [0, 1, None]
    ] # Hay adyacencias

    rows = [1, 2, 2]
    cols = [3, 2, 0]
    ships = [3, 2]

    print(validator(solution, rows, cols, ships)) # Deberia devolver false porque hay adyacencias

def test3():
    solution = [
        [0, None, None],
        [0, None, 1],
        [0, None, 1]
    ]

    rows = [1, 2, 2]
    cols = [2, 0, 2] # No se cumple la demanda de la primer columna
    ships = [3, 2]

    print(validator(solution, rows, cols, ships)) # Deberia devolver false porque no se cumplen las demandas de columna

def test4():
    solution = [
        [0, None, None],
        [0, None, 1],
        [0, None, 1]
    ]

    rows = [1, 2, 3] # No se cumple la demanda de la ultima fila
    cols = [3, 0, 2]
    ships = [3, 2]

    print(validator(solution, rows, cols, ships)) # Deberia devolver false porque no se cumplen las demandas de fila

def test5():
    solution_5_5_6 = [
        [2, None, None, 3, None],
        [2, None, None, 3, None],
        [None, None, None, None, None],
        [None, None, None, None, 4],
        [None, None, None, None, 4]
    ]

    
    rows, cols, ships = parse_input("inputs/5_5_6.txt")

    print(validator(solution_5_5_6, rows, cols, ships)) # Deberia devolver false porque las demandas no se cumplen exactamente



test1()
test2()
test3()
test4()
test5()
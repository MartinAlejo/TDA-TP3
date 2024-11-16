def print_grid(grid):
    print("----------------------")
    for row in grid:
        for cell in row:
            if cell == None:
                print('-', end=' ')
            else:
                print(cell, end=' ')
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
    if grid[row][col] != None:
        return False
    for i in range(-1, 2):
        for j in range(-1, 2):
            if row + i >= 0 and row + i < len(grid) and col + j >= 0 and col + j < len(grid[0]):
                if grid[row + i][col + j] != None:
                    return False
    return True

#Return a list of list, showing the placement of the ships
def ship_placement(rows, cols, ships):
    grid = [[None] * len(rows) for _ in range(len(cols))]
    gained_ammount = 0
    total_amount = sum(rows) + sum(cols)
    gained_ammount = ship_placemente_aux(rows, cols, ships, grid, 0)
    print("Gained ammount: ", gained_ammount)
    print("Total ammount: ", total_amount)
    print_grid(grid)

def ship_placemente_aux(rows, cols, ships, grid, current_ship):
    if current_ship == len(ships):
        return 0
    
    for i in range(len (rows)):
        for j in range(len (cols)):
            if (rows[i] > 0 and cols[j] > 0) and verify_position(grid, i, j):
                if i + ships[current_ship] <= len(rows):
                    can_place = True
                    for k in range(ships[current_ship]):
                        if not verify_position(grid, i + k, j):
                            can_place = False
                            break
                    if can_place:
                        for k in range(ships[current_ship]):
                            grid[i + k][j] = current_ship
                            rows[i + k] -= 1
                        return 2*(ships[current_ship]) + ship_placemente_aux(rows, cols, ships, grid, current_ship + 1)
                if j + ships[current_ship] <= len(cols):
                    can_place = True
                    for k in range(ships[current_ship]):
                        if not verify_position(grid, i, j + k):
                            can_place = False
                            break
                    if can_place:
                        for k in range(ships[current_ship]):
                            grid[i][j + k] = current_ship
                            cols[j + k] -= 1
                        return 2*(ships[current_ship]) + ship_placemente_aux(rows, cols, ships, grid, current_ship + 1)
                    


    return ship_placemente_aux(rows, cols, ships, grid, current_ship + 1)


    
def main():
    rows, cols, ships = parse_input('input.txt')
    ship_placement(rows, cols, ships)
    
    

if __name__ == '__main__':
    main()
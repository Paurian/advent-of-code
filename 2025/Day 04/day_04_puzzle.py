import sys

# Read the input from a file or return an empty list
def read_input(filename=None):
    if filename:
        with open(filename, 'r') as file:
            return file.read().strip().splitlines()
    else:
        return []

# Convert lines of roles into a grid (2D list)
def convert_lines_to_grid(lines):
    return [list(s) for s in lines]

# Print the rlle grid
def print_grid(roll_grid):
    for r in range(len(roll_grid)):
        for c in range(len(roll_grid[r])):
            print(roll_grid[r][c], end=' ')
        print()

# Scan the grid for roles that have fewer than 4 surrounding roles
def scan_grid_for_roles(roll_grid):
    rows = len(roll_grid)
    cols = len(roll_grid[0])
    movable_rolls = 0
    surrounding = [(-1, -1), (-1, 0), (-1, 1),  (0, -1), (0, 1), (1, -1),  (1, 0), (1, 1)]
    for r in range(rows):
        for c in range(cols):
            current_roll = roll_grid[r][c]
            surrounding_rolls = 0
            if current_roll == '@':
                for y, x in surrounding:
                    nr, nc = r + y, c + x
                    if 0 <= nr < rows and 0 <= nc < cols and roll_grid[nr][nc] != '.':
                        surrounding_rolls += 1
            
                if surrounding_rolls < 4:
                    roll_grid[r][c] = 'X'
                    movable_rolls += 1
    return movable_rolls

def clear_roll_grid(roll_grid):
    rows = len(roll_grid)
    cols = len(roll_grid[0])
    for r in range(rows):
        for c in range(cols):
            if roll_grid[r][c] == 'X':
                roll_grid[r][c] = '.'

def depleate_roll_grid(roll_grid):
    clear_roll_grid(roll_grid)
    total_removed_rolls = 0
    removed_rolls = scan_grid_for_roles(roll_grid)
    while removed_rolls > 0:
        clear_roll_grid(roll_grid)
        total_removed_rolls += removed_rolls
        removed_rolls = scan_grid_for_roles(roll_grid)

    return total_removed_rolls + removed_rolls
    

# Main execution
if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else None
    roll_lines = read_input(input_file)
    roll_grid = convert_lines_to_grid(roll_lines)
    print("Roll Grid:")
    print_grid(roll_grid)

    movable_rolls = scan_grid_for_roles(roll_grid)
    print("\nUpdated Roll Grid:")
    print_grid(roll_grid)
    print(f"\nNumber of movable rolls: {movable_rolls}")

    total_removed_rolls = depleate_roll_grid(roll_grid) + movable_rolls
    print("\nFinal Roll Grid after depletion:")
    print_grid(roll_grid)
    print(f"\nTotal number of removed rolls: {total_removed_rolls}")
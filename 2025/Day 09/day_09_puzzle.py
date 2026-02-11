import sys
from typing import List, Dict, Tuple
from pprint import pprint
import time

# Read the input from a file or return an empty list
def read_input(filename: str = None) -> List[Tuple[int,int]]:
    """
    Reads the input file and returns the tachyon tree as a list of strings.
    
    :param filename: Description
    :return: List of a list of characters representing the tachyon tree.
    """
    # junction_boxes = [] # Actually a matrix
    with open(filename, 'r', encoding='utf-8') as file:
        data = [tuple(map(int, line.split(','))) for line in file]
    return data


def area_between_points(point1, point2):
    """
    Calculates the Euclidean distance between two junction boxes.
    
    :param box1: Tuple representing the coordinates of the first box (x1, y1, z1).
    :param box2: Tuple representing the coordinates of the second box (x2, y2, z2).
    :return: Euclidean distance between the two boxes.
    """
    return abs(point1[0] - point2[0] + 1) * abs(point1[1] - point2[1] + 1)


def matrixinator(tiles: List[Tuple[int,int]]) -> List[List[int]]:
    _t0 = time.time()
    print("Preparing Matrix")
    columns, rows = zip(*tiles)
    max_cols, max_rows = (max(columns) + 3, max(rows) + 2)
    matrix = [[0] * max_cols] * max_rows
    # matrix = [[0] * max_cols for r in range(max_rows)]
    # Treat the tiles as drawing points.
    looped_tiles = tiles + [tiles[0]]
    last_point = looped_tiles[0]
    _t1 = time.time()
    _t_total = t1-t0
    print(f"{_t_total:.3f} seconds to initialize matrix")
    _t0 = time.time()

    print("Drawing in Matrix")
    for t in range(1, len(looped_tiles)):
        c, r = looped_tiles[t]
        lc, lr = last_point
        direction = -1 if r < lr or c < lc else 1
        if c == lc:
            for r in range(lr, r + direction, direction):
                matrix[r][c] = 1
        else:
            for c in range(lc, c + direction, direction):
                matrix[r][c] = 1
        last_point = looped_tiles[t]

    _t1 = time.time()
    _t_total = t1-t0
    print(f"{_t_total:.3f} seconds to draw matrix")
    _t0 = time.time()

    # Now to fill in the shape.
    # The end of a straight line could indicate an inner-point, or could be the end of the shape.
    # The dirty way to determine this is to see if the line is at the top or bottom of the drawing.
    # Though this logic is flawed on drawings that twist and intertwine, it should work for this exercise.
    print("Filling in Matrix")
    first_row, last_row = (min(rows), max(rows))
    for r in range(max_rows):
        t = 0
        z = 1 if r in (first_row, last_row) else 0
        for c in range(1, max_cols - 1):
            m, n = (matrix[r][c], matrix[r][c+1])
            t = (t^m)&(t|~n)&(~z)
            matrix[r][c] = t|m

    _t1 = time.time()
    _t_total = t1-t0
    print(f"{_t_total:.3f} seconds to fill {len(matrix)} row x {len(matrix[0])} column matrix")
    _t0 = time.time()

    return matrix


def area_of_shaded_rectangle_between_points(point1, point2, matrix):
    # Only need to look at each corner of each rectangle. If any corner is not shaded, throw it out.
    result = 0 if (matrix[point1[1]][point2[0]] & matrix[point2[1]][point1[0]]) == 0 else abs(point1[0] - point2[0] + 1) * abs(point1[1] - point2[1] + 1)
    # Of those that pass (if we want to be rigorous and correct) go down and across the sides. If any point is not shaded, throw it out.
    if result > 0:
        lc, rc = (min(point1[0],point2[0]), max(point1[0],point2[0]))
        tr, br = (min(point1[1],point2[1]), max(point1[1],point2[1]))
        for c in range(lc, rc + 1):
            result = result * matrix[tr][c] * matrix[br][c]
        for r in range(tr, br + 1):
            result = result * matrix[r][lc] * matrix[r][rc]
    return result


def get_largest_shaded_area_from_tile_points(matrix: List[List[int]], tiles: List[Tuple[int,int]]) -> int:
    def area_cycle(tiles, matrix):
        return [area_of_shaded_rectangle_between_points(tiles[a], tiles[b], matrix) for a in range(len(tiles)) for b in range(a + 1, len(tiles))]
    return max(area_cycle(tiles, matrix))


def get_largest_shaded_rectangle_area(tiles: List[Tuple[int,int]]) -> int:
    # 1. Calculate the area of all rectangles between two points.
    # 2. In order of largest to smallest, check to see if any other point from the tiles lies within
    #    If we do not, we have a winner. If we do, repeat the check with the next largest area.
    result = []
    tsr = sorted(tiles, key=lambda x: x[0]) # tiles sorted by row
    for a in range(len(tsr)):
        for b in range(a + 1, len(tsr)):
            # If we don't have any tiles between a and b that exist within the points of a and b then we can get the area
            has_intersection = False
            for x in range(a + 1, b):
                if tsr[x][0] not in (tsr[a][0], tsr[b][0]):
                    # tsr[x] is between rows where a and b reside.
                    has_intersection = tsr[x][1] > min(tsr[a][1], tsr[b][1]) and tsr[x][1] < max(tsr[a][1], tsr[b][1])
            if not has_intersection:
                result.append(area_between_points(tsr[a],tsr[b]))
    return max(result)


# area_cycle should really be a function of its own or expanded as a nested loop, but this is concise and only internal to this function.
def get_largest_area(tiles: List[Tuple[int,int]]) -> int:
    def area_cycle(tiles) -> List[int]:
        return [area_between_points(tiles[a], tiles[b]) for a in range(len(tiles)) for b in range(a + 1, len(tiles))]
    return max(area_cycle(tiles))


# Main execution
if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else "c:/Users/BGipson5/Repos/advent-of-code/2025/Day 09/day_09_test.txt"
    if input_file:
        t0 = time.time()
        print(f"Reading input from: {input_file}.")
        tiles = read_input(input_file)
        t1 = time.time()
        t_total = t1-t0
        t0 = time.time()
        print(f"{t_total:.3f} seconds to read file")

        print("Calculating point-to-point areas...")
        largest_area = get_largest_area(tiles)
        print(f"Largest Area is {largest_area}")
        t1 = time.time()
        t_total = t1-t0
        t0 = time.time()
        print(f"{t_total:.3f} seconds to calculate point-to-point areas (not shade-restricted)")

        print("Drawing and filling the matrix.")
        floor = matrixinator(tiles)
        # pprint(floor)
        t1 = time.time()
        t_total = t1-t0
        t0 = time.time()
        print(f"{t_total:.3f} seconds to generate, draw and fill the matrix")

        print("Calculating largest fully shaded area...")
        largest_shaded_area = get_largest_shaded_rectangle_area(tiles)
        print(f"Largest Shaded Area is {largest_shaded_area}")
        t1 = time.time()
        t_total = t1-t0
        t0 = time.time()
        print(f"{t_total:.3f} seconds to calculate point-to-point areas (shade-restricted)")

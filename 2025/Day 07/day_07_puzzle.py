"""Module for reading and processing the tachyon tree input."""

import sys

# Read the input from a file or return an empty list
def read_input(filename=None):
    """
    Reads the input file and returns the tachyon tree as a list of strings.
    
    :param filename: Description
    :return: List of a list of characters representing the tachyon tree.
    """
    _tachyon_tree = [] # Actually a matrix
    if filename:
        with open(filename, 'r', encoding='utf-8') as file:
            for s in file.read().strip().splitlines():
                _tachyon_tree.append(list(s))
    return _tachyon_tree


def apply_tachyon_beam(this_tachyon_tree):
    """
    Applies the tachyon beam effect to the tachyon tree.
    
    :param tachyon_tree: List of strings representing the tachyon tree.
    :return: Modified tachyon tree after applying the beam effect.
    """
    this_split_count = 0
    tachyon_weight_matrix = [[0 for _ in range(len(this_tachyon_tree[0]))] for _ in range(len(this_tachyon_tree))]
    for i in range(1, len(this_tachyon_tree)):
        for x in range(len(this_tachyon_tree[i])):
            if this_tachyon_tree[i-1][x] == 'S':
                    this_tachyon_tree[i][x] = '|'
                    tachyon_weight_matrix[i][x] = 1
            elif this_tachyon_tree[i-1][x] == '|':
                if this_tachyon_tree[i][x] == '^':
                    this_split_count += 1
                    this_tachyon_tree[i][x-1] = '|'
                    this_tachyon_tree[i][x+1] = '|'
                    tachyon_weight_matrix[i][x-1] = tachyon_weight_matrix[i][x-1] + tachyon_weight_matrix[i-1][x]
                    tachyon_weight_matrix[i][x+1] = tachyon_weight_matrix[i][x+1] + tachyon_weight_matrix[i-1][x]
                else:
                    this_tachyon_tree[i][x] = '|'
                    tachyon_weight_matrix[i][x] = tachyon_weight_matrix[i][x] + tachyon_weight_matrix[i-1][x]

    final_weight_sum = 0
    for x in range(len(this_tachyon_tree[-1])):
        final_weight_sum += tachyon_weight_matrix[-1][x]
    
    for m in tachyon_weight_matrix:
        print(m)
    return this_split_count, final_weight_sum


def print_tachyon_tree(this_tachyon_tree):
    """
    Prints the tachyon tree in a formatted manner.
    
    :param tachyon_tree: List of strings representing the tachyon tree.
    """
    for line in this_tachyon_tree:
        print(''.join(line))


# Main execution
if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else "C:/Users/bri/Repos/advent-of-code/2025/Day 07/day_07_test.txt"
    print(f"Reading input from: {input_file}")
    tachyon_tree = read_input(input_file)
    split_count, weight_sum = apply_tachyon_beam(tachyon_tree)
    print_tachyon_tree(tachyon_tree)
    print(f"Tachyon beam splits {split_count} times with a quantum weight sum of {weight_sum}.")

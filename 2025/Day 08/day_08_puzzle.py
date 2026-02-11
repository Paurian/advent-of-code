"""Module for reading and processing the playground junction box input."""

import sys
from typing import List, Dict, Tuple

# Read the input from a file or return an empty list
def read_input(filename=None):
    """
    Reads the input file and returns the tachyon tree as a list of strings.
    
    :param filename: Description
    :return: List of a list of characters representing the tachyon tree.
    """
    # junction_boxes = [] # Actually a matrix
    with open(filename, 'r', encoding='utf-8') as file:
        data = [tuple(map(int, line.split(','))) for line in file]
    return data

def distance_between_boxes(box1, box2):
    """
    Calculates the Euclidean distance between two junction boxes.
    
    :param box1: Tuple representing the coordinates of the first box (x1, y1, z1).
    :param box2: Tuple representing the coordinates of the second box (x2, y2, z2).
    :return: Euclidean distance between the two boxes.
    """
    return ((box2[0] - box1[0])**2 + (box2[1] - box1[1])**2 + (box2[2] - box1[2])**2)**0.5


def calculate_all_junction_box_distances(junction_boxes):
    distances = {}
    for i, box1 in enumerate(junction_boxes):
        for j in range(i + 1, len(junction_boxes)):
            dist = distance_between_boxes(box1, junction_boxes[j])
            distances[(box1, junction_boxes[j])] = dist

    return distances


def calculate_junction_box_distances(junction_boxes, number_of_distances_to_consider):
    """
    Calculates distances between all pairs of junction boxes.
    
    :param junction_boxes: List of tuples representing the coordinates of junction boxes.
    :param number_of_distances_to_consider: the number of shortest distances to consider
    :return: List of distances between each pair of junction boxes.
    """
    distances = {}

    for i, box1 in enumerate(junction_boxes):
        for j in range(i + 1, len(junction_boxes)):
            dist = distance_between_boxes(box1, junction_boxes[j])
            if len(distances) == 0 or dist < max(distances.values()):
                # If we have enough shortest distances, remove the longest one
                if len(distances) >= number_of_distances_to_consider:
                    # Remove the corresponding entry from distances
                    longest_distance_key = max(distances, key=lambda k: distances[k])
                    distances.pop(longest_distance_key)
                # Add the new shortest distance
                distances[(box1, junction_boxes[j])] = dist

    return distances


def reduce_boxes(junction_box_distances: Dict[Tuple[Tuple[int, int, int], Tuple[int, int, int]], float]):
    """
    Reduces the number of boxes from closest to furthest such that each box only appears once.

    param: junction_box_distances (Dict[Tuple[Tuple[int, int, int], Tuple[int, int, int]], float]): Dictionary of Box1-Box2 combinations
    """
    registered_boxes = []
    sorted_distances = sorted(junction_box_distances.items(), key=lambda item: item[1])
    for (box1, box2), _ in sorted_distances:
        already_registered = True
        if box1 not in registered_boxes:
            registered_boxes.append(box1)
            already_registered = False
        if box2 not in registered_boxes:
            registered_boxes.append(box2)
            already_registered = False
        if already_registered:
            # Remove the pair from the junction set
            junction_box_distances.pop((box1, box2))


def join_junction_boxes(junction_box_distances, total_number_of_boxes):
    """
    Joins junction boxes based on the shortest distances.
    
    :param junction_box_distances: Dictionary of distances between junction boxes.
    :return: List of joined junction boxes.
    """
    chained_box_sets = []
    sorted_distances = sorted(junction_box_distances.items(), key=lambda item: item[1])
    x_distance = 0
    for (box1, box2), _ in sorted_distances:
        if x_distance > 0:
            break
        chain_found = None
        for box_set in chained_box_sets:
            if box1 in box_set or box2 in box_set:
                box_set.update([box1, box2])
                if chain_found:
                    # merge sets
                    chain_found.update(box_set)
                    chained_box_sets.remove(box_set)
                else:
                    chain_found = box_set
                if len(box_set) == total_number_of_boxes and x_distance == 0:
                    x_distance = box1[0] * box2[0]
                    print(f"FOUND: {box1} / {box2}\n--> {x_distance}\n")
                    break
                
        if not chain_found:
            chained_box_sets.append(set([box1, box2]))

    return chained_box_sets, x_distance


def calculate_top_three_circuits(chained_box_sets):
    """
    Calculates the top three circuits based on the number of junction boxes.
    
    :param chained_box_sets: List of sets representing joined junction boxes.
    :return: Product of the sizes of the top three largest circuits.
    """
    sorted_box_sets = sorted(chained_box_sets, key=lambda s: len(s), reverse=True)
    r = min(3, len(sorted_box_sets))
    top_three_sizes = [len(sorted_box_sets[i]) for i in range(r)]
    product = 1
    for size in top_three_sizes:
        product *= size
    return product


# Main execution
if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else "c:/Users/BGipson5/Repos/advent-of-code/2025/Day 08/day_08_test.txt"
    maximum_set_size = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    if input_file:
        print(f"Reading input from: {input_file} for {maximum_set_size} shortest distances.")
        junction_boxes = read_input(input_file)
        print("Calculating Junction Box Distances...")
        junction_box_distances = calculate_junction_box_distances(junction_boxes, maximum_set_size)
        print("Joining Junction Boxes...")
        chained_box_sets, _x = join_junction_boxes(junction_box_distances, len(junction_boxes))
        print("Calculating Top 3 Circuits...")
        top_three_circuits = calculate_top_three_circuits(chained_box_sets)
        print(f"--> {top_three_circuits}")
        
        print("\nCalculating ALL Junction Box Distances...")
        all_junction_box_distances = calculate_all_junction_box_distances(junction_boxes)
        print("Joining ALL Junction Boxes...")
        chained_box_sets, _x = join_junction_boxes(all_junction_box_distances, len(junction_boxes))

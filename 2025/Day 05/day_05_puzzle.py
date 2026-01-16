import sys
from functools import reduce

# Read the input from a file or return an empty list
def read_input(filename=None):
    range_strings = []
    check_strings = []
    end_of_range = False
    if filename:
        with open(filename, 'r') as file:
            lines = file.read().strip().splitlines()
        for line in lines:
            if end_of_range:
                check_strings.append(line)
            elif line == "":
                end_of_range = True
            else:
                range_strings.append(line)
    return range_strings, check_strings

# Not necessary, but could speed things up ... reduce ranges first and keep them sorted.
def reduce_fresh_ingredient_ranges(range_strings):
    # Nested Lambda maps to convert range strings to a sorted list of integer tuples
    sorted_ranges = sorted(list(map(lambda r: list(map(lambda i: int(i), r.split('-'))), range_strings)), key=lambda x: x[0])
    reduced_ranges = []

    # Merge overlapping or contiguous ranges. Assumes sorted ranges.
    for r in sorted_ranges:
        # If the latest range (r) start is greater than the end of the last reduced range, append it to our list.
        if not reduced_ranges or reduced_ranges[-1][1] < r[0] - 0:  # No overlap
            reduced_ranges.append(r)
        else:
            # Since our ranges overlap, we merge them by updating the end of the last reduced range.
            reduced_ranges[-1] = (reduced_ranges[-1][0], max(reduced_ranges[-1][1], r[1]))

    return reduced_ranges

def check_ingredient_spoliage(ingredient_list, reduced_ranges):
    # Picking out the ingredient and checking if it falls within any of the reduced ranges.
    # Map to a list of tuples (ingredient, is_fresh)
    result = list(map(lambda i: (int(i), any(int(i) >= r[0] and int(i) <= r[1] for r in reduced_ranges)), ingredient_list))
    return result


# Main execution
if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else None
    fresh_ingredient_ranges, ingredient_list = read_input(input_file)
    print("Fresh Ingredient Ranges:", fresh_ingredient_ranges)
    print("Ingredient List:", ingredient_list)

    fresh_ingredient_ranges = reduce_fresh_ingredient_ranges(fresh_ingredient_ranges)
    print("Reduced Fresh Ingredient Ranges:", fresh_ingredient_ranges)
 
    fresh_ingredient_results = check_ingredient_spoliage(ingredient_list, fresh_ingredient_ranges)
    print("Ingredient Verification Results (Ingredient, Is Fresh):", fresh_ingredient_results)

    # The most convoluted and most pythonic of lines, this is a comprehension statement.
    # The tuple is structured as (ingredient, is_fresh), but we aren't interested in the ingredient value here so we throw it away with '_'.
    # Instead, we just add 1 for each fresh ingredient (is_fresh == True) in the list of tuples.
    number_of_fresh_ingredients = sum(1 for _, is_fresh in fresh_ingredient_results if is_fresh)
    print("Sum of Fresh Ingredients:", number_of_fresh_ingredients)

    # reduce example: Accumulate (acc) the total number of fresh ingredients across all ranges, which represented as tuples (t).
    fresh_ingredients_across_all_ranges = reduce(lambda acc, t: acc + (t[1] - t[0] + 1), fresh_ingredient_ranges, 0)
    print("Total Number of Fresh Ingredients in Ranges:", fresh_ingredients_across_all_ranges)

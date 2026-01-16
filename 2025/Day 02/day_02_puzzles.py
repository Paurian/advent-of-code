import sys

# Read the input from a file or return an empty list
def read_input(filename=None):
    split_lines = []
    if filename:
        with open(filename, 'r') as file:
            lines = file.read().strip().splitlines()
            for line in lines:
                split_lines.extend(line.split(','))
            return split_lines
    else:
        return []

# Get a list of invalid IDs where the ID consists of two identical halves
def get_list_of_invalid_ids(ranges):
    invalid_ids = []
    for r in ranges:
        start, end = map(int, r.split('-'))
        for i in range(start, end + 1):
            string_value = f"{i}"
            if len(string_value) % 2 == 0:
                mid = len(string_value) // 2
                left, right = string_value[:mid], string_value[mid:]
                if left == right:
                    invalid_ids.append(i)
    return invalid_ids

# Though we could do a quick determination that we don't exceed half the length of the string,
# we could optimize the search further by creating a set of possible denominators to check against.
# For example, a 9-character string can only be divided by 1 or 3 to create repeated segments and a
# 12-character string can be divided by 1, 2, 3, 4, or 6.
def get_full_partial_lengths(string_value):
    partial_lengths = []
    max_partial_length = len(string_value) // 2
    for mpl in range(max_partial_length, 0, -1):
        max_partial_length = mpl
        if len(string_value) % mpl == 0:
            partial_lengths.append(mpl)
    return partial_lengths

# Get a list of invalid IDs where the ID consists of repeated segments of any length
def get_extra_list_of_invalid_ids(ranges):
    extra_invalid_ids = []
    for r in ranges:
        start, end = map(int, r.split('-'))
        for i in range(start, end + 1):
            string_value = f"{i}"
            partial_lengths = get_full_partial_lengths(string_value)
            for j in partial_lengths:
                # Verify all parts are the repeated
                test_string = string_value[:j]
                repeats = len(string_value) // j
                if test_string * repeats == string_value:
                   extra_invalid_ids.append(i)
                   break
    return extra_invalid_ids

# Sum the invalid IDs
def sum_of_invalid_ids(invalid_ids):
    return sum(invalid_ids)


# Main execution
if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else None
    lines = read_input(input_file)
    print(lines)
    invalid_ids = get_list_of_invalid_ids(lines)
    print("List of invalid IDs:", invalid_ids)
    result = sum(invalid_ids)
    print("The sum of invalid IDs:", result)

    extra_invalid_ids = get_extra_list_of_invalid_ids(lines)
    print("List of extra invalid IDs:", extra_invalid_ids)
    result = sum(extra_invalid_ids)
    print("The sum of extra invalid IDs:", result)
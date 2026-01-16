import sys
from functools import reduce
import re

# Read the input from a file or return an empty list
def read_input(filename=None):
    number_lists = []
    operator_list = []
    if filename:
        with open(filename, 'r') as file:
            lines = file.read().strip().splitlines()
            # The last line contains the operators
            operator_list = list(lines[-1].replace(" ", ""))
            # Get all numbers from each line except the last line
            unpivoted_number_lists = list(map(lambda l: list(map(int, re.findall(r'\d+', l))), lines[:-1]))
            # Nifty trick to unpivot a list of lists
            number_lists = list(zip(*unpivoted_number_lists))
    return number_lists, operator_list


def apply_operator(a, b, operator):
    if operator == '+':
        return a + b
    elif operator == '-':
        return a - b
    elif operator == '*':
        return a * b
    elif operator == '/':
        return a / b
    else:
        raise ValueError(f"Unknown operator: {operator}")


def calculate_result(number_lists, operator_list):
    results = []
    for i in range(len(number_lists)):
        operator = operator_list[i]
        numbers = number_lists[i]
        # Get the result by reducing the numbers with the given operator
        result = reduce(lambda x, y: apply_operator(x, y, operator), numbers)
        results.append(result)
    return results


# This function reads the input in a cephalopod style
# i.e., numbers are aligned vertically down the columns, ignoring spaces.
# After tinkering with lambda functions and zip, it seemed clearer and simpler to just do nested loops.
def cephalopod_read_input(filename=None):
    number_lists = []
    operator_list = []
    if filename:
        with open(filename, 'r') as file:
            lines = file.read().splitlines()
            # The last line contains the operators
            operator_list = list(lines[-1].replace(" ", ""))
            # But numbers are aligned vertically down the columns, ignoring spaces.
            number_list = []
            list_of_number_lists = []
            print(f"length of last line: {len(lines[-1])}")
            for char_pos in range(len(lines[-1])):
                number_string = ""
                for line in lines[:-1]:
                    number_string += line[char_pos]
                if number_string.strip():  # Only consider non-empty strings
                    number_list.append(int(number_string))
                else:
                    list_of_number_lists.append(tuple(number_list))
                    number_list = []
            if number_list:  # Append any remaining numbers
                list_of_number_lists.append(tuple(number_list))
    return list_of_number_lists, operator_list                




# Main execution
if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else None
    number_lists, operator_list = read_input(input_file)
    print("Number Lists:", number_lists)
    print("Operator List:", operator_list)
    results = calculate_result(number_lists, operator_list)
    print("Results:", results)
    result_sum = sum(results)
    print("Sum of Results:", result_sum)
    
    # Cephalopod reading
    number_lists, operator_list = cephalopod_read_input(input_file)
    print("Ceph Number Lists:", number_lists)
    print("Ceph Operator List:", operator_list)
    results = calculate_result(number_lists, operator_list)
    print("Ceph Results:", results)
    result_sum = sum(results)
    print("Sum of Ceph Results:", result_sum)
    

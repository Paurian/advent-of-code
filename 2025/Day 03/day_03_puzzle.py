import sys

# Read the input from a file or return an empty list
def read_input(filename=None):
    if filename:
        with open(filename, 'r') as file:
            return file.read().strip().splitlines()
    else:
        return []

# Get the voltages from the battery banks, considering the top N batteries in each bank, provided they are in successive positions
def get_voltages(banks, number_of_batteries=2):
    voltages = []
    # From the first battery to the (last battery - number_of_batteries + 1)
    # If the current battery is greater than the first battery in the list, reassign the battery list
    # Stop at 9. The remainig batteries in the bank can then be checked for the next battery
    for bank in banks:
        battery = ["0"]*number_of_batteries # Initialize battery list for each bank

        left_pos = 0
        for b in range(number_of_batteries):
            b_end = len(bank) - (number_of_batteries - b) + 1
            for j in range(left_pos, b_end):
                if bank[j] > battery[b]:
                    battery[b] = bank[j]
                    left_pos = j + 1 # Starting point for next battery
                if battery[b] == 9:
                    break

        # Append the battery value to the voltage list
        voltage = ""
        for v in battery:
            voltage = voltage + v
        voltages.append(int(voltage))
    return voltages


# Main execution
if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else None
    banks = read_input(input_file)
    voltages = get_voltages(banks, 2)
    print("Voltages for 2 batteries:", voltages)
    print("Sum of voltages:", sum(voltages))

    voltages = get_voltages(banks, 12)
    print("Voltages for 12 batteries:", voltages)
    print("Sum of voltages:", sum(voltages))
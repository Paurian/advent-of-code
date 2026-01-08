import sys

def read_input(filename=None):
    if filename:
        with open(filename, 'r') as file:
            return file.read().strip().splitlines()
    else:
        return []

def process_data(lines):
    dial = 50
    zero_count = 0
    for line in lines:
        try:
            turn = line[0:1]
            number = int(line[1:])
            if turn == 'R':
                # Python handles negative modulo differently than some languages
                # In this case, we're leveraging that to simplify the wrap-around logic
                dial = (dial + (number % 100)) % 100
            elif turn == 'L':
                dial = (dial + number) % 100
        except ValueError:
            continue
        if dial == 0:
            zero_count += 1
    return zero_count

if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else None
    lines = read_input(input_file)
    result = process_data(lines)
    print(result)
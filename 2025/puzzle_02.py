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
        rotation = 0
        try:
            turn = line[0:1]
            clicks = int(line[1:])
            if turn == 'R':
                rotation = -1
            elif turn == 'L':
                rotation = 1
        except ValueError:
            print('Value Error encountered, skipping line:', line)
            continue

        relative_clicks = (rotation * clicks) % 100
        dial_rotations = clicks // 100
        dial_offset = dial + (rotation * clicks)
        new_dial = (dial + relative_clicks) % 100

        # Handle times the dial passed zero
        if new_dial != dial_offset or dial == 0:
            dial_rotations += 1

        print("From {}, turn {} to {} for {} times past (or on) 0".format(dial, line, new_dial, dial_rotations))
        zero_count += dial_rotations

        dial = new_dial
    return zero_count

if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else None
    lines = read_input(input_file)
    result = process_data(lines[0:100])
    print(result)
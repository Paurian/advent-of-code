import sys

# Read the input from a file or return an empty list
def read_input(filename=None):
    if filename:
        with open(filename, 'r') as file:
            return file.read().strip().splitlines()
    else:
        return []

# Count the number of times the dial lands on zero
def count_times_landing_on_zero(lines, start_dial=50):
    dial = start_dial
    zero_count = 0
    for line in lines:
        dir = 1 if line[0] == "R" else -1
        clicks = dir * int(line[1:])
        dial = (dial + clicks) % 100
        zero_count += 1 if dial == 0 else 0

    return zero_count

# Count the number of times the dial passes or lands on zero
def count_clicks_on_or_past_zero(lines, start_dial=50):
    dial = start_dial
    zero_count = 0
    for line in lines:
        dir = 1 if line[0] == "R" else -1
        clicks = dir * int(line[1:])

        if dial + clicks <= 0:
            zero_count += (abs(dial + clicks) // 100 + (dial != 0))
        elif dial + clicks > 99:
            zero_count += (dial + clicks) // 100

        dial = (dial + clicks) % 100
    return zero_count

# Alternate (from the illustrious Josiah) Count the number of times the dial passes or lands on zero
def alt_count_clicks_on_or_past_zero(lines, start_dial=50):
    answer = 0
    pos = 50
    for rot in lines:
        past = pos
        pos += (1 if rot[0] == "R" else -1) * int(rot[1:])

        if rot[0] == "L":
            if pos == 0 : answer += 1
            elif pos < 0 and past > 0 : answer += 1

        answer += abs(pos)//100
        pos %= 100
    return answer



# Main execution
if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else None
    lines = read_input(input_file)

    result = count_times_landing_on_zero(lines)
    print("Number of turns landing on zero:", result)

    result = count_clicks_on_or_past_zero(lines)
    print("Number of turns on or past zero:", result)

    result = alt_count_clicks_on_or_past_zero(lines)
    print("Alternate count of turns on or past zero:", result)

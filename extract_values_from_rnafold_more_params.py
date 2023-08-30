import sys
import re

# Check if the correct number of command line args are provided
if len(sys.argv) != 3:
    print("Usage: python script.py input_file output_file")
    sys.exit(1)

# Specify input and output files
input_file_path = sys.argv[1]
output_file_path = sys.argv[2]

# Open the input file for iteration
with open(input_file_path, 'r') as infile:
    lines = infile.readlines()

# Open the output file for writing
with open(output_file_path, 'w') as outfile:
    # Iterate through the lines in steps of 6
    for i in range(0, len(lines), 6):
        # Extract values using regex
        
        # Extract value from third line enclosed in parentheses
        third_value_match = re.search(r'\((-?\d+\.\d+)\)', lines[i + 2])
        third_value = third_value_match.group(1) if third_value_match else "N/A"

        # Extract value from fourth line enclosed in brackets
        fourth_value_match = re.search(r'\[(-?\d+\.\d+)\]', lines[i + 3])
        fourth_value = fourth_value_match.group(1) if fourth_value_match else "N/A"

        # Extract two values from fifth line enclosed in squiggly brackets
        fifth_value_match = re.search(r'\{(-?\d+\.\d+) d=(-?\d+\.\d+)\}', lines[i + 4])
        if fifth_value_match:
            fifth_value_1 = fifth_value_match.group(1)
            fifth_value_2 = fifth_value_match.group(2)
        else:
            fifth_value_1 = "N/A"
            fifth_value_2 = "N/A"

        # Extract the two numeric values from the sixth line
        
        # Use regex to capture decimal and scientific notation
        sixth_values = re.findall(r'((?:\d+\.\d+)|(?:\d+\.\d+e-\d+))', lines[i + 5])

        # Write tab-delimited output
        output_line = (
            lines[i].strip(),          # Original line from first row
            third_value,               # Numeric value from third row
            fourth_value,              # Numeric value from fourth row
            fifth_value_1,             # First numeric value from fifth row
            fifth_value_2,             # Second numeric value from fifth row
            sixth_values[0] if len(sixth_values) > 0 else "N/A",  # First numeric value from sixth row
            sixth_values[1] if len(sixth_values) > 1 else "N/A"   # Second numeric value from sixth row
        )
        outfile.write('\t'.join(output_line) + '\n')

#!/bin/bash

# Verify the correct number of command line arguments
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <input_file> <output_file>"
    exit 1
fi

# Command line arguments to provide input and output files
input_file="$1"
output_file="$2"

# Read each line from the input file
while IFS= read -r line; do
    # Check if the line starts with a sequence header'>' 
    if [[ "$line" == ">"* ]]; then
        # If it iss a seq header, write it to the output file
        echo "$line" >> "$output_file"
    else
        # If it's a sequence line, replace all characters except '>' with '.'
        modified_line=$(echo "$line" | tr -c '>' '.')
        # It seems like there is often an extra dot relative to the number of nucleotides in the input
        # Remove the last dot (if present) to match the original sequence length
        modified_line="${modified_line%.}"
        # Write the dot sequence to the output
        echo "$modified_line" >> "$output_file"
    fi
done < "$input_file"
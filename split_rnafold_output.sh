#!/bin/bash

# check for inputs and output
if [ $# -ne 2 ]; then
    echo "Usage: $0 <input_file> <output_file>"
    exit 1
fi

input_file="$1"
output_file="$2"

# Read the input file line by line
while IFS= read -r line; do
    # Check if the line starts with a fasta header ">"
    if [[ $line =~ ^\>(.*)$ ]]; then
        # Isolate the sequence name after the ">" character
        sequence="${BASH_REMATCH[1]}"
    fi
    
    # Check if the line contains the numeric value
    if [[ $line =~ \((-?[0-9]+\.[0-9]+)\)$ ]]; then
        # Isolate the numeric value enclosed in parentheses
        value="${BASH_REMATCH[1]}"
        
        # Output the sequence ID and value to the output file, tab delimited
        echo -e "$sequence\t$value" >> "$output_file"
    fi
done < "$input_file"

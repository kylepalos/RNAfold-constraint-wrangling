#!/bin/bash

# Check for correct inputs and outputs
if [ "$#" -ne 3 ]; then
    echo "Usage: $0 input_file1 input_file2 output_file"
    exit 1
fi

# Input files provided by sys args
file1="$1"
file2="$2"

# Output file
output_file="$3"

# Create a temporary directory to store sequences from the input sequence fasta file
temp_dir=$(mktemp -d)

# Read in sequences from file1-fasta file and store in the temporary directory
current_seq=""
while IFS= read -r line; do
    if [[ "$line" =~ ^\>.+ ]]; then
        current_seq="${line#>}"
    else
        echo "$line" >> "$temp_dir/$current_seq"
    fi
done < "$file1"

# Read sequences from file2 and combine with sequences from file1. Finally save to output file
current_seq=""
while IFS= read -r line; do
    if [[ "$line" =~ ^\>.+ ]]; then
        current_seq="${line#>}"
        echo "$line"
        cat "$temp_dir/$current_seq"
    else
        echo "$line"
    fi
done < "$file2" > "$output_file"

# Remove temp dir
rm -rf "$temp_dir"

echo "Combined sequences written to $output_file"
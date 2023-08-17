import sys

def replace_bases_in_fasta(fasta_file, tsv_file, output_file):
    # Read the constraint positions from the position tsv file and store them in a nested dictionary
    positions = {}
    with open(tsv_file, 'r') as tsv:
        for line in tsv:
            name, position = line.strip().split('\t')
            if name not in positions:
                positions[name] = []
            positions[name].append(int(position))
    
    # Modify the dots in the fasta file to 'x' characters
    with open(fasta_file, 'r') as fasta, open(output_file, 'w') as output:
        current_seq = ""         # Specifies the  sequence being processed
        current_name = None      # Specifies the name of the sequence being processed
        current_positions = None # Specifies the positions to modify for the sequence being processed
        
        for line in fasta:
            if line.startswith('>'):
                # Process previous sequence
                if current_name and current_name in positions:
                    modified_seq = current_seq
                    for position in positions[current_name]:
                        # Replace the base (a dot) at the specified position with 'x'
                        modified_seq = modified_seq[:position-1] + 'x' + modified_seq[position:]
                    # Send the new modified sequence to the output 
                    output.write(f">{current_name}\n{modified_seq}\n")
                else:
                    # If the current sequence doesn't need to be modified, write it as is
                    output.write(line)
                
                # Start processing a new sequence
                current_name = line.strip()[1:] # Extract the next sequence ID
                current_seq = ""                # Reset the sequence to the next seq.
                current_positions = positions.get(current_name, []) # Get positions for the current sequence
            else:
                current_seq += line.strip() # Append the current line to the current sequence
        
        # And for the last sequence
        if current_name and current_name in positions:
            modified_seq = current_seq
            for position in positions[current_name]:
                modified_seq = modified_seq[:position-1] + 'x' + modified_seq[position:]
            output.write(f">{current_name}\n{modified_seq}\n")
        else:
            # If the last sequence doesn't need to be modified, write as is
            output.write(f">{current_name}\n{current_seq}\n")

# Check for the correct command line arguments
if len(sys.argv) != 4:
    print("Usage:", sys.argv[0], "<input_fasta> <input_tsv> <output_fasta>")
    sys.exit(1)

# Inputs and outputs provided by sys args
input_fasta = sys.argv[1]
input_tsv = sys.argv[2]
output_fasta = sys.argv[3]

# Call the function to replace bases in the FASTA sequences
replace_bases_in_fasta(input_fasta, input_tsv, output_fasta)

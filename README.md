# RNAfold-constraint-wrangling

This repository is meant to host useful scripts for adding structural constraints to [ViennaRNA's](https://github.com/ViennaRNA/ViennaRNA) RNAfold algorithm.

Manual structural constraints are meant to tell the alroithm about known scrucutral features before predicting structure.

Providing constraints to RNAfold comes in the form of a modified fasta file, consider:

```
>sequence1
AUGC
.x..
```

This fasta entry for sequence1 allows A, G, and C (represented by a '.') to freely base-pair, but U (represented by a 'x') is not allowed to base-pair.

Generating a fasta file with hundreds to thousands of sequences that also have incorporated constraints is not straightforward.

This repository will walk through the steps to:

1. Generate a new fasta file where all nucleotides have been replaced by '.' characters.
2. Utilize an accessory file to specify the transcript positions that need to be changed from a '.' to an 'x'
3. Interleave the RNA sequences with the structural constraints.


# Very basic workflow

Starting with a genome fasta file and a genome annotation file (gtf/gff), get transcript sequences with [gffread](https://github.com/gpertea/gffread)

```
gffread -w my_transcriptome.fa -g my_genome.fa my_annotation.gtf
```

Now you have transcripts, I'd recommend cleaning up the headers and converting the transcriptome from DNA to RNA:

```
cut -d" " -f1 my_transcriptome.fa > my_transcriptome_clean.fa

perl -pe 'tr/tT/uU/ unless(/>/)' < my_transcriptome_clean.fa > my_transcriptome_clean_rna.fa
```

Now convert the fasta file of nucleotides to a fasta file of dots (representing no constraints)

```
bash convert_sequences_to_dots.sh my_transcriptome_clean_rna.fa my_dot_transcriptome.fa
```

The next step would be to convert positions of interest from a '.' to a 'x'

The following script takes a tab-separated file with sequence names in column 1, and positions to change in column 2, such as:

```
sequence1  1234
sequence1  5678
sequence2  910
```

These sequence names must match the sequence names in the transcriptome fasta files.
Note that you can change multiple positions in the same transcript.

```
python3 convert_dots_to_x_by_position.py my_dot_transcriptome.fa my_positions.txt my_dot_and_x_transcriptome.fa
```

You then need to interleave the sequences and dot-x notation to get an output that looks like the sequence at the top of the README.

```
bash combine_seq_with_dots_and_x.sh my_transcriptome_clean_rna.fa my_dot_and_x_transcriptome.fa for_rnafold.fa
```

This file can be used as input for RNAfold:

```
RNAfold -C for_rnafold.fa > rnafold_output.txt
```

This will give you an output that looks like the following:

```
>sequence1
AUGC
.x.. (-100)
```

But a more useful output would probably be a tab separated file like:

```
sequence1  -100
```

You can use the final script in the repo:

```
bash split_rnafold_output.sh rnafold_output.txt rnafold_output_clean.txt
```

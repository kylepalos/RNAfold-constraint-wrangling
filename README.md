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

Now you have transcripts, I'd recommend cleaning up the headers

```
cut -d" " -f1 my_transcriptome.fa > my_transcriptome_clean.fa
```

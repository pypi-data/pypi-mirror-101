![riboloco Logo](ribolocologo3.png)
# riboloco
A tool for consistently converting monosome-, disome-, trisome- (etc.) profiling data to single codon resolution. 

Riboloco employs a hybrid approach for determining the A/P/E-site offsets - for highly abundant read types, it uses enrichment at the start/stop codons or positions with greatest sequence bias. For less abundant read types, or those which cannot be easily determined from start/stop codon enrichment (eg disome/trisome footprints) it looks for sample-specific slow-to-decode signatures. 

Riboloco generates a report on each sample, showing which features cause greatest slowing/stalling of ribosomes, and how each footprint type is distributed across the coding sequences. Optionally, it can also detect signatures of out-of-frame translation, enabling identification of novel peptides.

# Quick reference:

## Step 1 - Generate information file and transcriptome fasta:

Build an "information" file from a user-supplied GFF file, and a fasta containg all the transcript sequences with the introns spliced out fron the user-supplied genomic fasta.

```riboco_convert_gff --input_gff your_gff_file.gff --genome_fasta your_fasta.fasta.gz --output_filename my_converted_files```


## Step 2 (Optional!) - Search for all open reading frames:

Useful for determining if specific read types are enriched for out of frame ribosomes. Uses the transcriptome fasta and the info file generated in step 1.

```riboloco_find_orfs -f your_transcriptome_fasta.fa -i your_info_file -o output_name```


## Step 3 - Detect ribosome positions and write out files

The simplest use would be:

```riboloco -s your_bam_or_bed_file -f your_transcriptome_fasta.fa -i your_info_file -o output_name```

There are a ton of optional arguments. Important ones:

--orf_file: supply the orf file generated in step 2 for a more detailed analysis of out-of-frame ribosomes

--plot_graphs: save a ton of graphs which show the properties of each footprint type

--min_abundance: the minimum fractional abundance of a read type to be included in analysis.

--save_stats: save data files used to make plots

# A more in-depth description:

## The riboloco approach

Ribosome profiling experiments generate footprints of approximately 30 nts. An important step in analysis is to determine which codon the ribosome that generated each footprint was translating.

Riboloco is based on the following principles:
* Most translation within annotated reading frames (ORFs) is in-frame with the annotated ORF, thus the most abundant footprint types will mainly correspond to in-frame translation
* Ribosome footprints are enriched at slow-to-decode sequences

Riboloco's algorithmic approach consists of the following two steps:
1. Identify slow-to-decode signatures from the most abundant footprint types 
2. Determine the correct offset for other footprint types by searching for these slow-to-decode signatures wtihin these footprints

Riboloco attempts to determine offsets for each "footprint type". Offsets are defined from the 3' end of each read, and are thus negative. A footprint type is defined by:
* Its read length
* The frame of the last (most 3') nucleotide, relative to the annotated start codon
* Optionally, whether the 5' end contains a mismatch - these are common due to non-templated nuelceotide addition during reverse transcription. Addition of such nucleotides impacts downstream ligation bias. (Only available, via the -mm option, when using a .bam file as input)

### Identifying slow-to-decode signatures:

Riboloco searches for codon RUST-enrichments (O'Connor et al., 2016) within the A, P and E sites. It first determines the A/P/E position for abundant footprint types using conventional methods (see below) and finds the RUST enrichments that correspond to these positions. Next, it searches for correct offsets for less abundant (thus more noisey) footprint types by searching for these slow-to-decode signatures in each footprint type.

Methods for initial detection of A/P/E sites for abundant footprints:
* Start codon enrichment (default, but not suitable for disome/trisomes etc)
* Positions of greatest Kullback-Leibler divergence/sequence bias (O'Connor et al., 2016)
* User defined
* Stop codon enrichment (not recommended)


### Best approach for monosome samples

Riboloco can be used with default settings. For particularly low read-depth samples, it may be useful to define a specific A-site offset (eg -t 28_0:-12)



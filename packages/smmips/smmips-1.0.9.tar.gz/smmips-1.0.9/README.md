# smMIPs #

smMIPs is tool for generating QC metrics in sequenced Single Molecule Molecular Inversion Probes libraries.

## Installation ##
### From PyPi ###
smmips is available from PyPi

```pip install smmips```

## Alignment to reference genome ##

Fastqs containing smMIP probes and UMIs need first to be aligned to a reference genome.
This can be done outside of smmips.py or with the ```align``` command. Paired fastqs are then aligned with ```bwa mem``` to a reference genome.

## smMIP assignment ##

Each aligned read pair is then assigned to a smMIP listed in the input panel.
The panel should be designed with [MIPGEN](http://shendurelab.github.io/MIPGEN/) and have the same columns and header. 

This step generates 2 coordinate-sorted and indexed bam with reads assigned to smMIPs and tagged with the smMIP name and the UMI sequence in the ```out``` subdirectory:
- out/prefix.assigned_reads.sorted.bam: assigned reads with capture target       
- out/prefix.empty_reads.sorted.bam: assigned reads missing target smmip

QC metrics with read counts are reported in two json files in the ```stats``` subdirectory:

- stats/prefix_extraction_metrics.json: read counts, including total reads, assigned and unassigned reads, empty smMIPs
- stats/prefix_smmip_counts.json: read counts without and with target for each smMIP in the panel

By default all the reads in the alignment file are assessed against the smmips in the panel. However, one can examine reads mapped to a single chromosome or a region within a chromosome.
This can potentially be used for parallelizing smmip assignments and a job for each chromosome or region. Command ```merge``` can be used to merge alignment files and stats files generated for different regions.
Script smmipRegionFinder.py can be used to defined the regions to examine.  


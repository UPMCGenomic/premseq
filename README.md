# PREMSEQ

PREprocessing Module for rna-SEQ data

## About
   Most modern sequencing technologies produce read that have adapter sequence at the end, a deteriorating quality towards the ends, incorrectly called bases in some regions and ... . All these bad quality reads negatively impact on assembly, mapping and downstream bioinfomatics analyses. These are particulary true, in de novo assembly where the genome or the transcriptome is reconstructed only based on information contained in reads.


   **Premseq** FASTQ trim and filter to remove low-quality base calls from reads. It can also remove detrimental artifacts introduced into the reads by the sequencing process. It uses Trimmomatic for trimming reads and FastQC to control read quality before and after trimming. It has two ways of working. It can either read trimming information from an XML file (A), either read  directly from the command line (B). Each ways has two modes, 'Single-Ends' (SE) and 'Paired-Ends' (PE).

 This module performs quality based and adapter trimming and filtering of FASTQ-formatted short read data produced by Illumina sequencers. Various criteria are available for trimming and filtering reads. The module operates on both paired end or single end data. Trimmomatic works with Illumina FASTQ files using phred33 or phred64 quality scores. Compressed input and output is supported and auto-detected from the file name (.gz, .bz2).

   PREMSEQ is an independant module for **adapter and quality trimming** of RNA-seq data which uses **Trimmomatic** and **FastQC**. This module is integrated in a pipeline of de novo assembly for non-models organisms. Here is the pipeline link : https://github.com/arnaudmeng/denovo-assembly-pipeline-upmc


## Version
1.0

## Requirements

**Python** 2.7.6

**Java** (for Trimmomatic) 

**Perl** (for FastQC)

## Usage

This module has two ways of working (reading input files and trimming parameters) from : 

- **an XML file** (A)
      
- or **command line directly** (B)


And each way has two modes to work :

- **single ends** "SE" `./premseq.py SE` 
     
- **paired ends** "PE" `./premseq.py PE`


To read input files and trimming parameters from the XML file, run :

`python ./premseq.py --XML`


To launch trimmomatic using commandline arguments see below:

   For more informations, see module help, running:

`python ./premseq.py --help`

or

`python ./premseq.py -h`
      
      
## Single ends data

`./premseq.py SE` takes an input fastq file and output a trimmed version of the file. 

It has all options given by Trimmomatic :

- remove adapter sequences : `illuminaclip <fastaWithAdaptersEtc>:<seed mismatches>:<palindrome clip threshold>:<simple clip threshold>` An example of adapter file is given, it removes illumina adapters and poly(A or T) tails

      Recommend : fasta-file:2:30:10
- quality trimming : `-slidingwindow <window-size>:<required-quality>` 

      Recommend : 4:30 for data with good quality, else 10:20
- adaptative quality trimming depending on the length of reads : `-maxinfo <target-length>:<strictness>`
- trim base from 5' end until the required minimal quality is achieved : `-leading <required-quality>`
- trim base from 3' end until the required minimal quality is achieved : `-trailing <required-quality>`
- trim a fixed number of bases from 5' end : `-head <number>`
- trim a fixed number of bases from 3' end : `-crop <number>`
- remove read shorter than a given length : `-minlen <length>`
- remove read which average quality is below the specified threshold : `-avgqual <quality>`
- re-encode phred score : `tophred33 | tophred64`


### Examples :

      python premseq.py SE read_1.fastq -illuminaclip fasta-file.fa:2:10:30
      python premseq.py SE read_1.fq -slidingwindow 10:30
      python premseq.py SE read_1.fq -maxinfo 15:0.8 -crop 7
      python premseq.py SE read_1.fq -slidingwindow 10:30 -leading 30 -minlen 36 -fastqc
      python premseq.py SE read_1.fq -illuminaclip fasta-file.fa:2:10:30 -slidingwindow 4:30 -leading 30 -minlen 36
      
      
## Paired ends data

`./premseq.py PE` takes two input fastq files and outputs a trimmed version of these files and a two files containing 'single reads' for each direction. 'Single reads' are reads who passed the filter for one direction but not the other. 

This mode has also all options given by Trimmomatic, see above.

### Examples :

      python premseq.py PE read_1.fastq read_2.fastq -illuminaclip fasta-file.fa:2:10:30 -crop 10
      python premseq.py PE read_1.fastq read_2.fastq -illuminaclip fasta-file.fa:2:10:30 -crop 10 -maxinfo 15:0.9
      python premseq.py PE read_1.fq.bz2 read_2.fq.bz2 -illuminaclip fasta-file.fa:2:10:30 -slidingwindow 10:30 -minlen 36
      python premseq.py PE read_1.fastq read_2.fastq -illuminaclip fasta-file.fa:2:10:30 -trailing 30 -fastqc

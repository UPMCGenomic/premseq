#! /usr/bin/env python
# -*- coding: utf8 -*-

""" 
parse_args.py : module containing all functions to parse commandline arguments.

Dependency : check_entries (personal module)
"""

__author__ = "Anita Annamalé"
__version__  = "1.0"
__copyright__ = "copyleft"
__date__ = "2015/07"

#-------------------------- MODULES IMPORTATION -------------------------------#


import argparse
import sys
import os.path
from argparse import RawTextHelpFormatter

# Personal module
import check_entries as ce


#---------------------------- CLASS DEFINITION --------------------------------#


class color:
   BOLD = '\033[1m'
   END = '\033[0m'


#-------------------------- FUNCTIONS DEFINITION ------------------------------#


# MENU of Premseq --------------------------------------------------------------

def premseq_parser():
    """
    Menu of Premseq 

    Don't takes argument
    
    Return parser
    """

    parser = argparse.ArgumentParser( 
        formatter_class = RawTextHelpFormatter,

        usage = color.BOLD + '\r       \n' +
"    PREMSEQ - A high throughput sequence adapter & quality trimming tool"

"\n\nSYNOPSIS\n\n" + color.END +

"  (A)\t%(prog)s --XML file.xml\n\n"
"  (B)\t%(prog)s SE input.fastq [options]\n\t"
"or\n\t%(prog)s PE input1.fastq input2.fastq [options]\n\n"

"    options : [-threads NN] [-output directory] [-phred {33,64}] \n"
"              [-illuminaclip file:NN:NN:NN] [-slidingwindow NN:NN] \n"
"              [-maxinfo NN:NN] [-leading NN] [-trailing NN] [-headcrop NN] \n"
"              [[-crop NN] [-avgqual NN] -minlen NN] [-keep-singleton] \n"
"              [-tophred33 | -tophred64] [-fastqc] \n",

        description= color.BOLD + "\n\nDESCRIPTION\n\n" + 
"    PREMSEQ" + color.END +
" FASTQ trim and filter to remove low-quality base calls from reads.\n"
"    It can also remove detrimental artifacts introduced into the reads by the\n"
"    sequencing process. It uses Trimmomatic for trimming reads and FastQC to\n"
"    control read quality before and after trimming. It has two ways of working.\n"
"    It can either read trimming information from an XML file (A), either read \n"
"    directly from the command line (B). Each ways has two modes, 'Single-Ends' \n"
"    (SE) and 'Paired-Ends' (PE).\n"
"\n"
"    This module performs quality based and adapter trimming and filtering of\n"
"    FASTQ-formatted short read data produced by Illumina sequencers. Various\n"
"    criteria are available for trimming and filtering reads. The module operates\n"
"    on both paired end or single end data. Trimmomatic works with Illumina FASTQ\n"
"    files using phred33 or phred64 quality scores. Compressed input and output\n"
"    is supported and auto-detected from the file name (.gz, .bz2).\n"
"\n"
"Use '%(prog)s --help' to see all command-line options.",

        epilog=color.BOLD + "\n\nEXAMPLES:\n\n" + color.END +
"   python %(prog)s -h                       for help\n\n"
"   python %(prog)s --XML file.xml           to launch trimmomatic using \n"
"                                               parameters from the XML file\n\n"
"   python %(prog)s PE \ \n"
"   read_1.fastq read_2.fastq \ \n"
"   -illuminaclip fasta-file.fa:2:10:30        for adapter trimming\n\n"
"   python %(prog)s SE read_1.fq \ \n"
"   -slidingwindow 10:30 \ \n"
"   -leading 30 -minlen 36                     for quality trimming\n\n"
"   python %(prog)s PE \ \n"
"   read_1.fq.bz2 read_2.fq.bz2 \ \n"
"   -illuminaclip fasta-file.fa:2:10:30 \ \n"
"   -slidingwindow 10:30 -minlen 36            for adapter and quality trimming.\n"
" \n")
 

    
    parser.add_argument("--XML",
                        type=str,
                        nargs=1,
                        action='store', 
                        help="Take trimming parameter from a given xml file.\n"
                        "  Usage:\n    '--XML file.xml'\n\n")
    
    
    group = parser.add_argument_group(
            color.BOLD + 'Options for commandline mode' + color.END,

            description="For commandline mode, the 'layout' of high throughput"
                        " sequencing data and \ninput file(s) (one for SE and two"
                        " for PE) are obligatory arguments.")

    group.add_argument("layout", 
                        type=str, 
                        nargs='?',
                        action='store', 
                        help = "Reads layout, can be single-ends (SE) or "
                        "paired-ends (PE).\n"
                        "  Usage: 'SE' or 'PE'\n\n")
    
    group.add_argument("input", 
                        type=str, 
                        nargs= '*',
                        action='store',
                        help = "Input read FASTQ file. One if SE or two if PE.\n" 
                        "  Usage:\n    - SE 'readfile.fastq' || 'readfile.fq.gz'\n"
                        "    - PE 'read_1.fastq read_2.fastq'    ||\n\t"
                        " 'read_1.fastq.gz/bz2 read_2.fastq.gz/bz2'\n\n")
    
    group.add_argument("-output",
                        type=str,
                        action='store',
                        default=os.getcwd(),
                        help="Name of directory for output (will be created if it\n"
                        "doesn't already exist).\n"
                        "  Default '%s' \n\n" %os.getcwd())
    
    group.add_argument("-threads",
                        type=int,
                        action='store',
                        default= 1,
                        help = "Number of threads to use.\n"
                        "  Usage : '-threads 5'\n\n")
    
    group.add_argument("-phred",
                        type=int,
                        action='store',
                        choices=[33,64],
                        help = "Phred quality of reads, can be 33 or 64.\n"
                        "  Usage : '-phred 33'\n\n")

    group.add_argument("-illuminaclip",
                        type=str,
                        action='store',
                        help= "Specify a non-default file which contains a list of\n"
                        "adapter sequences which will be searched on reads and\n"
                        "removed. The tolerated number of base mismatches and the\n"
                        "tolerated score threshold for each mode (simple for SE\n"
                        "and palindrome for PE) are required.\n"
                        "  Usage: \n   -illuminaclip <fastaWithAdaptersEtc>:"
                        "<seed mismatches>:\n   <palindrome clip threshold>:<simple"
                        " clip threshold>\n  Recommendation: fasta-file:2:30:10\n\n")
    
    group.add_argument("-slidingwindow",
                        type=str,
                        action='store',
                        help= "Sliding Window with quality and length threshold. It\n"
                        "takes the quality values and slides a window of a chosen\n"
                        "length across reads. The window slides along the quality\n"
                        "values until the average quality in the window drops\n"
                        "below the quality threshold, the algorithm determines\n"
                        "where in the window the drop occurs and cuts both the\n"
                        "read (3'-end cut).\n"
                        "  Usage: \n"
                        "   -slidingwindow <window-size>:<required-quality>\n"
                        "  Recommended: 4:30 for data with good quality, \n"
                        "               else 10:20\n\n")
    
    group.add_argument("-maxinfo",
                        type=str,
                        action='store',
                        help="Adaptative quality trimming which balances the benefits\n"
                        "of retaining longer reads against the costs of retaining\n"
                        "bases with errors. It can be tuned to be more strict or\n"
                        "tolerant based on the expected downstream use.\n"
                        "Parameters:\n"
                        "-target length : read length which is likely to allow \n"
                        "\t\t the location of the read within the\n"
                        "\t\t target sequence to be determined.\n"
                        "-strictness : value between 0 et 1. A low value (<0.2)\n"
                        "\t      favours longer reads while a high value \n"
                        "\t      (>0.8) favours read correctness.\n"
                        "Both must be specified to enable maxinfo quality trimming.\n"
                        "  Usage: \n"
                        "   -maxinfo <target-length>:<strictness>\n\n")
    
    group.add_argument("-leading",
                        type=int,
                        action='store',
                        help="Removes low quality bases from the beginning of the reads.\n"
                        "As long as a base has a quality value below this \n"
                        "threshold the base is removed until the quality of base\n"
                        "is above this threshold.\n"
                        "  Usage: \n"
                        "   -leading <required-quality>\n\n")
    
    group.add_argument("-trailing",
                        type=int,
                        action='store',
                        help="Removes low quality bases from the end of the reads.\n"
                        "As long as a base has a quality value below this\n"
                        "threshold the base is removed until the quality of base\n"
                        "is above this threshold.\n"
                        "  Usage: \n"
                        "   -leading <required-quality>\n\n")
    
    group.add_argument("-headcrop",
                        type=int,
                        action='store',
                        help="Removes a fixed amount of bases from the beginning of the\n"
                        "reads regardless of quality. \n"
                        "  Usage:\n"
                        "   -headcrop <number>\n\n")
        
    group.add_argument("-crop",
                        type=int,
                        action='store',
                        help="Removes a fixed amount of bases from the end of the read.\n"
                        "regardless of quality.\n"
                        "  Usage:\n"
                        "   -crop <number>\n\n")
    
    group.add_argument("-avgqual",
                        type=int,
                        action='store',
                        help="Drops the read if the average quality is below the\n"
                        "specified level.\n"
                        "  Usage:\n"
                        "   -avgqual <quality>\n\n")

    group.add_argument("-minlen",
                        type=int,
                        action='store',
                        help="Removes reads that fall below the minimum specified. It\n"
                        "normally should be used after all other trimming or\n"
                        "filtering steps.\n"
                        "  Usage:\n"
                        "   -minlen <length>\n\n")

    group.add_argument("-keep-singleton",
                       action='store_const',
                       const='yes',
                       help="Keep files containing reads that have past the filter \n"
                       "but not his partner.\n"
                       "  Usage:\n"
                       "    -keep-singleton\n\n")

    group.add_argument("-compress",
                          type =str,
                       action='store',
                       choices=['.gz','.bz2'],
                       help="Compress output files in zip or bzip2 format.\n"
                       "  Usage:\n"
                       "    -compress .gz || -compress .bz2\n\n")
    
    exclu = group.add_mutually_exclusive_group()
    
    exclu.add_argument("-tophred33",
                        action='store_const',
                        const='TOPHRED33',
                        help="(Re)Encodes phred score of the FASTQ file to phred 33.\n"
                        "  Usage:\n"
                        "   -tophred33\n\n")
    
    exclu.add_argument("-tophred64",
                        action='store_const',
                        const='TOPHRED64',
                        help="(Re)Encodes phred score of the FASTQ file to phred 64.\n"
                        "  Usage:\n"
                        "   -tophred64'\n\n")

    group.add_argument("-fastqc",
                       action='store_const',
                       const='FASTQC',
                       help= "Control quality of raw reads and trimmed reads by FastQC,\n"
                       "a quality control tool for high throughput sequence data.\n"
                       "  Usage:\n"
                       "    -fastqc\n\n")    
    

    return parser



# CHECK ARGUMENTS --------------------------------------------------------------

def check_illuminaclip(text):
    """
    Function that check illuminaclip (adapter trimming) arguments.
    
    Takes one argument :
        text [string] : given argument by user
    
    Returns one argument :
        - 1 [integer] : if argument is confrom
        - or quit, if not
    """
        
    # separates arguments
    illum = text.split(':')
        
    # verify the number of arguments between ':'.
    if not len(illum) == 4:
        sys.exit("/!\ Option illuminaclip must avec 4 elements between ':'")
    
    # get & check fasta file
    ce.check_fasta_file(illum[0])
    
    # check that an integer is entered for seed mismatches
    if not illum[1].isdigit():
        sys.exit("/!\ Value for seed mismatches must be an integer")

    # check that an integer is entered for palindrome clip threshold
    if not illum[2].isdigit():
        sys.exit("/!\ Value for palindrome clip threshold must be an integer")

    # check that an integer is entered for single clip threshold
    if not illum[3].isdigit():
        sys.exit("/!\ Value for simple clip threshold must be an integer")
        
    return 1



def check_slidingwindow(text):
    """
    Function that check slidingwindow (quality trimming) arguments.
    
    Takes one argument :
        text [string] : given argument by user.
    
    Returns one argument :
        - 1 [integer] : if argument is confrom
        - or quit, if not
    """
            
    # separates arguments
    slidw = text.split(':')
        
    # verify the number of arguments between ':'.
    if not len(slidw) == 2 :
        sys.exit("/!\ Option silidingwindow must have 2 elements between ':'")

    # check that an integer is entered for window size
    if not slidw[0].isdigit():
        sys.exit("/!\ Value for window-size (sliding-window) must be an integer")
    
    # check that an integer is entered for required quality
    if not slidw[1].isdigit():
        sys.exit("/!\ Value for required-quality (sliding-window) must be an integer")
    
    return 1
        


def check_maxinfo(text):
    """
    Function that check maxinfo (quality trimming) arguments.
    
    Takes one argument :
        text [string] : given argument by user
    
    Returns one argument :
        - 1 [integer] : if argument is confrom
        - or quit, if not
    """
        
    # separates arguments
    maxinfo = text.split(':')
        
    # verify the number of arguments between ':'.
    if not len(maxinfo) == 2:
        sys.exit("/!\ Option maxinfo must have two elements between ':'")
    
    # check that an integer is entered for targer length
    if not maxinfo[0].isdigit():
        sys.exit("/!\ Value for target-length (maxinfo) must be an integer")

    # convert strictness value into float
    nb = float(maxinfo[1])
    # check if it's between 0 and 1
    if (nb < 0 or nb > 1):
        sys.exit("/!\ Value for strictness must be a float between 0 and 1")
        
    return 1
    


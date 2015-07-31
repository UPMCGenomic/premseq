#! /usr/bin/env python
# -*- coding: utf8 -*-

""" 
commandline.py : module containing all functions to generate command line for
                 Trimmomatic and FastQC.

Dependency : check_entries (personal module)
"""

__author__ = "Anita Annamalé"
__version__  = "1.0"
__copyright__ = "copyleft"
__date__ = "2015/07"


#-------------------------- MODULES IMPORTATION -------------------------------#


import os
import os.path
import re

# Personal module
import check_entries as ce

#-------------------------- FUNCTIONS DEFINITION ------------------------------#


# INPUT / OUTPUT ---------------------------------------------------------------

def commandline_input_output(param, cmd, nb, inout):
    """
    Function that add to 'cmd' the input and output files commandline depending
    on if it's the first or second step of trimming (information given by nb)
    
    Takes 4 arguments :
        - param [dict] : dictionnary containing all parameters
        - cmd [string] : base command line of the programme (trimmomatic)
        - nb [integer] : number of executed trimming command
        - inout [dict] : dictionnary containing all generated files on the 
                        user's computer
    
    Returns two arguments:
        - cmd [string] : the command line with the input and output files
        - inout [dict] : with new files names
    """
    
    # SINGLE-END DATA ----------------------------------------------------------

    if(param['layout'] == 'SE'):
        cmd += ' SE'
        cmd += ' -threads {0}'.format(param['threads'])
        
        # Creating output filename(s) ------------------------------------------
    
        # get input file prefix to create new filename(s)
        prefix = ce.get_file_prefix(param['input'][0])
        trimmed = "{0}/trimmed_{1}.fastq".format(param['output'],prefix)
        
        # add the compression format if choosen
        if 'compress' in param :
            trimmed += "{0}".format(param['compress'])
        

        # Generation of commandline --------------------------------------------
        
        # if it's a the first trimming
        if (nb == 0):
            cmd += ' {0} {1}'.format(param['input'][0], trimmed)
            
            # adding the input and output files to inout
            inout['input'] = param['input']
            inout['trimmed'] = trimmed    
        
        # else step 2 input files are the output files of step 1
        elif (nb == 1):
            cmd += ' {0} {1}'.format(inout['tmp'], trimmed)
        
    
    # PAIRED-END DATA ----------------------------------------------------------

    elif(param['layout'] == 'PE') :
        cmd += ' PE'
        cmd += ' -threads {0} '.format(param['threads'])
        
        # Creating output filename(s) ------------------------------------------

        # get input file prefix to create new filename(s)
        prefix_1 = ce.get_file_prefix(param['input'][0])
        prefix_2 = ce.get_file_prefix(param['input'][1])
        
        trimmed_1 = "{0}/trimmed_{1}.fastq".format(param['output'],prefix_1)
        trimmed_2 = "{0}/trimmed_{1}.fastq".format(param['output'],prefix_2)
        
        single_1 = "{0}/single_{1}.fastq".format(param['output'],prefix_1)
        single_2 = "{0}/single_{1}.fastq".format(param['output'],prefix_2)
        
        
        # add the compression format if choosen
        if 'compress' in param :
            
            trimmed_1 += "{0}".format(param['compress'])
            trimmed_2 += "{0}".format(param['compress'])
            single_1 += "{0}".format(param['compress'])
            single_2 += "{0}".format(param['compress'])
            
        
        # Generation of commandline --------------------------------------------

        # if it's a the first trimming
        if(nb==0):
            cmd += ' {0} {1} {2} {3} {4} {5}'.format(param['input'][0], 
                                                     param['input'][1], 
                                                     trimmed_1, single_1, 
                                                     trimmed_2, single_2)
            
            # adding the input and output files to inout
            inout['input'] = param['input']
            inout['trimmed'] = trimmed_1, trimmed_2
            inout['single'] = single_1, single_2
        
        
        # else step 2 input files are the output files of step 1    
        elif(nb==1):
            cmd += '{0} {1} {2} {3} {4} {5}'.format(inout['tmp'][0],
                                                    inout['tmp'][1],
                                                    trimmed_1, single_1,
                                                    trimmed_2, single_2)
            
    return cmd,inout



def change_output_as_input(inout, param):
    """
    Function that change step1 output files into step2 input files.
    
    Takes 2 arguments :
        - inout [dict] : dictionnary containing all generated files on the 
                        user's working directory
        - param [dict] : dictionnary containing all parameters    
    
    Returns one argument:
        inout [dict] : containing the new files names
    """
        
    # SINGLE-END ---------------------------------------------------------------

    if(param['layout'] == 'SE'):
        
        # Creating temporary filename(s) ---------------------------------------
        
        # get the prefix of the file
        filename = ce.get_file_prefix(param['input'][0])
        
        # new temporary filename
        tmp = '{0}/tmp{1}.fastq'.format(param['output'], filename)
    
        if 'compress' in param:
            tmp += '{0}'.format(param['compress'])
        

        # Rename step 1 trimming file in temporary -----------------------------

        os.rename(inout['trimmed'], tmp)
        

        # Add the temporary file in io -----------------------------------------
        
        inout['tmp'] = tmp
        
        
    # PAIRED-END ---------------------------------------------------------------
    else :
        
        # Creating temporary filename(s) ---------------------------------------

        # get the prefix of files
        filename_1 = ce.get_file_prefix(param['input'][0])
        filename_2 = ce.get_file_prefix(param['input'][1])
        
        # new temporary filenames
        tmp_1 = '{0}/tmp{1}.fastq'.format(param['output'],filename_1)
        tmp_2 = '{0}/tmp{1}.fastq'.format(param['output'],filename_2)
        
        if 'compress' in param:
            tmp_1 += '.{0}'.format(param['compress'])
            tmp_2 += '.{0}'.format(param['compress'])
        

        # Rename step 1 trimming file in temporary -----------------------------
        
        os.rename(inout['trimmed'][0], tmp_1)
        os.rename(inout['trimmed'][1], tmp_2)
        

        # Add the temporary file in io -----------------------------------------
        
        inout['tmp'] = tmp_1, tmp_2
        

        # Delete step1 singleton read files ------------------------------------

        os.remove(inout['single'][0])
        os.remove(inout['single'][1])
    

    return inout    



# FASTQC -----------------------------------------------------------------------

def commandline_fastqc(loc, param, inout):
    """
    Function that generate commandline for FastQC
    
    Takes three arguments :
        - loc [string] : path where Fastqc program is located
        - param [dict] : dictionnary containing all parameters
        - inout [dict] : dictionnary containing all generated filenames

    Returns one argument :
        - cmd [string] : the commandline for fastqc
    """
    
    os.mkdir('{0}/Fastqc'.format(param['output']))

    if param['layout']=='SE':
        cmd = '{0}Utils/FastQC/fastqc {1} {2} \
--outdir {3}/Fastqc \
--quiet \
--extract'.format(loc[:-3], 
                  inout['input'][0], 
                  inout['trimmed'], 
                  param['output'])


    else :
        # check raw and trimmed reads quality
        cmd = '{0}Utils/FastQC/fastqc {1} {2} {3} {4} \
--outdir {5}/Fastqc \
--quiet \
--extract'.format(loc[:-3], 
                  inout['input'][0], 
                  inout['input'][1], 
                  inout['trimmed'][0], 
                  inout['trimmed'][1], 
                  param['output'])
    return cmd


def clean_fastqc_output(param,readfile):
    """
    Function that delete unwanted FastQC output files.

    Takes two arguments :
        - param [dict] : dictionnary containing all parameters
        - readfile [dict] : fastq file used by Fastqc

    Returns one argument :
        - file [dict] : containing quality control information about the readfile
    """

    # Save the working directory
    work_dir = os.getcwd()


    # Delete unwanted files ----------------------------------------------------
    
    # get prefix of readfile to delete unwanted files generated by FastQC
    file_1 = ce.get_file_prefix(readfile)
    
    # delete
    os.remove('{0}/Fastqc/{1}_fastqc.zip'.format(param['output'], file_1))
    os.chdir('{0}/Fastqc/{1}_fastqc'.format(param['output'], file_1))
    os.system('mv ../{0}_fastqc.html .'.format(file_1))
    os.system('rm -r fastqc_report.html fastqc.fo summary.txt Icons')


    # Get Quality control information about readfile ---------------------------

    # regex
    filename_re = re.compile("^Filename\t(.*)")
    encoding_re = re.compile("^Encoding\t(.*)")
    total_seq_re = re.compile("^Total Sequences\t(.*)")
    seq_length_re = re.compile("^Sequence length\t(.*)")
    GC_perc_re = re.compile("^%GC\t(.*)")

    # create a dict
    file1 = {}

    # get information
    with open("fastqc_data.txt", "rt") as f:
        for line in f:
            # filename
            match = filename_re.search(line)
            if match:
                file1['filename'] = match.group(1)
            # encoding
            match = encoding_re.search(line)
            if match:
                file1['encoding'] = match.group(1)
            # total sequences
            match = total_seq_re.search(line)
            if match:
                file1['total_sequence'] = match.group(1)    
            # sequence length
            match = seq_length_re.search(line)
            if match:
                file1['sequence_length'] = match.group(1)
            # percentage GC
            match = GC_perc_re.search(line)
            if match:
                file1['GC_perc'] = match.group(1)
    
    # go back to the working directory
    os.chdir(work_dir)

    return file1


def write_stat_file(dico,param):
    """
    Function that write a file containing statistic of reads before and after 
    trimming.

    Takes two arguments :
        - dico [dict] : dictionnary containing quality control informations
        - param [dict] : dictionnary containing all parameters

    Returns anything.
    """

    with open("{0}/statistic.txt".format(param['output']), "wt") as f:
        f.write("##FastQC    0.11.3\n")
        f.write("Filename\tEncoding\tTotal Sequences\tSequence Length\tGC Percentage\n")
        for files in dico :
            f.write( "{0}\t{1}\t{2}\t{3}\t{4}\n".format(files['filename'], 
                                                        files['encoding'], 
                                                        files['total_sequence'],
                                                        files['sequence_length'],
                                                        files['GC_perc']))



# STEP 1 COMMANDLINE -----------------------------------------------------------

def commandline_step_1(loc,param, nb,inout):
    """
    Function that generate step 1 command line for Trimmomatic.
    
    Takes 4 arguments :
        - loc [string] : path where Trimmomatic program is located
        - param [dict] : dictionnary containing all parameters
        - nb [integer] : number of executed step
        - inout [dict] : dictionnary containing all generated filenames
    
    Returns two arguments:
        - cmd [string] : the commandline for step1
        - inout [dict] : the new filenames generated by step1
    """
    
    # base command line
    cmd = 'java -jar {0}/Utils/trimmomatic-0.33.jar'.format(loc[:-3])
    
    # adding input and output filename
    cmd, inout = commandline_input_output(param, cmd, nb, inout)
    
    # adding adapter trimming parameters
    cmd += ' ILLUMINACLIP:{0}'.format(param['illuminaclip'])
    
    # add compression format if choosen
    if 'tophred33' in param :
        cmd += ' {0}'.format(param['tophred33'])
    
    if 'tophred64' in param :
        cmd += ' {0}'.format(param['tophred64'])    

    return cmd, inout


# STEP 2 COMMANDLINE -----------------------------------------------------------

def commandline_step_2(loc,param, nb, inout):
    """
    Function that generate step 2 command line for Trimmomatic.
    
    Takes 4 arguments :
        - loc [string] : path where Trimmomatic program is located
        - param [dict] : dictionnary containing all parameters
        - nb [integer] : number of executed step
        - inout [dict] : dictionnary containing all generated filenames
    
    Returns one argument :
        - cmd [string] : the commandline for step2
    """
    
    # base command line
    cmd = 'java -jar {0}Utils/trimmomatic-0.33.jar'.format(loc[:-3])
    
    # adding input and output filename
    cmd, inout = commandline_input_output(param,cmd,nb,inout)
    
    # adding quality trimming parameters
    if 'crop' in param :
        cmd += ' CROP:{0}'.format(param['crop'])
        
    if 'headcrop' in param :
        cmd += ' HEADCROP:{0}'.format(param['headcrop'])
    
    if 'leading' in param :
        cmd += ' LEADING:{0}'.format(param['leading'])    
    
    if 'trailing' in param :
        cmd += ' TRAILING:{0}'.format(param['trailing'])    
    
    if 'slidingwindow' in param :
        cmd += ' SLIDINGWINDOW:{0}'.format(param['slidingwindow'])
        
    if 'maxinfo' in param :
        cmd += ' MAXINFO:{0}'.format(param['maxinfo'])        
    
    if 'minlen' in param :
        cmd += ' MINLEN:{0}'.format(param['minlen'])
        
    if 'avgqual' in param :
        cmd += ' AVGQUAL:{0}'.format(param['avgqual'])
        
    # add compression format if choosen
    if 'tophred33' in param :
        cmd += ' {0}'.format(param['tophred33'])
    
    if 'tophred64' in param :
        cmd += ' {0}'.format(param['tophred64'])
            
    return cmd





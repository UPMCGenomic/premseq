#! /usr/bin/env python
# -*- coding: utf8 -*-

""" 
premseq.py : FASTQ trim and filter to remove low-quality base calls from reads. 
It can also remove detrimental artifacts introduced into the reads by the 
sequencing process. It uses Trimmomatic for trimming reads and FastQC to control
read quality before and after trimming. It has two ways of working. 
It can either read trimming information from an XML file, either read directly 
from the command line. Each ways works with 'Single-Ends' (SE) and 
'Paired-Ends' (PE) data.
 
This script need four personal modules to function : parse_xml, parse_args, 
commandline and check_entries"""

__author__ = "Anita Annamalé"
__version__  = "1.0"
__copyright__ = "copyleft"
__date__ = "2015/07"


#-------------------------- MODULES IMPORTATION -------------------------------#

import argparse
import xml.etree.ElementTree as ET
import shlex, subprocess
import os
import sys


# Add /src/ directory to Python path
loc= os.path.dirname(os.path.abspath(__file__)) + "/src"
sys.path.append(loc)

# Personal modules
import parse_args as pa
import parse_xml as px
import commandline as cl
import check_entries as ce


#-------------------------- FUNCTIONS DEFINITION ------------------------------#

if __name__ == '__main__' :

    # Creating premseq parser    
    arg_parser=pa.premseq_parser()    
    
    # Parsing arguments and convert into dictionnary
    arguments = arg_parser.parse_args()
    arguments = dict(arguments._get_kwargs())
    
    # Checking the correct usage of module
    if (len(sys.argv) < 2) or ((len(sys.argv) == 2) & (sys.argv[1] != '-h')):
        sys.exit("Usage : python premseq.py --XML file.xml"
                        " or python premseq.py layout read_files\n"
                "Do python premseq.py -h for more informations.")


    # PARSING PARAMETERS -------------------------------------------------------
    
    if arguments['XML'] != None : 
        # get parameters from xml file

            # parse the xml file
        tree = ET.parse(arguments['XML'])
            # get the root of the tree
        root = tree.getroot()
            # separate sub trees
        in_out, fastqc, trimmo = px.separate_steps(root)
            # separate trimming categories of Trimmomatic
        adapter, quality, useful = px.separate_categories_Trimmo(trimmo)
            # create an empty dict()
        param = dict()
            # fill the dictionnary with trimming parameters
        param = px.get_input_output_parameters(in_out, param)
        param = px.get_fastqc_choice(fastqc,param)
        param = px.get_adapter_parameters(adapter, param)
        param = px.get_quality_parameters(quality, param)
        param = px.get_useful_parameters(useful, param)

    else :
        # get parameters from argparse
        
            # copy arguments [dict]
        param = arguments
        
        
        # CHECK LAYOUT ---------------------------------------------------------
            
        layout = ce.check_layout(param['layout'])
        param['layout'] = layout
        
        
        # CHECK INPUT(s) ACCORDING TO LAYOUT -----------------------------------
        
        # For Single Ends, one input file is expected
        if(layout=='SE'):
        
            if not len(param['input']) == 1 :
                sys.exit("/!\ Only one file containing reads must be given for \
SE data.")

            ce.check_input(param['input'][0], 'for single end data')    
            
        # For Paired Ends, two input files are expected
        else:
            if not len(param['input']) == 2 :
                sys.exit("/!\ Two reads files must be given for PE data.")
    
            for files in param['input']:
                ce.check_input(files, 'for paired end data')
                
                
        # DELETE UNNECESSARY KEYS which have None for value --------------------
        
        for key, value in param.items():
            if value==None:
                del param[key]
        
        
        # CHECK OUTPUT DIRECTORY -----------------------------------------------
        
        if 'output' in param :
            param['output'] = ce.check_output_dir(param['output'])


        # CHECK PARAMETERS -----------------------------------------------------
        
            # check illuminaclip
        if 'illuminaclip' in param :
            pa.check_illuminaclip(param['illuminaclip'])
            
            # check slidingwindow 
        if 'slidingwindow' in param :
            pa.check_slidingwindow(param['slidingwindow'])
            
            # check maxingo
        if 'maxinfo' in param :
            pa.check_maxinfo(param['maxinfo'])
        
        
        # ADD QUALITY to dictionnary if a quality trimming parameter is choosen 
        
        quality=['slidingwindow', 'maxinfo', 'leading', 'trailing',
                 'headcrop', 'crop', 'avgqual', 'minlen', 'tophred33',
                 'tophred64']
    
        for element in quality :
            if element in param:
                param['quality']='yes'
                break



    # INITIALISATION -----------------------------------------------------------

    nb = 0 # number of executed command

    io= dict() # dictionnary wich will contain all created files 
    

    # STEP 1 : ADAPTER TRIMMING ------------------------------------------------

    if 'illuminaclip' in param :

        # Commandline generation
        cmd_step1, io = cl.commandline_step_1(loc,param,nb,io)
        
        # Launch commandline
        args_1 = shlex.split(cmd_step1)
        with open("{0}/step1_output.out".format(param['output']),"wt") as out1:
            prog_1 = subprocess.check_call(args_1, stderr=out1)
        
        # Number of executed commandline becomes 1
        nb = 1
        

    # STEP 2 : QUALITY TRIMMING ------------------------------------------------

    if 'quality' in param :
        

        if(nb==1):    
            # Change step1 output files into step2 input files
            io = cl.change_output_as_input(io, param)

        # Commandline generation
        cmd_step2 = cl.commandline_step_2(loc,param, nb, io)
                
        # Launch commandline
        args_2 = shlex.split(cmd_step2)
        with open("{0}/step2_output.out".format(param['output']),"wt") as out2:
            prog_2 = subprocess.check_call(args_2, stderr=out2)
    

    # DELETE TEMPORARY FILES ---------------------------------------------------

    if 'tmp' in io :

        if param['layout'] == 'SE' :
            os.remove(io['tmp'])
            
        else:
            os.remove(io['tmp'][0])
            os.remove(io['tmp'][1])

    if not 'keep_singleton' in param:
        # Delete singleton read files
        if 'single' in io:
            os.remove(io['single'][0])
            os.remove(io['single'][1])
    

    # STEP 3 : QUALITY CONTROL -------------------------------------------------

    if 'fastqc' in param:

        # Commandline generation
        cmd_step3 = cl.commandline_fastqc(loc, param, io)
            
        # Launch commandline
        args_3 = shlex.split(cmd_step3)
        prog_3 = subprocess.check_call(args_3)

        # DELETE UNNECESSARY FILES
        if arguments['layout'] == 'SE' :
            file_1 = cl.clean_fastqc_output(param,io['input'][0])
            file_2 = cl.clean_fastqc_output(param,io['trimmed'])
            fastqcfiles = [file_1, file_2]
        else :
            file_1 = cl.clean_fastqc_output(param,io['input'][0])
            file_2 = cl.clean_fastqc_output(param,io['input'][1])
            file_3 = cl.clean_fastqc_output(param,io['trimmed'][0])
            file_4 = cl.clean_fastqc_output(param,io['trimmed'][1])
            
            fastqcfiles=[file_1, file_2, file_3, file_4]
        
        # WRITE STATISTIC FILE
        cl.write_stat_file(fastqcfiles,param)


    #  check execution of premseq 
    if ('illuminaclip' not in param) and ('quality' not in param) and ('fastqc' not in param):
        print 'Oops! Nothing have been done, please check the commandline.'
    

#    -------------------------------- END ---------------------------------------

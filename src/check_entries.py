#! /usr/bin/env python
# -*- coding: utf8 -*-

""" 
check_entries.py : module containing all functions that check parameters for 
PREMSEQ
"""

__author__ = "Anita Annamalé"
__version__  = "1.0"
__copyright__ = "copyleft"
__date__ = "2015/07"

#-------------------------- MODULES IMPORTATION -------------------------------#

import xml.etree.ElementTree as ET
import sys
import os.path

#-------------------------- FUNCTIONS DEFINITION ------------------------------#


def check_child_number(tree, number):
    """
    Boolen that checks that the tree have the expected number of child.
    
    Takes two arguments : - tree [ElementTree] : the tree
                          - number [integer] : the expected number of child
    
    Return one argument:
        - 1 [integer] : if the number find is equal to the expected one
        - 0 [integer] : if not
    """
    
    # get the number of child
    nb_child = len(tree.getchildren())
    
    # check if it's equal to the expected one
    if(nb_child == number): 
        return 1
    
    return 0



def empty(text) :
    """
    Function that check if the text is empty or not.
    
    Takes one argument : text [string]
    
    Returns one argument :
        - 1 [integer] : if the text is empty
        - 0 [integer] : if it is not
    """
    # check that the text is none (=empty)
    if (text==None) :
        return 1
    else :
        # remove blank (before and after) from text
        clean_text=text.strip()
    
        # check if there is a text or not
        if bool(clean_text):
            return 0
        else :
            return 1



def check_layout(text) :
    """
    Function that check if the layout isn't empty, and if it's 'PE' or 'SE'.
    
    Takes one argument : text [string] : the layout
    
    Returns one argument :
        - clean_layout [string] : if the layout is conform
        - or quit, if not
    """
    
    if not empty(text):

        # remove bank before and after the text
        clean_layout = text.strip()    

        # upper it
        clean_layout = clean_layout.upper()
        
        # check if it's 'SE' or 'PE'
        if(clean_layout == 'SE' or clean_layout == 'PE') :
            return clean_layout
            
        sys.exit("/!\ Layout can only be 'SE' or 'PE'.")
            
    sys.exit("/!\ You must enter a type of layout for your reads.")



def check_fastq_extension(text):
    """ 
    Booleen that checks if the extension of a input file is '.fastq' or '.fq'.
    
    Takes one argument : text [string]
    
    Returns one argument:
        - 1 [integer] : if it is '.fastq' or '.fq'
        - 0 [integer] : if not
    """
    
    # getting the file extension
    ext = os.path.splitext(text)[1]
    
    if(ext=='.fastq' or ext=='.fq'):        
        return 1
            
    return 0



def check_input(text,location) :
    """
    Function that check that an input file is given, that it exists and that it
    has the right extension
    
    Takes two argument : - text [string]
                         - location [string] : location of the input file
                                                example : 'for SE data'
    
    Returns one argument :
        - clean_input [string] : if file exists and has the right extension
        - or quit, if not 
    """    

    # check that it's not empty
    if not empty(text) :

        # remove blank before and after the text
        clean_input = text.strip()
        
        # check if file exist
        if(os.path.isfile(clean_input)):
            
            # check if the file have fastq extension
            if(check_fastq_extension(clean_input) == 1) : 
                return clean_input
            
            # check if the file is compressed        
                # split the filename    
            ext1 = os.path.splitext(clean_input)
            
            # check the last extension (if compressed)
            if(ext1[1]=='.gz' or ext1[1]=='.bz2'):
                
                # check that the first extension is .fastq or .fq
                if(check_fastq_extension(ext1[0]) == 1) :
                    return clean_input
                    
            sys.exit("/!\ Input files have not the right extension [fastq/fq, \
fastq/fq.bzip2 or fastq/fq.gzip]")    
            
        sys.exit("/!\ Oops, file named '{0}'' did not exist".format(clean_input))
    
    sys.exit("/!\ You must give a fastq file containing all reads %s." %location)    



def check_yes_no(text, location):
    """
    Function that check if the text isn't empty and if it's either 'yes' 
    either 'no'
    
    Takes two arguments : - text [string]     
                           - location [string] : location of text
    
    Returns one argument :
        - clean_text : if it's 'yes' or 'no'
        - or quit, if not
    """    
    
    # check that it's not empty
    if not empty(text) :

        # remove bank before and after the text, and lower it
        clean_text = text.strip()
        clean_text = clean_text.lower()
        
        if(clean_text == 'yes' or clean_text == 'no'):
            return clean_text
            
        sys.exit("/!\ Value for %s can only be 'yes' or 'no'." %location) 
    
    sys.exit("/!\ You haven't enter a text for %s." %location)



def check_fasta_file(text):
    """
    Function that check that a fasta file is given, that it exists and that it
    has the right extension
    
    Takes one arguments : text [string] : the file
    
    Returns one argument :
        - fasta_file : if the file exists and has the right extension
        - or quit, if not
    """    
    
    # check that a file have been given
    if not empty(text):

        # remove blank before and after text
        fasta_file = text.strip()

        # check that file exists
        if(os.path.isfile(fasta_file)):
            
            # check that extension is fata
            ext = os.path.splitext(fasta_file)[1]
    
            if(ext=='.fasta' or ext=='.fa'):        
                return fasta_file
            
            sys.exit("/!\ Given adapter file is not a fasta file.")
        
        sys.exit("/!\ Given adapter file did not exist.")
        
    sys.exit("/!\ You must enter a fasta file containing adapter sequences \
if you want to do adapter trimminig.")



def check_integer(text, location):
    """
    Function that check if the text isn't empty and if it's an integer
    
    Takes two arguments : - text [string] 
                          - location [string] : location of integer
    
    Returns one argument :
        - clean_text : if it's an integer
        - or quit, if not
    """    

    # check that the text is not empty
    if not empty(text):

        # remove blank before and after text
        clean_text=text.strip()
        
        # convert into integer
        clean_text=int(clean_text)
        
        return clean_text
        
    sys.exit("/!\ You haven't enter an integer for %s." %location)



def check_true_false(text, location):
    """
    Function that check if the text isn't empty and is either 'true' either 
    'false'
    
    Takes two arguments : - text [string]     
                          - location [string] : location of text
    
    Returns one argument :
        - clean_text : if it's 'true' or 'false'
        - or quit, if not
    """    
    
    # check if the text is not empty
    if not empty(text):

        # remove blank before and after the text, and lower it
        clean_text = text.strip()
        clean_text = clean_text.lower()
        
        if(clean_text == 'true' or clean_text == 'false'):
            return clean_text
            
        sys.exit("/!\ Value for %s can only be 'true' or 'false'." %location)
        
    sys.exit("/!\ You haven't enter a text for %s." %location)



def check_float(text, location):
    """
    Function that check if the text isn't empty and is a float
    
    Takes two arguments : - text [string]     
                          - location [string] : location of float
    
    Returns one argument :
        - clean_text : if it's a float
        - or quit, if not
    """        
    
    # check that the text is not empty
    if not empty(text):

        # remove blank before and after the text
        clean_text=text.strip()

        # convert into float
        clean_text=float(clean_text)
        
        return clean_text
        
    sys.exit("/!\ You haven't enter a float for %s." %location)



def get_file_prefix(text):
    """
    Function that gets the prefix of a file without all extensions.
    
    Takes one argument : text [string]
    
    Returns one argument : prefix [string]
    """

    # get the basename of the file
    prefix = os.path.basename(text)

    # get the prefix if it's a non compressed fastq file
    prefix = os.path.splitext(prefix)[0]
    
    # get the prefix if it's a compressed fastq file
    if not(check_fastq_extension(text)) : 
        prefix = os.path.splitext(prefix)[0]
        
    return prefix



def check_xml_file(text):
    """
    Function that check if the given file is an xml and if it exists.
    
    Takes one argument : text [string] : the file
    
    Returns one argument :
        - 1 : if the xml file exists.
        - or quit, if not
    """    

    # check that file exist
    if(os.path.isfile(text)):
            
        # check extension is xml
        ext = os.path.splitext(text)[1]
        
        if(ext=='.xml'):        
            return 1
            
        sys.exit("/!\ Given file is not an xml file\n")
            
    sys.exit("/!\ Given file did not exist \n")



def check_output_dir(text):
    """
    Function that check that a output directory is given, that it exists, if not
    create it

    Takes one argument : text [string] : path to the directory

    Returns one argument : text [string] : clean directory path
    """

    # check that the text is not empty 
    if not empty(text):

        # remove blank before and after the text
        clean_text = text.strip()

        # remove '/' if it exist and return the clean text
        if (clean_text[-1] == '/'):
            clean_text = clean_text[:-1]

        # if the directory did not exist create it
        if not (os.path.isdir(clean_text)):
            os.mkdir(clean_text)
        
        return clean_text

    sys.exit("/!\ You must enter a 'output-directory' where the new output will\
 be written")

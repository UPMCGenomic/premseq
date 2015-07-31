#! /usr/bin/env python
# -*- coding: utf8 -*-

"""
parse_xml.py : module containing all functions to parse a XML file.

Dependency : check_entries (personal module)
"""

__author__ = "Anita Annamalé"
__version__  = "1.0"
__copyright__ = "copyleft"
__date__ = "2015/07"

#-------------------------- MODULES IMPORTATION -------------------------------#


import xml.etree.ElementTree as ET
import sys

# Personal module
import check_entries as ce


#-------------------------- FUNCTIONS DEFINITION ------------------------------#


# SEPARTATE STEPS --------------------------------------------------------------

def separate_steps(root):
    """
    Function that separate different steps (Inputs/Outputs and different Programs).
    
    Takes one argument : root [ElementTree] : the root of the tree
    
    Returns three arguments :
        - Puts [ElementTree] : subtree which contains inputs and outputs 
          information's
        - Fastqc [ElementTree] : subtree which contains quality control 
          information's
        - Trimmomatic [ElementTree] : subtree which contains Trimmomatic 
          program parameters
    """
    
    # check that the root have 3 child
    if not ce.check_child_number(root,3) :
        sys.exit("/!\ Warning : The XML file must contain exactly one Input and\
 Output section and two programs (FastQC & Trimmomatic)")
    
    # separte the different steps    
    for element in root :
        
        if(element.tag == 'input-output') :
            Puts = element
        
        elif(element.get('name')=='fastqc') :
            Fastqc = element
            
        elif(element.get('name')=='trimmomatic') :
            Trimmomatic=element
        
        else:
            sys.exit("/!\ Oops! Atleast the name of the section 'input-output' \
or one of program names (fastqc of trimmomatic) have been modified")
    
    return Puts, Fastqc, Trimmomatic



# INPUT / OUTPUT INFORMATION ---------------------------------------------------

def get_input_output_parameters(Puts, param):
    """
    Function that gets inputs and outputs parameters
    
    Takes two arguments : - Puts [ElementTree] : subtree which contains inputs 
                            and outputs information's
                          - param [dict] : dictionnary containing all 
                            parameters
    
    Returns param[dict] where have been added inputs and outputs parameters
    """
    
    # check if the section 'input-output' contains 4 parameters
    if not check_child_number(Puts,4):
        sys.exit("/!\ Warning : The XML file must contain exactly 4 parameters \
in the section 'input-output'!")
    

    # LAYOUT -------------------------------------------------------------------
    
    # get the layout text
    layout = Puts.find('layout').text

    # check that the layout is not empty and is 'SE' or 'PE'
    layout = ce.check_layout(layout)
    
    # add the layout to the dictionnary
    param['layout'] = layout
    

    # INPUTS -------------------------------------------------------------------

    # get input(s)

    if(checked_layout == 'SE') :

        # get the subtree which contain SE input and get the input file
        SE = Puts.find('single-ends')
        filename=SE.find('input').text    
        
        # check if the file exists
        filename = ce.check_input(filename, 'for single-end data')
        
        # add the checked input file
        param['input'] = filename
        
    else:
        # get the subtree which contain PE input
        PE = Puts.find('paired-ends')
        
        # get input files
        for filename in PE.findall('input') :
        
            if(filename.get('name') == 'read 1') :
                
                # check the input file for read 1
                Read1 = ce.check_input(filename.text, 'reads 1 for paired-end data')
                
            elif(filename.get('name') == 'read 2') :
                
                # check the input file for read 2
                Read2 = ce.check_input(filename.text, 'reads 2 for paired-end data')
            
            else :
                sys.exit("/!\ The value of 'name' in paired-end section have been \
modified")
        
        # add the checked input files 
        param['input']= Read1, Read2
        

    # OUTPUTS ------------------------------------------------------------------    
    
    # get the working-directory where the new files must be generated
    directory = Puts.find('output-directory').text
    
    # check that output-directory is given and if it exists
    directory =  ce.check_output_dir(directory)

    # add into the dictionnary
    param['output']= directory

    return param



# FASTQC -----------------------------------------------------------------------

def get_fastqc_choice(Fastqc, param):
    """
    Function that gets the choice of controling quality of raw input and 
    filtered data by FastQC.
    
    Takes two arguments : - Fastqc [ElementTree] : subtree which contains the 
                                                   choice of the user to do or 
                                                   not a quality control
                          - param [dict] : dictionnary containing all parameters
    
    Returns param[dict] where the choice for FastQC have been added
    """
    
    # check that the section Fastqc contains only a skip option
    if not ce.check_child_number(Fastqc,1):
        sys.exit("/!\ The XML file must contain only a skip option in the \
section 'fastqc'!")
    
    # get skip option text    
    skip = Fastqc.find('skip').text
    
    # check if it's not empty and either 'yes' or 'no'
    skip = ce.check_yes_no(skip, 'skip in fastqc')
    
    # if skip = 'no' add to param [dict]
    if(skip == 'no') :
        param['fastqc']='yes'
    
    return param



# TRIMMOMATIC ------------------------------------------------------------------

    # SEPARATE CATEGORIES ------------------------------------------------------

def separate_categories_Trimmo(Trimmomatic):
    """
    Function that separates the subtree (Trimmomatic program) according to 
    categories.
    
    Takes one argument : Trimmomatic [ElementTree]
    
    Returns four arguments :
        - Adapter [ElementTree] : subtree which contains adapter trimming 
        parameters
        - Quality [ElementTree] : subtree which contains quality trimming 
        parameters
        - Useful [ElementTree] : subtree which contains uselful parameters
    """
    
    # check that the number of categories is 3   
    if not ce.check_child_number(Trimmomatic,3) : 
        sys.exit("/!\ The XML file must contain exactly 3 categories for \
Trimmomatic!")
    
    # separates categories of Trimmomatic
    for category in Trimmomatic :
        
        # get parameters for 'Adapter-Trimming' in a subtree
        if(category.get('name') == 'adapter-trimming') :
            Adapter = category
            continue
        
        # get parameters for 'Quality-Trimming' in a subtree
        elif(category.get('name') == 'quality-trimming') : 
            Quality = category
            continue
            
        # get parameters for 'Usefull-Parameters' in a subtree
        elif(category.get('name') == 'useful-parameters') :
            Useful = category
            continue
        
        else :
            sys.exit("/!\ Atleast one category haven't been recognized.\n\
Please, have a look at the name of Trimmomatic categories, atleast one of them \
have been modified.")
    
    return Adapter, Quality, Useful



    # GET ADAPTER TRIMMING PARAMETERS ------------------------------------------

def get_adapter_parameters(Adapter, param):
    """
    Function that gets adapter trimming parameters
    
    Takes two arguments:
        - Adapter [ElementTree] : subtree which contains adapter trimming 
          parameters
        - param [dict] : dictionnary containing all parameters
        
    Returns param [dict] with added adapter trimming parameters
    """
    
    # check adapter section have 2 child (skip and parameters)
    if not ce.check_child_number(Adapter,2):
            sys.exit("/!\ Warning : The XML file must contain exactly 1 skip \
option and 1 parameter for adapter trimming.")
    

    # SKIP ---------------------------------------------------------------------

    # get the skip option text
    skip = Adapter.find('skip').text
    
    # checking if it's not empty and either yes either no
    skip = ce.check_yes_no(skip, 'skip in adapter trimming')
    

    # PARAMETERS ---------------------------------------------------------------
    
    # if skip = 'no' get parameters
    if(skip == 'no') :
        
        # getting the subtree parameter
        parameter = Adapter.find('parameter')
        
        # get parameter which name is 'illuminaclip'
        if(parameter.get('name')=='illuminaclip') :
            
            Clip = parameter
            
            # get obligatory parameters ----------------------------------------

            fasta_file = ce.check_fasta_file(Clip.find('adapters-fasta-file').text)
            
            mismatches = ce.check_integer(Clip.find('seed-mismatches').text, 
                                         'mismatches in illuminaclip')

            P_thres = ce.check_integer(Clip.find('palindrome-clip-threshold').text,
                                    'palindrome clip threshold in illuminaclip')

            S_thres = ce.check_integer(Clip.find('simple-clip-threshold').text,
                                      'simple clip threshold in illuminaclip')
            
            # optional parameters ----------------------------------------------
            

                # min-adapter-length
            minlen = Clip.find('min-adapter-length')    

            # get min-adapter-length skip value        
            minlen_skip = ce.check_yes_no(minlen.find('skip').text, 
                                  'min-adapter-length skip in adapter trimming')
            
            if(minlen_skip == 'no') :
                min_length = ce.check_integer(minlen.find('value').text, 
                                       'min-adapter-length in adapter trimming')
            else :
                min_length = 8 # default value
            

                # get keep-both-reads value 
            keepreads = Clip.find('keep-both-reads')
        
            # get keep-both-reads skip value
            keepreads_skip = ce.check_yes_no(keepreads.find('skip').text, 
                                     'keep-both-reads skip in adapter trimming')
            
            if(keepreads_skip == 'no'):
                keep = ce.check_true_false(keepreads.find('value').text,
                                          'keep-both-reads in adapter trimming')
            else:
                keep = 'true' # default value
            
            # Add all parameters to dictionnary --------------------------------

            param['illuminaclip']="{0}:{1}:{2}:{3}:{4}:{5}".format(fasta_file,
                                                           mismatches,P_thres,
                                                           S_thres,min_length,
                                                           keep)
            
        # if parameter name is not 'illuminaclip'
        else :
            sys.exit("/!\ Name of parameter 'illuminaclip' have been modified or\
 replaced by something else. Please rename it 'illuminaclip'")
            
    return param 



def get_quality_parameters(Quality, param) :
    """
    Function that gets quality trimming parameters.
    
    Takes 2 arguments:
        - Quality [ElementTree] : subtree which contains quality trimming 
          parameters
        - param [dict] : dictionnary containing all parameters
        
    Returns param [dict] with added quality trimming parameters
    """
    
    # check that quality trimming subtree have 9 child (skip and 9 parameters)
    if not ce.check_child_number(Quality,9) :
            sys.exit("/!\ The XML file must contain exactly one skip option \
skip and 8 parameters for quality trimming.")
    

    # SKIP ---------------------------------------------------------------------

    # get the skip option text
    skip = Quality.find('skip').text

    # check that it is not empty and either 'yes' either 'no'
    skip = ce.check_yes_no(skip, 'skip in quality trimming')
    

    # PARAMETERS ---------------------------------------------------------------

    # getting the parameters if skip = no
    if(skip == 'no'):
        
        param['quality']='yes'
        
        for parameter in Quality.findall('parameter'):
            
            # get and check the skip option for each parameter
            param_skip = ce.check_yes_no(parameter.find('skip').text, 
                       'skip in %s from quality trimming'%parameter.get('name'))
            
            # if skip = no, get parameter arguments and add to dict
            if(param_skip == 'no'):
                
                # SLIDING-WINDOW -----------------------------------------------
                
                if(parameter.get('name') == 'sliding-window'):

                    SW_size = ce.check_integer(parameter.find('window-length').text,
                                     'window length in sliding window trimming')
                    SW_quality = ce.check_integer(parameter.find('required-quality').text,
                                 'required-quality for sliding window trimming')
                    
                    param['slidingwindow'] = '{0}:{1}'.format(SW_size,SW_quality)
                    continue
                

                # MAXINFO ------------------------------------------------------

                elif(parameter.get('name')== 'maxinfo'):
                    
                    MI_length = ce.check_integer(parameter.find('target-length').text,
                                    'target-length in maxinfo quality trimming')
                    MI_strictness = ce.check_float(parameter.find('strictness').text,
                                       'strictness in maxinfo quality trimming')
                    
                    param['maxinfo'] = '{0}:{1}'.format(MI_length, MI_strictness)
                    continue
                

                # LEADING ------------------------------------------------------

                elif(parameter.get('name') == 'leading'):
                
                    lead_quality = ce.check_integer(parameter.find('required-quality').text,
                               "required-quality in 'leading' quality trimming")
                    
                    param['leading'] = lead_quality
                    continue
                

                # TRAILING -----------------------------------------------------

                elif(parameter.get('name') == 'trailing'):
                    
                    tail_quality = ce.check_integer(parameter.find('required-quality').text,
                              "required-quality in 'trailing' quality trimming")
                    
                    param['trailing'] = tail_quality
                    continue
                

                # CROP ---------------------------------------------------------

                elif(parameter.get('name') == 'crop'):
                    crop_length = ce.check_integer(parameter.find('length').text,
                                            "length in 'crop' quality trimming")
                    
                    param['crop'] = crop_length
                    continue
                

                # HEADCROP -----------------------------------------------------

                elif(parameter.get('name') == 'headcrop'):
                    headcrop_length = ce.check_integer(parameter.find('length').text,
                                        "length in 'headcrop' quality trimming")
                    
                    param['headcrop'] = headcrop_length
                    continue    
                    

                # MINLEN -------------------------------------------------------

                elif(parameter.get('name') == 'minlen'):
                    min_len = ce.check_integer(parameter.find('length').text,
                                          "length in 'minlen' quality trimming")
                    
                    param['minlen'] = min_len
                    continue
                

                # AVERAGE-QUALITY ----------------------------------------------

                elif(parameter.get('name') == 'average-quality'):
                    avg_qual = ce.check_integer(parameter.find('required-quality').text,
                               "required-quality in 'average quality' trimming")
                    
                    param['avgqual'] = avg_qual
                    continue
                
                else :
                    sys.exit("/!\ You have modified a quality trimming parameter\
 name or enter a new one which have not been recognized")
            
    return param



def get_useful_parameters(Useful, param) :
    """
    Function that gets useful parameters.
    
    Takes two arguments:
        - Useful [ElementTree] : subtree which contains useful parameters
        - param [dict] : dictionnary containing all parameters
        
    Returns param [dict] with added quality trimming parameters
    """
    
    # check that useful parameter have 4 child
    if not ce.check_child_number(Useful,4):
        sys.exit("/!\ The XML file must contain exactly 4 useful parameters.")
        

    # PARAMETERS ---------------------------------------------------------------
    
    for parameter in Useful.findall('parameter') :
        
        # SINGLETON-READS ------------------------------------------------------

        if(parameter.get('name') == 'singleton-reads'):
            
            # check if text for show is not empty and either yes or no
            show = ce.check_yes_no(parameter.find('show').text, 
                               'show in singleton-reads from useful-parameters')
            
            # if show = yes, then add to the dict
            if(show == 'yes'):
                param['keep_singleton'] = 'yes'
            continue
            

        # CONVERT-TO-PHRED -----------------------------------------------------

        elif(parameter.get('name') == 'convert-to-phred') :
            
            # get and check if skip text is not empty and if it's yes or no
            skip = ce.check_yes_no(parameter.find('skip').text, 
                              'skip in convert-to-phred from useful parameters')
            
            if(skip == 'no'): 
                # get parameter
                format_num = ce.check_integer(parameter.find('format').text,
                             'format in convert-to-phred in useful parameters.')
                
                # if format is phred33 or phred64, add to the dict
                if(format_num == 33):
                    param['tophred33'] = 'TOPHRED33'
                elif(format_num == 64):
                    param['tophred64'] = "TOPHRED64"
                else :
                    sys.exit("/!\ Quality score can only be converted to \
phred33 or phred64.")
                    
              
        # THREADS --------------------------------------------------------------      
        
        elif (parameter.get('name') == 'threads') :

            # get number of threads
            number = ce.check_integer(parameter.find('number').text, 
                                  'number in threads in useful parameters.')
            
            param['threads'] = number
            continue
            
            
        # COMPRESSION ----------------------------------------------------------

        elif(parameter.get('name') == 'compressed-output'):
            
            # get and check if skip text is not empty and if it's yes or no
            skip = ce.check_yes_no(parameter.find('skip').text,
                            'skip in compressed-output from useful parameters.')
            
            if(skip == 'no') :
                
                # get compression format
                format = parameter.find('format').text
                
                # check if the text is not empty and lower it
                if not empty(format) :
                    format = format.strip()
                    format = format.lower()

                    if(format == '.bz2' or format == '.gz'):
                        param['compress'] = format

                    sys.exit("/!\ Value for format in compressed-output in \
useful parameters can only be 'bz2' or 'gz'.")

                sys.exit("/!\ You haven't enter a text for format in \
compressed-output in useful parameters.")

                continue
                
        else :
            sys.exit("You have modified a useful parameter name or enter a new \
one which have not been recognized\n")
            
    return param

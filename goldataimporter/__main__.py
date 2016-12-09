# # # # #
# Project: GOLDataImporter
# File:
# Created by: Nathan Healea
# Date: 12/8/16
# Description:
# # # # #
import os
import sys
import yaml
from lib import TurningParser
import pickle as pic
from lib import RosterParser




def main(argv):
    validateSetup()
    validateCommands(argv)
    pass
# # # # # # # # # # # # # # # # # # # # # #
#           Helper Functions
# # # # # # # # # # # # # # # # # # # # # #

# #
# Validates that the correct setup information exist
def validateSetup():
    config_file = '/config.yml'
    config = None

    # checking for config file
    if (os.path.exists(os.path.abspath(PROJECT_PATH + config_file)) == 0):
        print "ERROR: configfile not found"
        print os.path.abspath(PROJECT_PATH + config_file)
        exit()
    else:
        # Load in config file
        with open(os.path.abspath(PROJECT_PATH + config_file), 'r') as ymlfile:
            config = yaml.load(ymlfile)

    # Check directory
    for dir in config['directory']:
        if os.path.exists(PROJECT_PATH + config['directory'][dir]) == 0:
            os.makedirs( PROJECT_PATH + config['directory'][dir])
    
    pass
            
# #
# Validates command augments
#
def validateCommands(argv):
    arguments = {
        'path' : None,
        'flag' : None,
        'output': 'default'
    }
    
    # Check for too few argument
    if len(argv) < 2:
        print "ERROR: Incorrect arguments"
        usage()
        exit()
    
    # Checking for to many arguments
    if len(argv) > 3:
        print "ERROR: Too many arguments"
        usage()
        exit()
    
    # Check flags
    if  argv[1] != '-s' and  argv[1] != '-f':
        print "ERROR: incorrect flag"
        usage()
        exit()
    else:
        arguments['flag'] = argv[1]
            
    # Check path
    if (os.path.exists(os.path.abspath(argv[0])) == 0):
        print "ERROR: parsing path not found"
        usage()
        exit()
    else:
        arguments['path'] = os.path.abspath(argv[0])
        
    if len(argv) == 3:
        if(os.path.exists(os.path.abspath(argv[2])) == 0):
            print "ERROR: output path not found using default"
            arguments['output'] = os.path.abspath(CONFIG['directory']['output'])
        else:
            arguments['output'] = os.path.abspath(argv[2])
        
    
    
    print arguments
    return
        


# #
# Display usage of the GOLDataImporter
#
def usage():
    print '''usage: ./goldataimporter <directory> [-f] [-s] [output]
        directory:  relative path to GOL data
           output:  relative path to directory where finished data will be saved
               -f:  parsing full research data
               -s:  parsing a directory of research data'''


if __name__ == '__main__':
    global SCRIPT_PATH
    global PROJECT_PATH
    global CONFIG
    
    # setting globals
    SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))
    PROJECT_PATH = os.path.abspath(os.curdir)
    
    print SCRIPT_PATH
    print PROJECT_PATH
    
    main(sys.argv[1:])
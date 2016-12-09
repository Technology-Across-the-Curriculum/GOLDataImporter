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




def main(excitable, *argv):
    validate()
    pass
# # # # # # # # # # # # # # # # # # # # # #
#           Helper Functions
# # # # # # # # # # # # # # # # # # # # # #

# #
# Validates comands entered by user
#
def validate(argv):
    command = {
        'path' : None,
        'flag' : None
    }
    print argv
    
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
    if argv[1] == '-s':
        command['flag'] = '-s'
    elif argv[1] == 'f':
        command['flag'] = '-f'
    else:
        print "ERROR: incorrect flag \n"
        print argv[0]
        usage()
        exit()

        
    # Checking path
    if (os.path.exists(argv[0]) == 0):
        print "ERROR: parsing path not found\n"
        print argv[0]
        usage()
        exit()
        


# #
# Display usage of the GOLDataImporter
#
def usage():
    print '''usage: goldataimporter.py <directory> [-f] [-s] [output]
        directory:  relative path to GOL data
           output:  relative path to directory where finished data will be saved
               -f:  parsing full research data
               -s:  parsing a directory of research data'''


if __name__ == '__main__':
    main(sys.argv)
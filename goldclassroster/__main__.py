# # # # #
# Project: GOLDClassRoster
# File:
# Created by: Nathan Healea
# Date: 4/27/17
# Description:
# # # # #
import os
import sys
import yaml
import warnings
from lib import RosterValidator
import pickle

# #
#
# #
def main(argv):
    # validating program before execution
    validateSetup()
    validateCommands(argv)

    print PROJECT_PATH
    # Calling loop depending on flag
    if ARGUMENTS['flag'] == '-f':
        fullData()

    if ARGUMENTS['flag'] == '-s':
        singleData()

    pass

def singleData():
    rval = RosterValidator()
    rval.open(ARGUMENTS['path'])
    rval.parse('C')
    rval.parse('G')
    rval.compair()
    rval.record()
    rval.close()
    pass

def fullData():
    # processed files
    filesMatched = 0
    directoryCount = 0
	# Gathering terms
    terms = os.listdir(ARGUMENTS['path'])
    terms = removeFiles(terms)  # Only getting term directories

    # term loop
    for term in terms:

        # Setting path for the current term
        term_path = ARGUMENTS['path'] + '/' + term


        rval = RosterValidator()

        # Getting classes in the term
        classes = os.listdir(term_path)
        classes = removeFiles(classes)  # Only getting class directories

        # counting directories
        directoryCount += len(classes)

        # course loop
        for courseDir in classes:
            class_path = term_path + '/' + courseDir
            classFiles = removeFiles(os.listdir(class_path))

            for file in classFiles:
                if 'session' not in file:

                    rval.open(class_path + '/' + file)
                    print "  |-- Opened: " + file

                    print "    |-- Parsing C"
                    rval.parse('C')
                    
                    print "    |-- Parsing G"
                    rval.parse('G')

                    print "    |-- Compairing GC"
                    rval.compair()
                    
                    print "    |-- Recording Matches"
                    rval.record()
                    

                    rval.close()
                    print "  |-- Closed: " + file

                    filesMatched += 1
    print "  |-- Num Course Directories : " + str(directoryCount)
    print "  |-- Num File Processed: " + str(filesMatched)
    pass

# # # # # # # # # # # # # # # # # # # # # #
#           Helper Functions
# # # # # # # # # # # # # # # # # # # # # #

# #
# Validates that the correct setup information exist
def validateSetup():
    # Defining variables
    global CONFIG
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
            os.makedirs(PROJECT_PATH + config['directory'][dir])

    CONFIG = config
    pass


# #
# Validates command augments
# #
def validateCommands(argv):
    # Defining variables
    global ARGUMENTS
    arguments = {
        'path': None,
        'flag': None,
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
    if argv[1] != '-f' and argv[1] != '-s':
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
        if (os.path.exists(os.path.abspath(argv[2])) == 0):
            print "ERROR: output path not found using default"
            arguments['output'] = os.path.abspath(CONFIG['directory']['output'])
        else:
            arguments['output'] = os.path.abspath(argv[2])

    ARGUMENTS = arguments
    pass

# #
# Removes files from list
def removeFiles(list):
    newList = []

    for element in list:
        exist = False
        for ignoreFile in CONFIG['ignore']:
            if CONFIG['ignore'][ignoreFile] in element:
                exist = True
                break
        if not exist:
            newList.append(element)

    return newList


# #
# Display usage of the GOLDClasslist
# #
def usage():
    print '''usage: ./goldclasslist <directory> [-d] [-s]
        directory:  relative path to GOL data
               -f:  merges all GC.xml file in directory
               -s:  merges a single GC.xml file'''


# # # # # # # # # # # # # # # # # # # # # #
#      Main call function for program
# # # # # # # # # # # # # # # # # # # # # #
if __name__ == '__main__':
    # Defining Global variables for program
    global SCRIPT_PATH
    global PROJECT_PATH
    global CONFIG
    global ARGUMENTS

    CONFIG = None
    ARGUMENTS = None

    # setting globals
    SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))
    PROJECT_PATH = os.path.abspath(os.curdir)

    # calling main loop
    main(sys.argv[1:])
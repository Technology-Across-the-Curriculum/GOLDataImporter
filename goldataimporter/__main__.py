# # # # #
# Project: GOLDataParser
# File:
# Created by: Nathan Healea
# Date: 12/8/16
# Description:
# # # # #
import os
import sys
import yaml
import pickle as pic
from lib import dbconnector as DBConnector


# #
#
# #
def main(argv):
    # validating program before execution
    validateSetup()
    validateCommands(argv)


    pass


# # # # # # # # # # # # # # # # # # # # # #
#           Options Functions
# # # # # # # # # # # # # # # # # # # # # #




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
    if len(argv) < 1:
        print "ERROR: Incorrect arguments"
        usage()
        exit()

    # Checking for to many arguments
    if len(argv) > 3:
        print "ERROR: Too many arguments"
        usage()
        exit()

    # Check flags
    if len(argv) == 2:
        if argv[1] != '-c':
            print "ERROR: incorrect flag"
            usage()
            exit()
        else:
            arguments['consent'] = argv[1]

    # Check flags
    if len(argv) == 3:
        if argv[1] != '-di':
            print "ERROR: incorrect flag"
            usage()
            exit()
        else:
            arguments['deidentified'] = argv[1]

    # Check path
    if (os.path.exists(os.path.abspath(argv[0])) == 0):
        print "ERROR: parsing path not found"
        usage()
        exit()
    else:
        arguments['path'] = os.path.abspath(argv[0])


    ARGUMENTS = arguments
    pass


# #
# Removes files from list
# #
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
# Display usage of the GOLDataImporter
# #
def usage():
    print '''usage: ./goldataimporter <directory> [-c] [-di]
        directory:  relative path to GOL data parced object files
               -c:  only import concenters
              -di:  de-identify on import'''


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

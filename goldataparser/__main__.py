# # # # #
# Project: GOLDataParser
# File:
# Created by: Nathan Healea
# Date: 12/8/16
# Description:
# # # # #
import os
import pickle as pic
import sys

import yaml

from lib import RosterParser
from lib import TurningParser


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
        signleData()

    pass


# # # # # # # # # # # # # # # # # # # # # #
#           Options Functions
# # # # # # # # # # # # # # # # # # # # # #

def signleData():
    # Creating objects
    tp = TurningParser()
    rp = RosterParser()

    # Setting variables
    class_path = ARGUMENTS['path']
    classFiles = removeFiles(os.listdir(class_path))

    # Creating course object
    course = createCourse(os.path.basename(os.path.normpath(ARGUMENTS['path'])))

    # parsing section information
    course['section'] = tp.getSection(course['directory'])
    print(" |-- Section: Parsing information")

    # Check if directory had session files
    if 'sessions' in classFiles:
        tp.setPath(class_path + '/sessions')
        # Store course session and participation list
        course['session'], course[
            'participationlist'] = tp.parse()
    else:
        print "  |-- Session: ERROR no session files found"

    # Check if a Grade/Concent file exist
    if '.xlsx' in classFiles[0]:
        rp.open(class_path + '/' + classFiles[0])
        course['classlist'] = rp.parse()
        rp.close()
        print "  |-- Courselist: Parsed"

    # Matching Students
    matchStudents(course)
    print "  |-- Match: Complete"

    # Saving Course Informaion
    saveCourse(course)
    print "  |-- Coure Saved: Complete"


# #
# Recursive iterates through all terms and terms classes in the research data
# #
def fullData():
    # Gathering terms
    terms = os.listdir(ARGUMENTS['path'])
    terms = removeFiles(terms)  # Only getting term directories

    # term loop
    for term in terms:

        # Setting path for the current term
        term_path = ARGUMENTS['path'] + '/' + term

        # Creating Objects
        tp = TurningParser()
        rp = RosterParser()

        # Getting classes in the term
        classes = os.listdir(term_path)
        classes = removeFiles(classes)  # Only getting class directories

        # course loop
        for courseDir in classes:
            class_path = term_path + '/' + courseDir
            classFiles = removeFiles(os.listdir(class_path))

            # Creating Course object
            course = createCourse(courseDir)

            # parsing section information
            course['section'] = tp.getSection(course['directory'])
            print(" |-- Section: Parsing information")

            # Check if directory had session files
            if 'sessions' in classFiles:
                tp.setPath(class_path + '/sessions')

                # Store course session and participation list
                course['session'], course[
                    'participationlist'] = tp.parse()
            else:
                print "  |-- Session: ERROR no session files found"

            # Check if a Grade/Concent file exist
            if '.xlsx' in classFiles[0]:
                rp.open(class_path + '/' + classFiles[0])
                course['classlist'] = rp.parse()
                rp.close()
                print "  |-- Courselist: Parsed"

            # Matching Students
            matches = matchStudents(course)
            print "  |-- Match: Complete"
            print "    |-- Num Match:{0}".format(matches)

            # Saving Course Information
            saveCourse(course)
            print "  |-- Coure Saved: Complete"


# #
# Creates a course object that will hold all parsed information
# #
def createCourse(directoryName):
    # variables
    directoryInfo = directoryName.split('_')  # directory name split

    print("Current Directory: %s") % (directoryName)

    # creating course object
    course = {}
    course['acronym'] = directoryInfo[3]
    course['directory'] = directoryName
    course['section'] = {}  # dictionary for section information
    course['session'] = []  # array of section objects
    course['classlist'] = []  # array of students from Consent/Grade list
    course['participationlist'] = []  # array of participants from session files

    return course


# #
# Saves the course object once it all
def saveCourse(couseObj):
    if ARGUMENTS['output'] != 'default':
        pic.dump(couseObj, open(
            os.path.abspath(ARGUMENTS['output'] + '/' + couseObj[
                'directory'] + '.obj',
                            "wb")))
    else:
        pic.dump(couseObj, open(
            os.path.abspath(str(
                PROJECT_PATH + CONFIG['directory']['output'] + '/' + couseObj[
                    'directory'] + '.obj')),
            "wb"))


# #
# Creats matchs between course['classlist'] and course ['participationlist']
# #
def matchStudents(course):
    matchFound= 0
    for student_c in course['classlist']:

        for student_p in course['participationlist']:
            if student_c['firstname'] == student_p['firstname'] and student_c[
                'lastname'] == student_p['lastname']:
                matchFound += 1
                for key, value in student_p.iteritems():
                    if not hasattr(student_c, key):
                        student_c[key] = value
                if student_c['consent'] != 1:
                    student_c['consent'] = 0
            elif ('email' in student_c) and ('email' in student_p):
                c_email = False
                p_email = False


                if student_c['email'] is not None:
                    c_email = student_c['email'].split('@')
                if student_p['email'] is not None:
                    p_email = student_p['email'].split('@')

                if c_email and p_email:
                    if c_email[0] == p_email[0] :
                        matchFound += 1
                        for key, value in student_p.iteritems():
                            if not hasattr(student_c, key):
                                student_c[key] = value
                        if student_c['consent'] != 1:
                            student_c['consent'] = 0

        
    return matchFound

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
    if argv[1] != '-s' and argv[1] != '-f':
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
    print '''usage: ./goldataimporter <directory> [-f] [-s] [output]
        directory:  relative path to GOL data
           output:  relative path to directory where finished data will be saved
               -f:  parsing full research data
               -s:  parsing a directory of research data'''


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

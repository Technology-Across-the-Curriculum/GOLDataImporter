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
from lib import TurningParser
from lib import RosterParser


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
    class_path = ARGUMENTS['path']
    classFiles = removeFiles(os.listdir(class_path))
    # Creating Cousre object
    course = createCourse(os.path.basename(os.path.normpath(ARGUMENTS['path'])))

    # Check if directory had session files
    if 'sessions' in classFiles:
        tp = TurningParser()
        tp.setPath(class_path + '/sessions')

        # Store course session and participation list
        course['session'], course[
            'participationlist'] = tp.parse()
    else:
        print "ERROR: no session files found, Course ignored"
        pass

    # Check if a Grade/Concent file exist
    if '.xlsx' in classFiles[0]:
        rp = RosterParser()
        rp.open(class_path + '/' + classFiles[0])
        course['classlist'] = rp.parse()
        rp.close()

    matchStudents(course)

    saveCourse(course)

# #
# Recursive iterates through all terms and terms classes in the research data
# #
def fullData():
    # Gethering terms
    terms = os.listdir(ARGUMENTS['path'])
    terms = removeFiles(terms)  # Only getting term directories

    # term loop
    for term in terms:
        term_path = ARGUMENTS['path'] + '/' + term

        # Selecting classes in the term
        classes = os.listdir(term_path)
        classes = removeFiles(classes)  # Only getting class directories

        # course loop
        for courseDir in classes:
            class_path = term_path + '/' + courseDir
            classFiles = removeFiles(os.listdir(class_path))

            # Creating Cousre object
            course = createCourse(courseDir)

            # Check if directory had session files
            if 'sessions' in classFiles:
                tp = TurningParser()
                tp.setPath(class_path + '/sessions')

                # Store course session and participation list
                course['session'], course[
                    'participationlist'] = tp.parse()
            else:
                print "ERROR: no session files found, Course ignored"
                pass

            # Check if a Grade/Concent file exist
            if '.xlsx' in classFiles[0]:
                rp = RosterParser()
                rp.open(class_path + '/' + classFiles[0])
                course['classlist'] = rp.parse()
                rp.close()

            matchStudents(course)

            saveCourse(course)


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


def saveCourse(couseObj):
    if ARGUMENTS['output'] != 'default':
        pic.dump(couseObj, open(
            os.path.abspath(ARGUMENTS['output'] + '/' + couseObj[
                'directory'] + '.obj',
                            "wb")))
    else:
        pic.dump(couseObj, open(
            os.path.abspath(str(PROJECT_PATH + CONFIG['directory']['output'] + '/' + couseObj[
                'directory'] + '.obj')),
                            "wb"))




# #
# Creats matchs between course['classlist'] and course ['participationlist']
# #
def matchStudents(course):
    for student_c in course['classlist']:
        match = 0
        for student_p in course['participationlist']:
            if student_c['firstname'] == student_p['firstname'] and student_c[
                'lastname'] == student_p['lastname']:
                for key, value in student_p.iteritems():
                    if not hasattr(student_c, key):
                        student_c[key] = value


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

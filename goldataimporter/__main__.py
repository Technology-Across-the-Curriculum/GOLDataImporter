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
from lib import DBConnector


# #
#
# #
def main(argv):
    # validating program before execution
    validateSetup()
    validateCommands(argv)
    importData()
    pass


# # # # # # # # # # # # # # # # # # # # # #
#           Options Functions
# # # # # # # # # # # # # # # # # # # # # #

def importData():
    course_list = {}
    classroom_list = {}
    dummy_student = {'firstname': 'Darth', 'lastname': 'Vader', 'sid': None,
    'email': None, 'consent': None, 'grade': None,
    'score': None}
    
    dbconnector = DBConnector(CONFIG['mysql'])
    courses = os.listdir(ARGUMENTS['path'])
    
    # Files being removed becase of bad data
    #courses.remove('GLFNAUD_201602_W16_CS101_001_30274.obj')
    #courses.remove('ALS4001_201602_W16_PSY201_002_38203.obj')
    
    for course_name in courses:

        pickleFile = open(ARGUMENTS['path'] + '/' + course_name,
                          "r")  # Opening file containing object
        course = pic.load(pickleFile)  # Load object from file
        pickleFile.close()  # Close object file
        print "Course: " + course['directory']
        
        # Check to see if the cousre is already added to the database
        if course['acronym'] in course_list.keys():
            course['id'] = course_list[course['acronym']]
        else:
            course['id'] = dbconnector.insertCourse(
                course)  # Insert course information
            course_list[course['acronym']] = course['id']

            classroom_id = None
        # Check if clas room is already added to the database
        if course['section']['classroom'] in classroom_list.keys():
            classroom_id = classroom_list[course['section']['classroom']]
        else:
            classroom_id = dbconnector.insertClassroom(
                course['section'][
                    'classroom'])  # Inserting classroom information
            classroom_list[course['section']['classroom']] = classroom_id

        # Section: set and insert information
        course['section']['classroom_id'] = classroom_id
        course['section']['course_id'] = course['id']
        course['section']['id'] = dbconnector.insertSection(course['section'])
        print("|--> Section: information inserted")
        
        # Student: sets and inserts information
        for student in course['classlist']:
            #print student;
            student['section_id'] = course['section']['id']
            validateStudent(student)
            student['id'] = dbconnector.insertStudent(student)
        print("  |--> class_list: student inserted")

        # creating a dummy student
        dummy_student['section_id'] = course['section']['id']
        dummy_student['id'] = dbconnector.insertStudent(dummy_student)
        print("  |--> class_list: dummy student inserted")
        
        # opening logging file
        FILE_PATH = PROJECT_PATH + '/log/' + course['directory'] + '.txt'
        
        # loop for each section found in a course
        for session in course['session']:

            # Session: set and insert information
            session['section_id'] = course['section']['id']
            session['id'] = dbconnector.insertSession(session)
            print("    |--> Session: inserted")
            
            # Match session participants with classlist students
            for participant in session['participants']:
                # if turn, the id from the classlist will be added to the participant 
                # # # # # # # # # # # # # # # # # #  # # # #
                matchParticipant(course['classlist'],
                 participant, dummy_student)
                # # # # # # # # # # # # # # # # # #  # # # #
                participant['session_id'] = session['id']
                participant['id'] = dbconnector.insertParticipant(
                    participant)
            print("      |--> Participants: inserted")

            for question in session['questions']:

                # Question: set and insert information
                question['session_id'] = session['id']
                question['id'] = dbconnector.insertQuestion(question)
            print("      |--> Question: inserted")
            
            # Insert loop for answers found in current questions
            for answer in question['answers']:
                answer['question_id'] = question['id']
                answer['id'] = dbconnector.insertAnswer(answer)
            print("        |--> Answers: inserted")

            # Insert loop for responses found in current questions
            for response in question['responses']:
                # if ture, the current responce will have the id of the corresponding session participant
                if (matchParticipantResponse(session['participants'],
                    response, dummy_student)):
                    response['question_id'] = question['id']
                    response['id'] = dbconnector.insertResponse(response)

            print("        |--> Responses: inserted")


# # # # # # # # # # # # # # # # # # # # # #
#           Helper Functions
# # # # # # # # # # # # # # # # # # # # # #

# temp methods to create valid student data
def validateStudent(student):
    keys = ['firstname', 'lastname', 'email', 'sid', 'consent', 'grade']
    
    for k in keys:
        if haskey(student, k) != 1:
            student[k] = 'null'


# Checks if an object contains a certain
def haskey(obj, key):
    keys = obj.keys()
    key_found = 0
    for k in keys:
        if k == key:
            key_found = 1

            return key_found


# Matches a session participant to the corresponding classlist student
# Return True if match is found, sets classlist_id for corresponding participant
# Return False if no match is found
# def matchParticipant(student_list, participant, dummy):
#     match_flag = 0
#     # print '|--Participant:' + participant['firstname'] + ', ' + participant[
#     #     'lastname']
#     for student in student_list:

#         if (student['firstname'] == participant['firstname'] and student[
#             'lastname'] == participant['lastname']): 

#             # set the participant classlist_id
#             participant['classlist_id'] = student['id']

#             # set flag
#             match_flag = 1

#             break

#         if ('email' in student) and ('email' in participant):
#             c_email = False
#             p_email = False

#             # Parse email befor the @
#             if student['email'] is not None:
#                 c_email = student['email'].split('@')
#             if participant['email'] is not None:
#                 p_email = participant['email'].split('@')

#             # Compare "onids"
#             if c_email and p_email:
#                 if c_email[0] == p_email[0] :

#                     # set the participant classlist_id
#                     participant['classlist_id'] = student['id']

#                     # set flag
#                     match_flag = 1

#                     break

#         if ('SID' in student) and ('lmsid' in student_p):
#             c_sid = False
#             p_lmsid = False

#             # Parse email befor the @
#             if student['SID'] is not None:
#                 c_sid = student['SID'];
#             if participant['lmsid'] is not None:
#                 p_lmsid = participant['lmsid']

#             if c_sid and p_lmsid:
#                 if c_sid == p_lmsid:

#                     # set the participant classlist_id
#                     participant['classlist_id'] = student['id']

#                     # set flag
#                     match_flag = 1
#                     break

#     if  match_flag == 0:
#         # print "NO: match found set to dummy"
#         # print "  |--Not Match: set to Dummy"
#         participant['classlist_id'] = dummy['id']

def matchParticipant(student_list, participant, dummy):
    match = False;
    studentCount = 0
    studentListSize = len(student_list) -1

    # for each student in the course list
    #for student in student_list:
    while (studentCount < studentListSize) and (match != True):
        matchAttributes = {
            'device_alt_id': False, 
            'participantid': False, 
            'firstname': False, 
            'lastname': False, 
            'sid': False, 
            'userid': False, 
            'turningid': False, 
            'assigneddevice': False, 
            'lmsid': False, 
            'email': False, 
            'device_id': False
        }
        match = False

        student = student_list[studentCount]

        # for each attriubite that can be matched.
        for attr in matchAttributes:
            s_data = False
            p_data = False

            # validato if student and participant have matching attributes
            if( attr in student) and (attr in participant):

                # check for null data and set data
                if(student[attr] is not None):
                    if attr == 'email':
                        s_data = student['email'].split('@')[0]
                    else:
                        s_data = student[attr]

                # check for null data and set data
                if(participant[attr] is not None):
                    if attr == 'email':
                        p_data = participant['email'].split('@')[0]
                    else:
                        p_data = participant[attr]

                # if *_data contains data
                if s_data and p_data:
                    # check if *_data match
                    if s_data == p_data:
                        matchAttributes[attr] = True

        match = isMatch(matchAttributes)

        # if participan and student match set participant classlist_id to student id
        if(match):
            participant['classlist_id'] = student['id']
        # Increese counter
        studentCount += 1

    # if not mach is found set to dummy student
    if not match:
        participant['classlist_id'] = dummy['id']






def isMatch(attrObject):
    count = 0;
    result = False;
    size = len(attrObject);

    for attr in attrObject:
        if attrObject[attr]:
            count += 1

    matchPercent = float(count) / float(size)
    if matchPercent >= .18:

        result = True
    return result



# Matches a responds to the corresponding session participant
# Return True if match is found, sets participant_id for corresponding responds
# Return False if no match is found
def matchParticipantResponse(participant_list, response, dummy):
    for participant in participant_list:
        if (participant['device_id'] == response['deviceid']):
            response['participant_id'] = participant['id']
            
            return 1
            return 0


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
        if argv[2] != '-di':
            print "ERROR: incorrect flag"
            usage()
            exit()
        else:
            arguments['deidentify'] = argv[2]

    # Check path
    if (os.path.exists(os.path.abspath(argv[0])) == 0):
        print os.path.abspath(PROJECT_PATH + argv[0])
        print "ERROR: data object path not found"
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
    print '''usage: ./goldataimporter <directory> [-c] [-s] [salt]
    directory:  relative path to GOL data parced object files
    -c:  only import concenters
    -s:  salt entry in import'''


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

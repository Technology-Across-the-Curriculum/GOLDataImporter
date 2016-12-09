# # # # #
# Project: GOLDataImporter
# File: 
# Created by: Nathan Healea
# Description:
# 
# # # # #
import os
import turningparser as TurningParser

class SessionParser:
    def __init__(self, rootPath):
        self.root = rootPath

    def parseData(self):

        # Getting session files
        session_files = os.listdir(self.root)  # list of files in root

        # variables
        #directoryName = os.path.split(self.root)[1]  # directory name
        #directoryInfo = directoryName.split('_')  # directory name split

        #print("Current Directory: %s") % (directoryName)

        # creating turning parser obj
        turnParse = TurningParser()
        #rosterParse = RosterParser()

        # creating course object
        course = {}
        #course['acronym'] = directoryInfo[3]
        #course['directory'] = directoryName
        #course['section'] = {}  # dictionary for section information
        course['session'] = []  # array of section objects
        #course['classlist'] = []  # array of students from Consent/Grade list
        course[
            'participationlist'] = []  # array of participants from session files

        # parsing section information
        #course['section'] = turnParse.getSection(directoryName)
        #print(" |-- Section: Parsing information")

        # rosterParse.open('{0}/{1}'.format(root, files[0]))
        # course['classlist'] = rosterParse.parse()
        # rosterParse.close()
        # print(" |-- Section: Parsing Classlist")

        for file in session_files:
            # split filename and extension
            filename, fileExt = os.path.splitext(file)

            # openfile
            turnParse.openFile(self.root + '/' + file)

            print("  |-- Session: %s") % (filename)

            # Parsing and storing the current session
            session = turnParse.getSession()
            print("    |-- Information: Parsed")

            # Parsing and inserting questions
            session['questions'] = turnParse.getQuestion()
            print("      |-- Questions: Parsed")

            # Parsing and inserting participants for session
            session[
                'participants'] = turnParse.getParticipant()  # Processing participant list
            print("      |-- Participants: Parsed")

            turnParse.closeFile()  # Close the current file

            course['session'].append(session)  # Append session to section

        # build section participant list
        for session in course['session']:
            turnParse.getSectionParticipantList(course['participationlist'],
                                                session['participants'])
        # for student_c in course['classlist']:
        #     match = 0
        #     for student_p in course['participationlist']:
        #         if student_c['firstname'] == student_p['firstname'] and \
        #                         student_c[
        #                             'lastname'] == student_p['lastname']:
        #             for key, value in student_p.iteritems():
        #                 if not hasattr(student_c, key):
        #                     student_c[key] = value

        return course
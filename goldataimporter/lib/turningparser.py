import sys
import os
from dictmysql import DictMySQL
import xml.etree.ElementTree as ET


class TurningParser:
    extension = '.xml'
    key = ['classroom', 'term_code', 'alt_term_code', 'acronym', 'section', 'crn', 'data_type']
    tree = None
    root = None

    # #
    # Constructor the Turning Parser Class
    def __init__(self):
        self.path = ''  # Path for current file
        self.courseObj = {}  # Hold course information

    # #
    # Opens a file and sets the tree and root
    # filepath: string (absolute path to file to be open)
    def openFile(self, filepath):
        if (os.path.exists(filepath) == False):
            print('ERRORL: file not found')
            return 1

        self.tree = ET.parse(filepath)  # Set tree
        self.root = self.tree.getroot()  # Set Root
        return 0

    # #
    # Closes the empty file
    def closeFile(self):
        self.tree = ''
        self.root = ''

        return 0

    # #
    # Parser section information out of directory name
    # directory_name: string (name of section directory to be parsed)
    # course_id: int (id of the course for section directory)
    # #
    def getSection(self, directory_name):

        sectionValues = directory_name.split("_")  # Parsing course information

        section = {  # Defining section object
            'classroom': 0,
            'section': 0,
            'crn': 0,
            'term_code': 0,
            'alt_term_code': 0,

        }

        index = 0  # index for irritation
        for k in section:
            if (k != 'sessions' and k != 'classlist'):
                section[k] = sectionValues[self.key.index(k)]

        return section

    # #
    # Parser session information out of file
    # filepath: string (absolute path to file)
    # section_id: int (id of the course section for session file)
    # #
    def getSession(self):

        # Defining session object
        session = {
            'questions': [],
            'participants': None
        }

        loopFlag = 1  # Hold flag to indicate that first properties child has been indexed

        for prop in self.root.iter('properties'):
            if (loopFlag):
                loopFlag = 0
                for field in prop:
                    session[field.tag] = field.text

        return session

    # #
    # Parser participant list from session data
    # Filepath: string (absolute path to file)
    # #
    def getQuestion(self):
        question_list = []
        for questions in self.root.iter('questions'):
            for child in questions:

                question = {
                    'id': 0,
                    'guid': 'null',
                    'sourceid': 'null',
                    'countdowntime': '',
                    'countdowntimer': '',
                    'questiontext': '',
                    'starttime': '',
                    'endtime': '',
                    'correctvalue': '',
                    'answers': [],
                    'responses': None

                }  # Defining Session object

                for leaf in child:
                    if (
                                    leaf.tag != 'responses' and leaf.tag != 'responsehistory' and leaf.tag != 'metadata' and leaf.tag != 'answers'):
                        question[leaf.tag] = leaf.text
                    elif (leaf.tag == 'responses'):
                        question['responses'] = self.getResponses(leaf)
                    elif (leaf.tag == 'answers'):
                        question['answers'] = self.getAnswers(leaf)
                        # for answer in leaf:
                        #     answerObj = {
                        #         'id': 0,
                        #         'question_id': 0
                        #     }
                        #     for property in answer:
                        #         answerObj[property.tag] = property.text
                        # question['answers'].append(answerObj)
                question_list.append(question)
        return question_list

    # #
    # Parses responses from question
    # response_list : xml that contains responses for parsing
    def getResponses(self, response_list):
        parseResponseList = []  # array of response parsed from a question
        for response in response_list:
            responseObj = {
                'id': 0,
                'question_id': 0,
                'participant_id': 0,
                'deviceid': '',
                'elapsed': 0,
                'answer': ''
            }  # Defining response object
            for property in response:
                if (property.tag == 'responsestring'):
                    responseObj['answer'] = property.text
                else:
                    responseObj[property.tag] = property.text
            parseResponseList.append(responseObj)
        return parseResponseList

    # #
    # Parses answers from question
    # answer_list: xml that contains answers for parsing
    def getAnswers(self, answer_list):
        parseAnswerList = [] # array of answers parsed from a question
        for answer in answer_list:
            answerObj = {
                'id': 0,
                'question_id': 0
            } # defining answer object
            for property in answer:
                answerObj[property.tag] = property.text
            parseAnswerList.append(answerObj)
        return parseAnswerList

    # #
    # Parser participant list from session data
    # Filepath: string (absolute path to file)
    # #
    def getParticipant(self):

        participantList = []
        loopFlag = 1  # Hold flag to indicate that first properties child has been indexed

        for child in self.root.iter('participant'):
            # Defining Session object
            participant = {
                'participantid': '',
                'firstname': '',
                'lastname': '',
                'lmsid': '',
                'userid': '',
                'device_id': '',
                'device_alt_id': '',
                'turningid': '',
                'email': '',
                'activelicense': ''
            }

            for leaf in child:

                if (leaf.tag == 'devices'):
                    count = 0
                    for device in leaf:
                        if (count == 0):
                            participant['device_id'] = device.text
                            count += 1
                        elif (count == 1):
                            participant['device_alt_id'] = device.text
                            count += 1
                else:
                    participant[leaf.tag] = leaf.text

            if (participant != {}):
                participantList.append(participant)
        return participantList

    # #
    # Creates a list of participants from section session files
    # classlist: array (List of section participant)
    # ses_list: array (session participants list)
    def getSectionParticipantList(self, classlist, ses_list):

        for part_ses in ses_list:  # for each participant in the session list of participants
            is_partispant = 0  # 0 = false , 1 = true

            # Check if the session participant has first and last name
            for part_sec in classlist:
                if (part_ses['firstname'] == part_sec['firstname'] and part_ses['lastname'] == part_sec[
                    'lastname'] or part_ses['device_id'] == part_sec['device_id']):
                    is_partispant = 1
                    break
            if (is_partispant == 0):
                classlist.append(part_ses)

pass



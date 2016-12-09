# # # # #
# Project: TurningParser
# File: 
# Created by: Nathan Healea
# Description:
# 
# # # # #

import os
import sys
from openpyxl import load_workbook

class RosterParser:
    def __init__(self):
        self.C = []  # Consent
        self.G = []  # Grades
        self.file = ''
        self.wb = None
        self.ws = {}
        self.match = []
        self.filename = None
        self.filepath = None
        self.key = ['firstname', 'lastname', 'sid', 'email', 'consent', 'grade']

    # #
    # Opens a give workbook and index worksheets
    # Parameters
    #   file: path to file to be open
    # Output
    #  True: File was open and sheets parsed
    #  False: File not opened or sheets not parsed
    def open(self, file):
        # Defining process flag
        status = True

        # Saving file name
        head, tail = os.path.split(file)
        self.filename = os.path.splitext(tail)[0]
        self.filepath = head

        # Setting File string and load workbook
        self.file = file
        self.wb = load_workbook(self.file)

        if self.wb == None:  # Check if workbook was opened
            status = False
            print ("ERROR: wb was not open")
        else:
            # Gets names of sheets from workbook
            wsNames = self.wb.get_sheet_names()
            count = 0

            # Adds sheets names and sheet to dictionary
            for sheet in self.wb.worksheets:
                self.ws[wsNames[count]] = sheet
                count += 1

            if len(self.ws) <= 0:  # Check if sheets where indexed
                status = False
                print ("ERROR: Workbooks sheet not index ")

        return status

    # #
    # Parses out sheets of a file
    # Parameters
    #   sheet: Name of the sheet to be parse
    # Output
    #   none
    # End Condition
    #    contains array of students from the passed sheet
    def parse(self):

        # Defining process status
        status = True

        # Activating consentor worksheet

        firstRow = False
        index = []
        classlist = []

        for row in self.ws['M'].iter_rows():
                count = 0
                student = {}
                for cell in row:
                    student[self.key[count]] = cell.value
                    count += 1
                classlist.append(student)
        return classlist

    # #
    # Closes current workbook and removes all data from object
    #
    def close(self):
        self.C = []  # Consent
        self.G = []  # Grades
        self.file = ''
        self.wb = None
        self.ws = {}
        self.match = []
        self.filename = None
        self.filepath = None

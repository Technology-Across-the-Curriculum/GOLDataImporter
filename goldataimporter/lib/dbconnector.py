from dictmysql import DictMySQL


class DBConnector:
    __connection = ''  # Holds connection to database

    # #
    # Constructor for  DBConnector
    # Take database configuration as argument
    # config: object containing(db, host, user, passwd)
    #       db: database name
    #       host: host address
    #       user: username
    #       passed: password
    def __init__(self, config):
        # Need to change database connection information
        self.__connection = DictMySQL(db=config['db'],
                                      host=config['host'],
                                      user=config['user'],
                                      passwd=config['passwd'])

    # #
    # Inserts course information in the course table
    # course: object containing (acronym)
    # returns: id of row inserted
    def insertCourse(self, course):

        for key in course:
            if course[key] == 0:
                print("ERROR: Not all key are filled. \n")
                return 1

        course_id = self.__connection.insert(table='course',
                                             value={
                                                 'acronym': course['acronym']
                                             })

        if (course_id == 0):
            print("ERROR: Course not inserted. \n")
            return 1

        return course_id

    # #
    # Inserts classroom information in the classroom table
    # name: name of the classroom (ex: LINC100)
    # returns: id of row inserted
    def insertClassroom(self, name):

        if (name == None):
            print("ERROR: Classroom not provided. \n")
            return 0

        classroom_id = self.__connection.insert(table='classroom',
                                                value={
                                                    'name': name
                                                })

        if (classroom_id == 0):
            print("ERROR: classroom not inserted. \n")
            return 1

        return classroom_id

    # #
    # Inserts section into the section table
    # section: object containing (classroom_id, code, crn, term_code, alt_term_code, course_id)
    # returns: id of row inserted
    def insertSection(self, section):
        for key in section:
            if section[key] == 0:
                print("ERROR: Not all key are filled. \n")
                return 1
        section_id = self.__connection.insert(table='section',
                                              value={
                                                  'classroom_id': section['classroom_id'],
                                                  'code': section['section'],
                                                  'crn': section['crn'],
                                                  'term_code': section['term_code'],
                                                  'alt_term_code': section['alt_term_code'],
                                                  'course_id': section['course_id']

                                              })


        if (section_id == 0):
            print("ERROR: Section not inserted. \n")
            return 1

        return section_id

    # #
    # Inserts student information into student table
    # student: object (section_id, fristname, middlename, lastname, studentid, email, consent)
    # returns: id fo row inserted
    def insertStudent(self, student):
        student_id = self.__connection.insert(table='classlist',
                                              value={
                                                  'section_id': student['section_id'],
                                                  'first_name': student['firstname'],
                                                  'last_name': student['lastname'],
                                                  'email': student['email'],
                                                  'student_id': student['sid'],
                                                  'consent': student['consent'],
                                                  'grade' : student['grade'],
                                                  'score' : student['score']

                                              })
        if (student_id == 0):
            print("ERROR: Student not inserted. \n")
            return 1

        return student_id

        

    # #
    # Inserts session information into session table
    # session: object containing (guid, sourceid, sessiontype, datecreated, section_id)
    # returns: id of row inserted
    def insertSession(self, session):

        session_id = self.__connection.insert(table='session',
                                              value={'guid': session['guid'],
                                                     'source_id': session['sourceid'],
                                                     'session_type': session['sessiontype'],
                                                     'date_created': session['datecreated'],
                                                     'section_id': session['section_id']}
                                              )
        if (session_id == 0):
            print("ERROR: Session not created. \n")
            return 1

        return session_id
    
    

    # #
    # Inserts participant information into participant table
    # participant: object containing
    #   (session_id, classlist_id, firstname, lastname, lmsid, userid, device_id, device_alt_id, turningid, email, activelicense)
    # returns: id of row inserted
    def insertParticipant(self, participant):
        participant_id = self.__connection.insert(table='participant_list',
                                                  value={
                                                      'session_id': participant['session_id'],
                                                      'classlist_id': participant['classlist_id'],
                                                      'first_name': participant['firstname'],
                                                      'last_name': participant['lastname'],
                                                      'lmsid': participant['lmsid'],
                                                      'user_id': participant['userid'],
                                                      'device_id': participant['device_id'],
                                                      'device_alt_id': participant['device_alt_id'],
                                                      'turning_id': participant['turningid'],
                                                      'email': participant['email'],
                                                      'active_license': participant['activelicense'],
                                                  })
        if (participant_id == 0):
            print("ERROR: Session not created. \n")
            return 1
        return participant_id

    # #
    # Inserts question information into question table
    # question: object containing:
    #   (guid, sourceid, questiontext, starttiem, endtime, countdowntime, countdowntimer, correctvalue, session_id)
    # returns: id of the row inserted
    def insertQuestion(self, question):
        question_id = self.__connection.insert(table='question',
                                               value={
                                                   'guid': question['guid'],
                                                   # 'repollguid': question['repollguid'],
                                                   'sourceid': question['sourceid'],
                                                   'questiontext': question['questiontext'],
                                                   'start_time': question['starttime'],
                                                   'end_time': question['endtime'],
                                                   # 'showresults': question['showresults'],
                                                   # 'responsegrid': question['responsegrid'],
                                                   'countdown_time': question['countdowntime'],
                                                   'countdown_timer': question['countdowntimer'],
                                                   'correct_value': question['correctvalue'],
                                                   # 'incorrectvalue': question['incorrectvalue'],
                                                   # 'keywordvaluetype': question['keywordvaluetype'],
                                                   'session_id': question['session_id']
                                               })

        if (question_id == 0):
            print("ERROR: question not inserted. \n")
            return 1
        return question_id

    # #
    # Inserts answer information (from a question) into the answer table
    # answer: object containing (question_id, guid, answertext, valuetype)
    # returns: id of row inserted
    def insertAnswer(self, answer):
        answer_id = self.__connection.insert(table='answer',
                                             value={
                                                 'question_id': answer['question_id'],
                                                 'guid': answer['guid'],
                                                 'text': answer['answertext'],
                                                 'value': answer['valuetype']
                                             })

        if (answer_id == 0):
            print("ERROR: question not inserted. \n")
            return 1
        return answer_id

    # #
    # Inserts response information (from a question) into the response table
    # response: object containing (answer, elapsed, deviceid, participant_id, question_id)
    # returns: id of row inserted
    def insertResponse(self, response):
        response_id = self.__connection.insert(table='response',
                                               value={
                                                   'answer': response['answer'],
                                                   'time_elapsed': response['elapsed'],
                                                   'device_id': response['deviceid'],
                                                   'participant_id': response['participant_id'],
                                                   'question_id': response['question_id'],

                                               })

        if (response_id == 0):
            print("ERROR: responce not inserted. \n")
            return 1
        return response_id

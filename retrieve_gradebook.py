from gAPI import Create_Service
import pandas as pd
import numpy as np
import json
import csv
from pandas.io.json import json_normalize
from googleapiclient.errors import HttpError


CLIENT_SECRET_FILE = 'client_secret.json'
API_SERVICE_NAME = 'classroom'
API_VERSION = 'v1'
SCOPES = ['https://www.googleapis.com/auth/classroom.coursework.students https://www.googleapis.com/auth/classroom.courses']

service = Create_Service(CLIENT_SECRET_FILE, API_SERVICE_NAME, API_VERSION, SCOPES)

class ClassMasteryData:
    def __init__(self,class_name):
        self.class_name = class_name
        self.id = self.get_class_id()
        self.coursework = self.get_coursework()
        self.submissions = self.get_submissions(self.coursework)

    def get_class_id(self):
        my_courses = get_courses()
        for course in my_courses:
            if(json.dumps(course[0]).find(self.class_name)!= -1):
                self.id = json.dumps(course[1]).strip('"')
        return self.id
        
    def get_coursework(self):
        aslist = [self.id]
        self.coursework = get_coursework(aslist)
        return self.coursework

    #this needs to be edited to return a dict or list of submissions tied to each course
    def get_submissions(self, coursework_id):
        coursework_id_i = [coursework_id[0]['courseWork'][0]['id']]
        self.submissions = get_submissions([self.id], coursework_id_i)
        return self.submissions

class Classwork(ClassMasteryData):
    def __init__(self, class_name):
        ClassMasteryData.__init__(self, class_name)
        self.classId = ClassMasteryData.get_class_id(self)

    #def collect_all(self):
        #function to collect all individual coursework into a list

    #def get_courseWorkId(self):
        


class Submission(Classwork):
    def __init__(self, class_name):
        Classwork.__init__(self, class_name)
        self.draftGrade =self.get_draftGrade()
        self.updateTime = self.get_updateTime()
        self.alternateLink = self.get_alternateLink()
        self.userId = self.get_userId()
        self.creationTime = self.get_creationTime()
        self.state = self.get_state()
        self.courseWorkId = self.get_courseWorkId()
        self.courseWorkType = self.get_courseWorkType()
        self.assignedGrade = self.get_assignedGrade()
        self.id = self.get_id()
        self.maxPoints = self.get_maxPoints()    
        self.courseId = self.get_class_id()
        self.classId = Classwork.get_class_id(self)
    
    def get_draftGrade(self):
        return self.submissions[0]['studentSubmissions'][0]['draftGrade']
       
    def get_updateTime(self):
        return self.submissions[0]['studentSubmissions'][0]['updateTime']

    def get_alternateLink(self):
        return self.submissions[0]['studentSubmissions'][0]['alternateLink']

    def get_userId(self):
        return self.submissions[0]['studentSubmissions'][0]['userId']

    def get_creationTime(self):
        return self.submissions[0]['studentSubmissions'][0]['creationTime']

    def get_state(self):
        return self.submissions[0]['studentSubmissions'][0]['state']
   
    def get_courseWorkId(self):
        return self.submissions[0]['studentSubmissions'][0]['courseWorkId']
   
    def get_courseWorkType(self):
        return self.submissions[0]['studentSubmissions'][0]['courseWorkType']
  
    def get_assignedGrade(self):
        return self.submissions[0]['studentSubmissions'][0]['assignedGrade']

    def get_id(self):
        return self.submissions[0]['studentSubmissions'][0]['id']
  
    def get_maxPoints(self):
        return self.submissions[0]['studentSubmissions'][0]['submissionHistory'][2]['gradeHistory']['maxPoints']
    
    

def get_courses():
    raw_response_data = service.courses().list().execute()
    response_data = raw_response_data['courses']
    l_response = []
    for course in response_data:
        l_response.append((course['name'], course['id']))
    return l_response

def isolate_ids(courses):
    ids = []
    for course in courses:
        ids.append(course[1])
    return ids

def get_coursework(course_ids):
    raw_response_data = []
    for i in range(len(course_ids)):
        id = course_ids[i]
        raw_response_data.append(service.courses().courseWork().list(courseId=id).execute())
    return json.loads(json.dumps(raw_response_data))

def isolate_cw_ids(coursework):
    ids = []
    for work in coursework:
        if 'courseWork' in work.keys():
            ids.append(work['courseWork'][0]['id'])
    return ids

def get_submissions(course_ids, coursework_ids):
    raw_response_data = []
    for i in range(len(course_ids)):
        for j in range(len(coursework_ids)):
            try:
                raw_response_data.append(service.courses().courseWork().studentSubmissions().list(courseId=course_ids[i], courseWorkId=coursework_ids[j]).execute())
                return raw_response_data
            except HttpError as err:
                if err.resp.status in [403, 500, 503]:
                    time.sleep(5)
                else: raise




#the following will spit out a list of all submissions!
#courses = get_courses()
#ids = isolate_ids(courses)
#coursework = get_coursework(ids)
#cw_ids = isolate_cw_ids(coursework)
#raw_submissions = get_submissions(ids, cw_ids)
#submissions = raw_submissions[0]['studentSubmissions']

#testclass = ClassMasteryData('Code Nation Test')
#testclass2 = ClassMasteryData('Opportunity Hack Dummy')
#c2 = service.courses().get(id=testclass2.id).execute()
#c = service.courses().get(id=testclass.id).execute()
#print(testclass.class_name , c['name'])
#print(testclass2.class_name, c2['name'])

#testclass = ClassMasteryData('Code Nation Test')
#print(testclass.submissions)

mySubmission = Submission('Code Nation Test')
print(mySubmission.id, mySubmission.assignedGrade, mySubmission.maxPoints)





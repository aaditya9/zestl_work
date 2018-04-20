import sys
import json
import logon as LL
import logging
import os
import common as CM
import csv
import password as PD
import json
# BASE_URL = "http://twig-me.com/v13/"  ### dev server
BASE_URL = "https://twig.me/v13/"
email = "admin@zestl.com"
# pwd = "TwigMeNow"
pwd = PD.pwd
inputFile = "C:/Users/Minal Thorat/Dropbox/Zestl-scripts/millennium/script_inputs/one.csv"
headers, headers1 = LL.req_headers(email, pwd, BASE_URL)
# zviceID = "95YTMAVLYEE7D"   # kidz care dev
zviceID = "FWSMGL6USVKDW"   # kidz care prod
hasHeader = "Y"

#*******************************    Upload   Data*****************

with open(inputFile, 'r') as rf:
    data = csv.reader(rf, delimiter=',')
    if hasHeader == "Y":
        row1 = data.next()
    counter = 0
    for row in data:
        counter += 1
        print counter
        body = {}
        url = BASE_URL + "kidzcare/" + zviceID + "/content/upload"
        method = "POST"
        body['Content'] = CM.force_decode(row[0].strip())
        body['Flag'] = CM.force_decode(row[1].strip())
        body['Center'] = CM.force_decode(row[2].strip())
        b = []
        b.append(body)
        resp = CM.hit_url_method(b, headers1, method, url)
        print resp
#***************************************************************

# url = BASE_URL + "kidzcare/" + zviceID + "/reports/upload"
# method = "POST"
#
# body = {}
# body['OrgZviceID'] = 3000012597
# body['CenterName'] = "YADKIN"
# # body['CenterName'] = "YADKIN"
# body['Date'] = "2017-11-10"
# topbody = []
# with open(inputFile, 'r') as rf:
#     data = csv.reader(rf, delimiter=',')
#     if hasHeader == "Y":
#         row1 = data.next()
#     counter = 0
#     req = {}
#     for row in data:
#         counter += 1
#         print counter
#
#         # url = BASE_URL + "kidzcare/" + zviceID + "/reports/upload"
#         # method = "POST"
#         #
#         # body = {}
#         # body['OrgZviceID'] = 3000012597
#         # body['CenterName'] = "YADKIN"
#         # body['Date'] = "2017-11-10"
#         # body = {}
#         # body['OrgZviceID'] = 3000012597
#         # body['Cente0rName'] = "YADKIN"
#         # body['CenterName'] = row[0]
#         # body['Date'] = "2017-11-10"
#         # body['Date'] = row[1]
#         req[row[2]] = {
#                         "Hosp" : row[3] ,
#                         "Absent" : row[4] ,
#                         "HalfDay" : row[5] ,
#                         "Onsite" : {
#                             "PatientsScheduled" : row[6] ,
#                             "PatientsSeen" : row[7] ,
#                             "Noshow" : row[8]
#                         }}
#
#
#         body['Doctors'] = json.dumps(req)
#         topbody.append()
#             # {row[2]:{
#             #             "Hosp" : row[3] ,
#             #             "Absent" : row[4] ,
#             #             "HalfDay" : row[5] ,
#             #             "Onsite" : {
#             #                 "PatientsScheduled" : row[6] ,
#             #                 "PatientsSeen" : row[7] ,
#             #                 "Noshow" : row[8]
#             #             }
#             #         }}
#
#
#
#         # print body
# topbody = []
# topbody.append(body)
# print topbody
# resp = CM.hit_url_method(topbody, headers1, method, url)
# print resp
#
#         # CenterName: "YADKIN"
#         # Date: "2017-11-01"
#         # Doctors: {
#         #     "MyTrang Dang, PA-C": {
#         #         "Hosp": "0",
#         #         "Absent": false,
#         #         "HalfDay": false,
#         #         "Onsite": {
#         #             "PatientsScheduled": "10",
#         #             "PatientsSeen": "10",
#         #             "NoShow": "0"
#         # *RequestBody:
#         # *{
#         #     *"OrgZviceID": "ZviceID"
#         #                    * "CenterName": "<Unique name>",
#         #                                    *"Date": "<Date>",
#         #                                             *"Data": [
#         #     *{
#         #          * // Key = > Value
#         #                       *}
#         # *]
#         # *}
#         #

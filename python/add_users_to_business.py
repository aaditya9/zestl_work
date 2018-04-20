#!/usr/local/bin/python

import base64
import time
import urllib2
from urllib2 import URLError
from urllib2 import HTTPError
import requests
import urllib
import json
import time
import os
import re
import sys
import hashlib
import csv
import pprint
import argparse

import lib.login_prod as LL
import common_functions as CF


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-userDetails', nargs=1, type=str, required=True, dest='inputcsv', help = 'Provide input csv that contains the user inputs')
    parser.add_argument('-loginDetails', nargs=1, type=str, required=True, dest='credentials', help = 'Provide a file that contains the login credentials')
    parser.add_argument('-report', nargs=1, type=str, dest='report', help = 'Provide path for report file')
    args = parser.parse_args()

    inputcsv = args.inputcsv[0]
    credentials = args.credentials[0]
    if (args.report):
        report = args.report[0]
    else:
        timestamp = time.strftime("%d%m%Y_%H_%M_%S", time.localtime())
        report = "tempfiles/report_" + timestamp

    reportfile = open (report, 'w')
    
    print credentials
    
    CV = {}
    execfile (credentials, CV)

    # login
    headers, headers1, userIdentity = LL.req_headers(CV['BASE_URL'], CV['email'], CV['pwd'])
    
    #get base card details
    method = 'POST'
    url = CV['BASE_URL'] + 'zvice/detailscard/' + CV['zbotID']
    body = {}
        
    response = CF.hit_url(method, url, json.dumps(body), headers1)
    
    csvfile = open (inputcsv, 'r')
    orgInputs = csv.DictReader(csvfile)
        
    response = json.loads(response)
    cardlist = response['data']['elements']
    for card in cardlist:
        title = card['title']
        if (title == 'Users'):
            actionlist= card['actions']
            for action in actionlist:
                if (action['title'] == 'Create'):
                    # found action now create all inputs for the API call
                    apiurl = action['actionUrl']
                    method = action['method']
                    body = {}
                    # get all fixed inputs
                    inputlist = action['inputs']
                    for inp in inputlist:
                        proplist = inp['properties']
                        key = ""
                        value = ""
                        for i, prop in enumerate(proplist):
                            if (i == 0):
                                key = prop['value']
                            if (i == 1):
                                value = prop['value']
                        body[key] = value
                    #now insert specific inputs
                    for row in orgInputs:
                        body['title'] = row['Title']
                        body['linkemail'] = row['Email ID']
                        body['zviceinfo'] = row['Description']
                        body['zviceid'] = row['Tag Id']
                        # Hit URL to add user
                        adduser_response = CF.hit_url(method, apiurl, json.dumps(body), headers1)  
                        adduser_response = json.loads(adduser_response)
                        if (adduser_response['error'] == False):
                            message = "User added Successfully! \nName: " + row['Title'] + " Tag ID: " + row['Tag Id']
                            print message
                            reportfile.write(message)
                        if (adduser_response['error'] == True):
                            message = "User addition FAILED! \nName: " + row['Title'] + " Tag ID: " + row['Tag Id'] + " Error Message: " + adduser_response['message']
                            print message
                            reportfile.write(message)
                            
    reportfile.close()
    print "Check log at: ", report
    

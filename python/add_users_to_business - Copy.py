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
# TODO: need to take this from cmmand line to make it generic
import lib.credential_millennium as CV
import common_functions as CF

def add_phone_number(response, user, headers1):
    response = json.loads(response)
    cardlist = response['data']['elements']
    for card in cardlist:
        title = card['title']
        if (title == 'Contact Details'):
            actionlist= card['actions']
            for action in actionlist:
                if (action['title'] == 'Edit'):
                    # found action now create all inputs for the API call
                    url = action['actionUrl']
                    method = action['method']
                    body = {}
                    # create body
                    inputlist = action['inputs']
                    for inp in inputlist:
                        if 'EditText' in inp['widget']:
                            proplist = inp['properties']
                            key = ""
                            value = ""
                            for i, prop in enumerate(proplist):
                                if (i == 0):
                                    key = prop['value']
                                if (i == 1):
                                    value = prop['value']
                            body[key] = value
                    print body
                    #now insert specific inputs
                    body['Contact'] = user['Contact Number']
                    body['EmailID'] = user['Email ID'] 
                    print body
                    # Hit URL to add user
                    #response = CF.hit_url(method, url, json.dumps(body), headers1)  
                    #response = json.loads(response)
                    #print response
                            
                    
         #   print actionlist
    return
    
def add_contact_details (headers1, user):
    method = "POST"
    url = CV.BASE_URL + 'zvice/detailscard/' + user['Tag Id']
    response = CF.hit_url(method, url, None, headers1)

    response = json.loads(response)
    cardlist = response['data']['elements']
    for card in cardlist:
        title = card['title']
        if (title == 'Contact Details'):
            method = card['method']
            url = card['cardsjsonurl']
            body = card['content']
            response = CF.hit_url(method, url, body, headers1)
            add_phone_number(response, user, headers1)
    return
    
if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-filename', nargs=1, type=str, required=True, dest='inputcsv', help = 'Provide input csv')
#    parser.add_argument('-loginID', nargs=1, type=str, required=True, dest='loginID', help = 'Provide login email')
#    parser.add_argument('-pwd', nargs=1, type=str, required=True, dest='pwd', help = 'Provide login pwd')
    args = parser.parse_args()

    inputcsv = args.inputcsv[0]
    
    # login
    headers, headers1, userIdentity = LL.req_headers(CV.BASE_URL, CV.email, CV.pwd)
    
    #get base card details
    method = 'POST'
    url = CV.BASE_URL + 'zvice/detailscard/' + CV.zbotID
    body = {}
        
    response = CF.hit_url(method, url, json.dumps(body), headers1)
#    with open('MNS', 'w') as f:
#        f.write(str(response))
    
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
#                        adduser_response = CF.hit_url(method, apiurl, json.dumps(body), headers1)  
#                        adduser_response = json.loads(adduser_response)
#                        if (adduser_response['error'] == False):
#                            print "User added Successfully! \nName: ", row['Title'], " Tag ID: ", row['Tag Id']
#                        if (adduser_response['error'] == True):
#                            print "User addition FAILED! \nName: ", row['Title'], " Tag ID: ", row['Tag Id'], " Error Message: ", adduser_response['message']
                        
                        # Now update contact details of the User
                        add_contact_details(headers1, row)
                        
                                
#                        print adduser_response
#                        with open('MNS', 'w') as f:
#                            f.write(str(adduser_response))
                        
            
    
    #print response
    
#    URL = args.server[0]
#    BASE_URL =str(URL + "/v1/")
#    email = args.loginID[0]
#    pwd = args.pwd[0]
    
#        filename = "./../../Millennium/MNS_AdminData_TwigMe_CSV.csv"
    #with open (inputcsv, 'r') as csvfile:
     #   reader = csv.DictReader(csvfile)
      #  for row in reader:
      #      pprint.pprint(row)
            
    # login
#    headers, headers1, userIdentity = LL.req_headers(BASE_URL, email, pwd)
    
 #   print userIdentity
    #tagID = userIdentity.strip(URL) right usage
  #  tagID = userIdentity.strip("http://www.twig.me/")
   # print "server: ", URL, "\nemail: ", email, "\ntagID: ", tagID 
    
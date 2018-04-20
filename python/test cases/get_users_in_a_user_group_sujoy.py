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
import hashlib\

import argparse
import lib.login1 as LL
import create_text_cards as TC

def getAllUserGroups(headers, zbotID):
    jsondata = LL.invoke_rest('GET', LL.BASE_URL + 'usergroups/' + zbotID, None, headers)
    return jsondata['reply']

def getUsersInGroup(headers, grpID, zbotID):
    jsondata = LL.invoke_rest('GET', LL.BASE_URL + 'usergroups/' + grpID + '/' + zbotID, None, headers)
    return jsondata['reply']

def get_users_in_nested_groups(f1, grpName, allGrpData):
    print grpName
    for x in allGrpData:
        if x == grpName :
            print "group found: ", x, " ", grpname[x]
            
            #get group details
            grpdetails = json.loads(getUsersInGroup(headers1, str(grpname[x]) ,LL.zbotID))
            # check if group contains groups            
            grpdetails = grpdetails['output']['groupdetails']
            for y in grpdetails:
                print y
                # check if group contains groups        
                if y == 'groups' :
                    groups = grpdetails[y]
                    for z in groups:
                        get_users_in_nested_groups(z,grpname)
                        
                if y == 'users' :
                    users = grpdetails[y]
                    for z in users:
                        #print (z + "\t" + users[z])
                        f1.write(z + "\t" + users[z] + "\n")
            break
    return

def printUsers(grpname1, zvice):
    grpdetails = json.loads(getUsersInGroup(headers1, str(grpname1), zvice))
    grpdetails = grpdetails['output']['groupdetails']
    for y in grpdetails:
        print y
        # check if group contains groups
        if y == 'groups':
            groups = grpdetails[y]
            for z in groups:
                get_users_in_nested_groups(f1, z, grpname)

        if y == 'users':
            users = grpdetails[y]
            for z in users:
                print z + "\t" + users[z]
                # f1.write(z + "\t" + users[z] + "\n")
    return users

if __name__ == '__main__':
    
    # i must login
    headers, headers1 = LL.req_headers()

    # name = "Weekday Boarders Boys"
    name = "Freelance Trainers"

    inputGrpName = name
    print "User Group Name : " + inputGrpName
    
    # f1=open('./tempfiles/jsonout', 'w')
    #get all user groups information
    usergroups = TC.getAllUserGroups(headers1, LL.zbotID, LL.BASE_URL)
        # getAllUserGroups(headers1, LL.zbotID)
    # print usergroups
    grpvals = json.loads(usergroups)
    grps = grpvals['output']
    grpname = grps['usergroup']

    # get group number of group whose data is required
    for x in grpname:
        print x
        if x == inputGrpName :
            print "======================================"
            print "group found: ", x, " ", grpname[x]

            users = printUsers(grpname[x], LL.zbotID)
            #get group details

            # print users
            break
    
    # f1.close()

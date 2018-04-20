#!/usr/local/bin/python

import base64
import time
import urllib2
from urllib2 import URLError
from urllib2 import HTTPError
import requests
import urllib
import json
import csv
import time
import os
import re
import sys
import hashlib\

import lib.login1 as LL


def getUsersInGroup(headers, grpID, zbotID):
    jsondata = LL.invoke_rest('GET', LL.BASE_URL + 'usergroups/' + grpID + '/' + zbotID, None, headers)
    return jsondata
    
def getAllUserGroups(headers, zbotID):
    # jsondata = LL.invoke_rest('GET', LL.BASE_URL + 'usergroups/' + zbotID + '?filter=\{\\"limit\":0,\"offset\":1000\}', None, headers)  ###### Trial Code

    jsondata = LL.invoke_rest('GET', LL.BASE_URL + 'usergroups/' + zbotID, None, headers)    #### Sir Code****************
    return jsondata['reply']

def add_user(body, headers, zbotID, grpID):
    jsondata = LL.invoke_rest('POST', LL.BASE_URL + 'usergroups/' + grpID + '/user/add/' + zbotID, body, headers)
    
    # print "User Group API response : Code : " + str(jsondata['code'])
    # print "======================="
    # print jsondata['reply']
    # print "======================="
    return jsondata['reply']

def add_usergrps_grps(body, headers, zbotID, grpID):
    jsondata = LL.invoke_rest('POST', LL.BASE_URL + 'usergroups/' + grpID + '/usergroup/add/' + zbotID, body, headers)
    # print "User Group API response : Code : " + str(jsondata['code'])
    # print "======================="
    # print jsondata['reply']
    # print "======================="
    return jsondata['reply']

def modify_grps(body, headers, zbotID, grpID):
    print LL.BASE_URL + 'usergroups/' + grpID + '/modify/' + zbotID
    jsondata = LL.invoke_rest('PUT', LL.BASE_URL + 'usergroups/' + grpID + '/modify/' + zbotID, body, headers)   
    return jsondata['reply']

def set_groups(body, headers, zviceID):
    return LL.invoke_rest('POST', LL.BASE_URL + 'usergroups/add/' + zviceID, json.dumps(body), headers)

if __name__ == '__main__':
        
        # i must login
        headers, headers1 = LL.req_headers()

        # createGroups = True
        hasHeader = 'Y'
        createGroups = False

        addUsers = True
        # addUsers = False

        # addUserGrps = True
        addUserGrps = False
        print "Zbot ID : " +LL.zbotID
        print "URL : " +LL.BASE_URL
        usergroups = getAllUserGroups(headers1, LL.zbotID)
        groups =  json.loads(usergroups)['output']['usergroup']
        for k, v in groups.items():
            print k

        ## create the groups
        #### the file contains a new user group name on each line
        if createGroups == True:
# <<<<<<< HEAD
# <<<<<<< HEAD
            tmpfile = "C:\Users\User\Dropbox\Zestl-scripts\millennium\script_inputs\NIO_user_groups.csv"
# =======
            # tmpfile = "/Users/sujoychakravarty/Dropbox/Zestl-scripts/millennium/script_inputs/SportsAndHobbiesStructure_ug.csv"
# >>>>>>> 62250e283c75a8a1132eb66c0e5596b127e3255b
# =======
            # tmpfile = "/Users/sujoychakravarty/Dropbox/Zestl-scripts/millennium/script_inputs/userGroups.csv"
# >>>>>>> 759a935472b9a1a42258b58d29b5482a44fff032
            # tmpfile = "/home/ec2-user/python/inputs/PrePrimaryTeacherUserGroups.csv"

            with open(tmpfile, 'r') as my_file:
                data = csv.reader(my_file, delimiter=',')
                if hasHeader == "Y":
                    row1 = data.next()
                # method = "POST"
                counter = 0
                for row in data:
                    grpname = row[0].strip()
                    grpDesc = row[1]
                    print grpname
            # go ahead and create those groups

            # for grpname in groupnames:
                    counter += 1
                    print counter
                    if grpname == "":
                        print "blank grp ignoring"
                    else:
                        body =  {'groupName': grpname, 'groupDesc': grpDesc}
                        print " === adding new grp " + grpname
                        print set_groups(body, headers1, LL.zbotID)

        ### end create groups

        if addUsers == True:
# <<<<<<< HEAD
# <<<<<<< HEAD
            fname = "C:\Users\User\Dropbox\Zestl-scripts\millennium\script_inputs\Add_users_to_usergroups.txt"
# =======
#             fname = "/Users/sujoychakravarty/Dropbox/Zestl-scripts/millennium/script_inputs/SportsAndHobbiesStructure_sport.txt"
# >>>>>>> 62250e283c75a8a1132eb66c0e5596b127e3255b
# =======
#             fname = "/Users/sujoychakravarty/Dropbox/Zestl-scripts/millennium/script_inputs/userGroups_users.txt"
# >>>>>>> 759a935472b9a1a42258b58d29b5482a44fff032
            # fname = = "/home/ec2-user/python/inputs/PrePrimaryTeacherUserGroups.csv"
            grpvals = json.loads(usergroups)
            print "=======================****"
            grps = grpvals['output']
            grpname = grps['usergroup']

            # print grpname
            print " groups : %s " % grpname.keys()
            print "=======================****"
            # print grpname
            for k, v in grpname.items():
                print (k)
            dict1 = grpname
            print dict1
            counter = 0
            with open(fname, 'r') as f:
                for line in f:
                    counter += 1
                    print counter
                    needs = line.split('\t')
                    trialgrp = needs[1].strip()
                    originalgrp = needs[0].strip()

                    zvice = needs[0].strip()
                    print "trialgrp " +  trialgrp
                    # print "dict 1 : " + dict1
                    # for key in dict1.keys():
                    #     print "the key name is" + key + "and its value is" + dict1[key]
                    grpID = dict1[trialgrp]
                    # print zvice
                    # print trialgrp
                    body = { 'grpUserZviceID'  : zvice}
                    print "Adding " + zvice + " to group " + trialgrp + " which has groupID = " + str(grpID)
                    add_user(json.dumps(body), headers1, LL.zbotID, str(grpID))

        if addUserGrps == True:
            fname = "/Users/sujoychakravarty/Dropbox/Zestl-scripts/millennium/script_inputs/UserGroupsInUserGroups_13Oct.txt"
            # fname = = "/home/ec2-user/python/inputs/PrePrimaryTeacherUserGroups.csv"
            grpvals = json.loads(usergroups)
            print "=======================****"
            grps = grpvals['output']
            grpname = grps['usergroup']

            print grpname
            print " groups : %s " % grpname.keys()
            print "=======================****"
            # print grpname
            for k, v in grpname.items():
                print (k)
            dict1 = grpname
            print dict1
            counter = 0
            with open(fname, 'r') as f:
                for line in f:
                    counter += 1
                    print counter
                    needs = line.split('\t')
                    childgrp = needs[1].strip()
                    parentgrp = needs[0].strip()

                    zvice = needs[0].strip()
                    grpID = dict1[parentgrp]
                    body = {'grpUserGroupID': dict1[childgrp]}
                    print "Adding " + childgrp + " to group " + parentgrp + " which has groupID = " + str(grpID)
                    add_usergrps_grps(json.dumps(body), headers1, LL.zbotID, str(grpID))



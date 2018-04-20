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
    jsondata = LL.invoke_rest('GET', LL.BASE_URL + 'usergroups/' + zbotID + "?filter={\"limit\":1000,\"offset\":0}", None, headers)
    return jsondata['reply']

def add_user(body, headers, zbotID, grpID):
    jsondata = LL.invoke_rest('POST', LL.BASE_URL + 'usergroups/' + grpID + '/user/add/' + zbotID, body, headers)
    
    print "User Group API response : Code : " + str(jsondata['code'])
    print "======================="
    print jsondata['reply']
    print "======================="
    return jsondata['reply']

def add_usergrps_grps(body, headers, zbotID, grpID):
    jsondata = LL.invoke_rest('POST', LL.BASE_URL + 'usergroups/' + grpID + '/usergroup/add/' + zbotID, body, headers)
    print "User Group API response : Code : " + str(jsondata['code'])
    print "======================="
    print jsondata['reply']
    print "======================="
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
        hasHeader = 'N'
        createGroups = False

        addUsers = True
        # addUsers = False

        # addUserGrps = True
        addUserGrps = False
        usergroups = getAllUserGroups(headers1, LL.zbotID)
        groups =  json.loads(usergroups)['output']['usergroup']
        for k, v in groups.items():
            print k

        ## create the groups
        #### the file contains a new user group name on each line
        if createGroups == True:
            tmpfile = "C:/Users/User/Dropbox/Zestl-scripts/millennium/script_inputs/IndusNewUserGroups-29Dec.csv"
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
            # fname = "/Users/sujoychakravarty/Dropbox/Zestl-scripts/millennium/script_inputs/userGroups_users.txt"
            fname = "C:\Users\User\Dropbox\Zestl-scripts\millennium\script_inputs\lavas_add_to_user_group.txt"
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
                    trialgrp = needs[1].strip()
                    originalgrp = needs[0].strip()

                    zvice = needs[0].strip()
                    grpID = dict1[trialgrp]
                    body = { 'grpUserZviceID'  : zvice}
                    print "Adding " + zvice + " to group " + trialgrp + " which has groupID = " + str(grpID)
                    add_user(json.dumps(body), headers1, LL.zbotID, str(grpID))

        if addUserGrps == True:
            # fname = "/Users/sujoychakravarty/Dropbox/Zestl-scripts/millennium/script_inputs/UserGroupsInUserGroups_13Oct.txt"
            fname = "C:/Users/User/Dropbox/Zestl-scripts/millennium/script_inputs/IndusUserGroupsInUserGroups-29Dec.txt"
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
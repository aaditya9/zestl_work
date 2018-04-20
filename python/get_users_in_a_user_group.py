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
import lib.login_prod as LL


#def getUsersInGroup(headers, grpID, zbotID):
#    jsondata = LL.invoke_rest('GET', LL.BASE_URL + 'usergroups/' + grpID + '/' + zbotID, None, headers)
#    # jsd = json.loads(jsondata)
#    return jsondata
#    

#
#def add_user(body, headers, zbotID, grpID):
#    jsondata = LL.invoke_rest('POST', LL.BASE_URL + 'usergroups/' + grpID + '/user/add/' + zbotID, body, headers)
#    
#    # print "User Group API response : Code : " + str(jsondata['code'])
#    # print "======================="
#    # print jsondata['reply']
#    # print "======================="
#    return jsondata['reply']
#
#   
#   
#def add_usergrps_grps(body, headers, zbotID, grpID):
#    jsondata = LL.invoke_rest('POST', LL.BASE_URL + 'usergroups/' + grpID + '/usergroup/add/' + zbotID, body, headers)
#    print "User Group API response : Code : " + str(jsondata['code'])
#    print "======================="
#    print jsondata['reply']
#    print "======================="
#    return jsondata['reply']
#
#
#def modify_grps(body, headers, zbotID, grpID):
#    print LL.BASE_URL + 'usergroups/' + grpID + '/modify/' + zbotID
#    jsondata = LL.invoke_rest('PUT', LL.BASE_URL + 'usergroups/' + grpID + '/modify/' + zbotID, body, headers)   
#    return jsondata['reply']
    
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
    
if __name__ == '__main__':
    
    # i must login
    headers, headers1 = LL.req_headers()
    
    #take group name from prompt
    parser = argparse.ArgumentParser()
    parser.add_argument('-userGrpName', nargs=1, type=str, required=True, dest='userGrpName', help = 'Provide user group name')
    args = parser.parse_args()
    
    inputGrpName = args.userGrpName[0]
    print "User Group Name : " + inputGrpName
    
    f1=open('./tempfiles/jsonout', 'w')
    #get all user groups information
    usergroups = getAllUserGroups(headers1, LL.zbotID)
    grpvals = json.loads(usergroups)
    grps = grpvals['output']
    grpname = grps['usergroup']

    # get group number of group whose data is required
    for x in grpname:
        if x == inputGrpName :
            print "group found: ", x, " ", grpname[x]
            
            #get group details
            grpdetails = json.loads(getUsersInGroup(headers1, str(grpname[x]) ,LL.zbotID))    
            grpdetails = grpdetails['output']['groupdetails']
            for y in grpdetails:
                print y
                # check if group contains groups        
                if y == 'groups' :
                    groups = grpdetails[y]
                    for z in groups:
                        get_users_in_nested_groups(f1, z,grpname)
                        
                if y == 'users' :
                    users = grpdetails[y]
                    for z in users:
                        f1.write(z + "\t" + users[z] + "\n")
  #                      print z, " ", groups[z]
 #                   print groups
#                    for z in grpname:
#                        print z, " ", grpname[z]
 #           grpdetails = grpdetails['data']
#            print grpdetails
#            f1=open('./tempfiles/jsonout', 'w')    
#            print >> f1, grpdetails     
            break
    
    f1.close()
 #   print grpname['Teachers']
             #
 #       f1=open('./tempfiles/jsonout', 'w')    
 #       print >> f1, grpname      
        # ## the response is ugly - so i'll housekeep it
        
#        grpvals = json.loads(usergroups)
#        print "=======================****"
#        grps = grpvals['output']
#        grpname = grps['usergroup']
#        
#        for k, x in grpname.items():
#            if "-" in k:
#                classname = "Class " + re.sub(r'(\w+)\-(\w+)',r'\1\2',k)
#                print (k, "hi there", x)
#                grpID = str(x)
#                # print grpID
#                body = { "groupName" : classname}
#                response = modify_grps(json.dumps(body), headers1, LL.zbotID, grpID)
#                print response
                # print classname
        
        # grpID = '60'
        # body = { "groupName" : "Class 1A"}
        # response = modify_grps(json.dumps(body), headers1, LL.zbotID, grpID)
        # print response
        # 
        
 # Modify a User Group
 #    Method : POST
 #    URI : /:version/usergroups/:GroupID/modify/:ZviceID
 #    Params:
 #   	 "groupName"    : <New Group Name>
 #    

        
        # grpdetails = getUsersInGroup(headers1, "292" ,LL.zbotID)
        # print grpdetails
        # grpd = json.loads(grpdetails['reply'])        
        # grpd = grpd['output']
        # grpd = grpd['groupdetails']
        # print len(grpd)
        # if (len(grpd) > 0):
        #     print "long"
        # print "=========###########=============="
        # print grpd
        #
        
        #############start here for details of users in a group
        # for k, v in grpname.items():
        #     print "=========###########=============="
        #     print (k)
        #     print (v)
        #     grpdetails = getUsersInGroup(headers1, str(v) ,LL.zbotID)
        #     if(grpdetails['code'] == 200):
        #         print "=================================="
        #         grpd = json.loads(grpdetails['reply'])        
        #         grpd = grpd['output']
        #         grpd = grpd['groupdetails']
        #         if (len(grpd) > 0):
        #             if 'users' in grpd.keys():
        #                 # print "found users"
        #                 grpd = grpd['users']
        #                 for k, v in grpd.items():
        #                     print (k, v)
        #             else:
        #                 for k, v in grpd.items():
        #                     print (k, v)
        #                     
                            
        ######### end details of users in a group
        
        
        
                # # if (len(grpd) == 1):
                # #     for k, v in grpd.items():
                # #         print (k, v)
                # # 
        # 
        # 
        # print grpname
        # print " groups : %s " % grpname.keys()
        # print "=======================****"
        # for k, v in grpname.items():
        #     print (k)
        # groupA = groupnames.split("\"")
        # groupA = [w.replace(':', '') for w in groupA]
        # groupA = [w.replace(',', '') for w in groupA]
        
        ## and create the key value pairs
        # dict1 = dict(zip(groupA[1::2],groupA[2::2]))
        # dict1 = grpname
        # print grpname
        # 
        # grpdetails = getUsersInGroup(headers1, '162' ,LL.zbotID)
        # 
        # print "=========#####=============="
        # grpd = json.loads(grpdetails['reply'])        
        # grpd = grpd['output']
        # grpd = grpd['groupdetails']
        # grpd = grpd['users']
        # for k, v in grpd.items():
        #     print (k, v)
       
        #dict1 is the golden dictionary for this script now
        
        # now open that file specified on the command line format of which is
        # zvice_id   group_name
        # 
        # with open(sys.argv[1], 'r') as f:
        #     for line in f:
        #         needs = line.split('\t')
        #         trialgrp = needs[1].strip()
        #         originalgrp = needs[0].strip()
        #         if len(originalgrp) > 0 :
        #             g1 = grpname[originalgrp]
        #             print g1
        #         if len(trialgrp) > 0:
        #             grpID = grpname[trialgrp]
        #             
        #             print str(g1)
        #             print str(grpID)
        #             body = { "grpUserGroupID" : str(g1) }
        #             add_usergrps_grps(json.dumps(body), headers1, LL.zbotID, str(grpID))
        #                         
        #             
        #         zvice = needs[0]
        #         grpID = dict1[trialgrp]
        #         body = { 'grpUserZviceID'  : zvice}
#    	 "grpUserGroupID" : <UserGroupID>
# add_usergrps_grps
        #         add_user(json.dumps(body), headers1, LL.zbotID, str(grpID))
        # 
        

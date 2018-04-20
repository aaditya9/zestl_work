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

import lib.login1 as LL

def getAllUserGroups(headers, zbotID):
    jsondata = LL.invoke_rest('GET', LL.BASE_URL + 'usergroups/' + zbotID, None, headers)
    
    print "User Group API response : Code : " + str(jsondata['code'])
    print "======================="
    print jsondata['reply']
    print "======================="
    return jsondata['reply']

def add_user(body, headers, zbotID, grpID):
    jsondata = LL.invoke_rest('POST', LL.BASE_URL + 'usergroups/' + grpID + '/user/add/' + zbotID, body, headers)
    
    print "User Group API response : Code : " + str(jsondata['code'])
    print "======================="
    print jsondata['reply']
    print "======================="
    return jsondata['reply']

def expand(std):
        if std == "1" or std == "2" or std == "3" or std == "4":
            vals = [std+'A', std+'B', std+'C', std+'D', std+'E', std+'F']
        if std == "5" or std == "6" or std == "7" or std == "8" or std == "9":
            vals = [std+'A', std+'B', std+'C', std+'D', std+'E']
        if std == "10":
            vals = [std+'A', std+'B', std+'C']
        # "2": "green",
        # "3": "blue",
        # "4": "yellow",
        # 
        return vals # if the house is not assigned - then use "not assigned" as value.

def gen_grpfile():
    with open("tmpfile", 'w') as fw:
        with open(sys.argv[1], 'r') as f:
            grouplist = []
    
            for line in f:
                attributes = line.split('\t')
                # print attributes
                if len(attributes[3]) :
                    classes = attributes[3].split(',')
                else :
                    del classes[:]
                if len(attributes[4]) :
                    classes = classes + attributes[4].split(',')
                if len(attributes[5]) :
                    subjects = attributes[5].split(',')
                if len(attributes[2]) :
                    typ = attributes[2].split(',')
                    
    # define all
    # 1-4 (F) 5-9(E) 10(C) 
                tagID = attributes[12].strip()
                for i in range(0,len(classes)):
                    if 'AL' in classes[i]:
                        # classes.remove(classes[i])
                        expander = classes[i].replace("\"","").split()
                        # classes.remove(classes[i])
                        expandedString = expand(expander[1])
                        for j in range (0, len(expandedString)):
                            fw.write (tagID + "\t" + "Teachers " + expandedString[j].strip() + "\n")
                            if "Teachers " + expandedString[j].strip() in grouplist:
                                k = 0
                            else:
                                grouplist.append("Teachers " + expandedString[j].strip())
                        # print expandedString
                    else :
                        fw.write (tagID + "\t" + "Teachers " + classes[i].replace("\"","").strip() + "\n")
                        if "Teachers " + classes[i].replace("\"","").strip() in grouplist:
                            k = 0
                        else:
                            grouplist.append("Teachers " + classes[i].replace("\"","").strip())
                for i in range(0, len(subjects)):    
                    fw.write (tagID + "\t" + "Teachers " + subjects[i].replace("\"","").strip() + "\n")
                    if "Teachers " + subjects[i].replace("\"","").strip() in grouplist:
                        k = 0
                    else:
                        grouplist.append("Teachers " + subjects[i].replace("\"","").strip())
                for i in range(0, len(typ)):    
                    fw.write (tagID + "\t" + "Teachers " + typ[i].replace("\"","").strip() + "\n")
                    if typ[i].replace("\"","").strip() in grouplist:
                        k = 0
                    else:
                        grouplist.append(typ[i].replace("\"","").strip())
            return grouplist


def set_groups(body, headers, zviceID):
    return LL.invoke_rest('POST', LL.BASE_URL + 'usergroups/add/' + zviceID, json.dumps(body), headers)



if __name__ == '__main__':
    
        grplist = gen_grpfile()
        print grplist
              
        # i must login
        headers, headers1 = LL.req_headers()
 
         #This section should only be use if new groups must be added
        ####################################
        # with open("tmpfile", 'r') as my_file:
        #     groupnames = my_file.read().split()
        #     print groupnames
        # go ahead and create those groups    
        # for grpname in grplist: 
        #     body =  {'groupName': grpname}
        #     print set_groups(body, headers1, LL.zbotID)
        # 
        
        usergroups = getAllUserGroups(headers1, LL.zbotID)
        
        ## the response is ugly - so i'll housekeep it
        groupnames = re.sub(r'.*output\"\:\{\"usergroup\"\:\{(.*)\}\}.*', r'\1', usergroups)
        groupA = groupnames.split("\"")
        groupA = [w.replace(':', '') for w in groupA]
        groupA = [w.replace(',', '') for w in groupA]
        
        ## and create the key value pairs
        dict1 = dict(zip(groupA[1::2],groupA[2::2]))
        
        dict1 is the golden dictionary for this script now
        
        # now open that file specified on the command line format of which is
        # zvice_id   group_name
        
        with open("tmpfile", 'r') as f:
            for line in f:
                needs = line.split('\t')
                trialgrp = needs[1]
                zvice = needs[0]
                grpID = dict1[trialgrp]
                body = { 'grpUserZviceID'  : zvice}
                add_user(json.dumps(body), headers1, LL.zbotID, json.dumps(str(grpID)))
        
        

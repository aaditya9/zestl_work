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

#######################
#use correct login file
import lib.login_mns_prod as LL
#######################
    
def getAllUserGroups(headers, zbotID):
    # jsondata = LL.invoke_rest('GET', LL.BASE_URL + 'usergroups/' + zbotID, None, headers)
    jsondata = LL.invoke_rest('GET', LL.BASE_URL + 'usergroups/' + zbotID + "?filter={\"limit\":1000,\"offset\":0}",
                              None, headers)
    return jsondata['reply']

if __name__ == '__main__':
    
    # i must login
    headers, headers1 = LL.req_headers()
        
    # f1=open('./tempfiles/all_user_grps', 'w')
    f1 = open('C:\Users\Minal Thorat\MINAL OFFICE DATA\minal\group', 'w')
    #get all user groups information
    usergroups = getAllUserGroups(headers1, LL.zbotID)
    grpvals = json.loads(usergroups)
    grps = grpvals['output']
    grpname = grps['usergroup']

    for x in grpname:
        print x
        f1.write(x + "\n")
            
    f1.close()

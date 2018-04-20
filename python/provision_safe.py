
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
import StringIO
import itertools
from fuzzywuzzy import fuzz
from urllib import urlopen
from datetime import datetime


import hashlib\

import lib.login_admin as LL

def hit_url_method(body, headers, method, BASE_URL):
    jsondata = LL.invoke_rest(method, BASE_URL, json.dumps(body), headers)
    return jsondata['reply']



def registerZvice(headers, body, zviceID):
    return LL.invoke_rest('PUT', LL.BASE_URL + 'zvice/register/' + zviceID, body, headers)

def getBaseStructure(zbotID, headers1):
    url = LL.BASE_URL + 'zvice/detailscard/' + zbotID
    RequestBody = {}
    response = hit_url(RequestBody, headers1, zbotID, url)
    return response



def hit_url(body, headers, zbotID, BASE_URL):
    jsondata = LL.invoke_rest('POST', BASE_URL, json.dumps(body), headers)
    return jsondata['reply']


def getPublicIp():
    data = str(urlopen('http://checkip.dyndns.com/').read())
    # data = '<html><head><title>Current IP Check</title></head><body>Current IP Address: 65.96.168.198</body></html>\r\n'

    return re.compile(r'Address: (\d+\.\d+\.\d+\.\d+)').search(data).group(1)


def getAllUserGroups(headers, zbotID, BASE_URL):
    jsondata = LL.invoke_rest('GET', BASE_URL + 'usergroups/' + zbotID, None, headers)
    #
    # print "User Group API response : Code : " + str(jsondata['code'])
    # print "======================="
    # print jsondata['reply']
    # print "======================="
    return jsondata['reply']


def change_view_permissions_fullurl(body, headers, BASE_URL):
    jsondata = LL.invoke_rest('POST', BASE_URL , json.dumps(body), headers)
    return jsondata['reply']

#
# ipAddress = getPublicIp()
#
# print ipAddress
# ItagID = "DWUL75YCZN4JS"
# ItagID = "A7AMRJC487L5Q"    #Sayali Prod# sidhharth test
# ItagID = "D9WXJHXE6WQEB"
# ItagID = "6KC8DZ5P5CXAC" ##Amol Prod
# ItagID = "3U65UQ7KLYGEB"  ### Nitin prod
# ItagID = "XGUJNGG9N4GEZ"  ### sujoy@silabtech.com
# ItagID = "A4TDL84AV6YWE"  ## manasi test
ItagID = "D9WXJHXE6WQEB"  ####Manasi prod
# ItagID = "7U8XWW4N3HZX8"   ###Sidhharth
# ItagID = "3K8FG6FULGER6"
# ItagID = "A4TDL84AV6YWE"    #demo manasi
# ItagID = "7Q879NCUXF7BM"    ###Radhika
# ItagID = "65WD7PCYB7HTE"    ### Pallavi Test
# ItagID = '9J5EDAR3Y2PZA'    ####Millenium
# ItagID = "EGF3JG2V63E5B"    ####Sayali test
# ItagID = "DWUL75YCZN4JS"    #Sayali DEv
# ItagID = "4KBW5GZ4XP4RX"   ###Minaltest
# ItagID = "9ED7VXL4BF4TN"    ###ShripadTest
# ItagID = "6APSM4B85ARZW"    ## lankesh test
# ItagID = "49N5G8CL9BE83"    ###akshay dev
# ItagID = "8CKZG8CKKMAC7"    ###MInalDEv
# ItagID = "4V3VGHPVUJPYT"    ## Hardik Prod
# ItagID = "26RXGKHU6263A" ## Murtaza Prod
# ItagID = "3JBXMYD8WR978" ##Aditya Paralikar
# ItagID = "479YUDW4ZM59G"    #### Aditya 2
# ItagID = "FNB5W476FG7KM"    #RADHIKA test
# ItagID = "X4WNG3EBKMTJH" #Sachin test
# ItagID = "W965CATJTM3EL"
SItagID1 = ""
SItagID2 = ""

storeDir = "~/Dropbox/Zestl-Deployment/issued_tags/test/"
# storeDir = "/Users/sujoychakravarty/Dropbox/Zestl-share/scripts/issued_tags/demo/"
storeDir = "C:/Users/Minal Thorat/Dropbox/Zestl-Deployment/issued_tags/"



passkey = str(raw_input("Enter password : "))
print "... Working ....."
headers, headers1 = LL.req_headers(passkey)

#
#
# print "===========headers==========="
# print headers1
# print "===========headers==========="
#

reqTag  = 0
CustomerName = str(raw_input("Enter customer name : "))
addTags = int(raw_input("Do you want to \n 1) add a new customer  OR \n 2) add more tags to an existing customer OR \n 3)Request more tags for an existing customer \n : "))
if addTags != 1 and addTags != 2 and addTags != 3:
    sys.exit("illegal input")

Maxtags = int(raw_input("Max number of tags allowed : "))
NeedTags = str(raw_input("Do you need extra tags - press Y for yes : "))


if NeedTags == 'Y' or NeedTags == 'y':
    reqTag  = int(raw_input("How many extra tags do you need: "))


Cname = re.sub('[\W_]+', '', CustomerName)
# print Cname
# print Maxtags
if addTags == 1:
    data = {}

    body = { "DisplayName": Cname, "MaxAllowedTags": Maxtags}

    url = LL.BASE_URL +  "customers"
    print url
    method = "POST"

    jsonreply = hit_url_method(body, headers1, method, url)

    print jsonreply
    jsondata =  json.loads(jsonreply)
    ZbotID =  jsondata['data'][0]['ZbotID']



    # ZbotID = "ETSUXNAFXTH5W"
    print ZbotID

    usergroups = getAllUserGroups(headers1, ZbotID, LL.BASE_URL)

    grplist = json.loads(usergroups)['output']['usergroup']

    print grplist['Linked Users']



    # ZbotID = 'A4CJ2VHTTJS9Y'

    # url = LL.BASE_URL + "zvice/register_pre"
    # body = {"zviceid" : ZbotID, "title" : CustomerName,  "zvicetype" : "ZTAG", "zviceinfo" : "enter description here", "category" : "ORGANISATION",  "lat" : 'lat', "long" : "long", "zviceloc" : '--', "zvicelink" : 'NEW'}
    #
    # method = "PUT"
    #
    # jsonreply = hit_url_method(body, headers1, method, url)
    # print jsonreply

    print "============================="

    url = LL.BASE_URL + "zvice/interaction/" + ZbotID
    method = "POST"
    body = {"title" : CustomerName, "desc" : CustomerName,  "interactionID" : "CommonInteraction_INTERACTION_TYPE_UPLOAD_BASECARD_IMG"}
    if re.match(r'\w{13}', ItagID):
        body['PrimaryOwnerITagID'] = ItagID
    if re.match(r'\w{13}', SItagID1):
        body['SecondaryOwnerITagID1'] = SItagID1
    if re.match(r'\w{13}', SItagID2):
        body['SecondaryOwnerITagID2'] = SItagID2
    jsonreply = hit_url_method(body, headers1, method, url)
    print jsonreply
    print "============================="
    print " ===== changing permissions ============="
    # post /:version / card / permissions /:ZviceID

    grpID = grplist['Linked Users']
    actionType = 'VIEW'
    RequestBody = {"opType": "1",
                   "actionType": actionType,
                   "groupID": grpID,
                   "cardID": "",
                   "cardType": ""
                   }
    zbotID = ZbotID
    zviceID = ZbotID
    # url = LL.BASE_URL + 'zvice/interaction/' + zviceID
    url = LL.BASE_URL + "card/permissions/" + ZbotID
    response = change_view_permissions_fullurl(RequestBody, headers1, url)
    print response

    print "====== Permissions changed ==========="



if addTags == 3:
    method = "GET"
    url = LL.BASE_URL + 'customers'
    body = {}
    print " .... Working ....."
    jsonreply = hit_url_method(body, headers1, method, url)
    print jsonreply
    jsonreply = json.loads(jsonreply)
    for elements in jsonreply['data']:
        # print elements['mapped_customers']
        try:
            for cust in elements['mapped_customers']:
                if fuzz.partial_ratio(CustomerName, cust['Title']) > 70:
                    confirm = str(raw_input("Is \"" + cust['Title'] +" \" the customer you are interested in : "))
                    if confirm == 'y' or confirm == 'Y':
                        ZbotID = cust['ZbotID']
        except KeyError:
            print "keyerror"
# else:
#     print "---------------------------"


if addTags == 2:
    method = "GET"
    url = LL.BASE_URL + 'customers'
    body = {}
    print " .... Working ....."
    jsonreply = hit_url_method(body, headers1, method, url)
    jsonreply = json.loads(jsonreply)
    for elements in jsonreply['data']:
        # print elements['mapped_customers']
        try:
            for cust in elements['mapped_customers']:
                if fuzz.partial_ratio(CustomerName, cust['Title']) > 70:
                    confirm = str(raw_input( "Do you want to change \"" + cust['Title'] + "\" maximum number of tags from " + str(elements['MaxAllowedTags']) + " to " + str(Maxtags) + ": " ))
                    if confirm == 'y' or confirm == 'Y':
                        body['DisplayName'] = elements['DisplayName']
                        body['MaxAllowedTags'] = Maxtags
                        body['ZbotID'] = cust['ZbotID']
                        url = LL.BASE_URL + "customers/" + str(elements['CustomerID'])
                        method = "PUT"
                        print cust['ZbotID']
                        ZbotID = cust['ZbotID']
                        jsonreply = hit_url_method(body, headers1, method, url)
                        print jsonreply


                    # print (cust['Title'], fuzz.partial_ratio(CustomerName, cust['Title']))
                    # print (elements['DisplayName'], elements['CustomerID'], cust['ZbotID'])

        except KeyError:
            print "keyerror"


if NeedTags == 'Y' or NeedTags == 'y':
    url = LL.BASE_URL + "nexttag/" + ZbotID + "/tags/" + str(reqTag)
    method = "GET"
    body = {}
    jsonreply = hit_url_method(body, headers1, method, url)
    print jsonreply
    jsonreply = json.loads(jsonreply)
    tagIDs = "\n".join(str(x) for x in jsonreply['available_tagIDs'])
    now = str(datetime.now())
    now = re.sub(r' ', r'_', now)
    now = re.sub(r'\-', r'', now)
    now = re.sub(r'\:', r'', now)
    now = re.sub(r'\.', r'', now)
    now.replace("-", "")
    now.replace(":", "")
    now.replace(".", "")
    writeFileName = storeDir + Cname + now + ".txt"
    with open(writeFileName, 'w') as wf:
        wf.write(tagIDs)
    print tagIDs
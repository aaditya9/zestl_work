


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
import csv
import StringIO
import itertools
from fuzzywuzzy import fuzz
import hashlib\

import lib.login_generic as LL









def getNextTag(ZbotID, base_url, headers1):
    url = base_url + "nexttag/" + ZbotID + "/tags/1"
    method = "GET"
    body = {}
    jsonreply = hit_url_method(body, headers1, method, url)
    return jsonreply


def hit_url_method(body, headers, method, BASE_URL):
    jsondata = LL.invoke_rest(method, BASE_URL, body, headers)
    return jsondata['reply']



refcount = 0
tagfound = 0
taginCol = 1
moreInfo = [None] * 100
print "This script adds users to a business"
## take all the necessary inputs
# userName = str(raw_input("Enter username : "))
userName = "manasi@zestl.com"
# password = str(raw_input("Enter password : "))
password = "Zestl123"
# whichServer = int(raw_input("Which server\n1)Prod\n2)Test\n3)Dev\n4)demo\n : "))
whichServer = 1
# ZbotID = str(raw_input("Enter tag ID of business: "))
ZbotID = "6U3HP7PW3HGYY"

# IDsExist = str(raw_input("Does your xls contain tag IDs assigned already (Y for yes) : "))
IDsExist = 'n'
# filename = str(raw_input("Enter filename (full path) : "))
filename = "/Users/sujoychakravarty/Dropbox/Zestl-share/scripts/millennium/script_inputs/Member_fitbox.csv"

# Kunte_pyc.csv
# Kunte_walve.csv
# Kunte_aundh.csv

if whichServer == 1:
    base_url = "https://twig.me/v1/"
elif whichServer == 2:
    base_url = "http://52.8.240.85/v1/"
elif whichServer == 3:
    base_url = "http://www.twig-me.com/v1/"
else:
    sys.exit("This server does not exist")

headers, headers1 = LL.req_headers(userName, password, ZbotID, base_url)

outfilename = re.sub(r'\.', r'OUT.', filename)
print outfilename

with open(outfilename, 'w') as fw:

    with open(filename, 'r') as f:
        data = csv.reader(f, delimiter=',')
        rowout1 = ""
        row1 = data.next()
        for i in range(0, len(row1)):
            rowout1 += row1[i] + ","

        fw.write(rowout1 + "\n")
        for row in data:
        ## mapping functions
            ref_no = str(row[0].strip())
            if ref_no == "":
                ref_no = "auto" + str(refcount)
                refcount += 1

### this is an important decision point and needs to be probably updated manually based on different inputs
            tagID = str(row[1].strip())
            if re.match(r'\w{13}', tagID.upper()):
                tagID = tagID.upper()
                taginCol = 1
                tagfound = 1
            else:
                print "+++++++ Tag error : illegal tag ID defined ++++++++++++++++"

            name = row[2]

            eMail = row[3]
            if eMail == "":
                eMail = userName

            # moreInfo[0] = row[4]
            # desc = row[4]
            #
            # contactMobile = row[5]
            #
            # moreInfo[1] = "DOB : " + row[6]
            #
            # moreInfo[2] = "DOJ : " + row[7]
            tag = ""
            if tagfound == 0:
                jsonreply = getNextTag(ZbotID, base_url, headers1)
                # for k, v in jsonreply.items():
                #     print k, v
                print jsonreply
                tag = json.loads(jsonreply)["available_tagIDs"]
                for val in tag:
                    row[1] = val
            rowout = ""
            for i in range(0, len(row)):
                # if i == taginCol:
                #     rowout += tag + ","
                # else:
                rowout += row[i] + ","
            fw.write(rowout + "\n")





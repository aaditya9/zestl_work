
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
import hashlib\

#import lib.login1 as LL
import lib.login1 as LL

def getBaseStructure(zbotID):
    url = LL.BASE_URL + 'zvice/detailscard/' + zbotID
    RequestBody = {} 
    response = hit_url(RequestBody, headers1, LL.zbotID, url)
    with open('tmp', 'w') as f:
        f.write(str(response))
    return json.loads(response)


def method_url(body, headers, BASE_URL, method):
    jsondata = LL.invoke_rest(method, BASE_URL, json.dumps(body), headers)
    return jsondata['reply']


def hit_url(body, headers, zbotID, BASE_URL):
    jsondata = LL.invoke_rest('POST', BASE_URL, json.dumps(body), headers)
    return jsondata['reply']


def get_emailID(jsondata, details):
    for a in jsondata['data']['elements']:
        if 'basecard' in a['cardtype']:
            for b in a['actions']:
                if "Explore" in b['title']:
                    body = {}
                    jsondata = method_url(body, headers1, b['actionUrl'], b['method'])
                    jsondata = json.loads(jsondata)
                    for c in jsondata['data']['elements']:
                        if "Contact Details" in c['title']:
                            for d in c['actions']:
                                if "Message" in d['title']:
                                    for e in d['actions']:
                                        if "Chat" in e['title']:
                                            print "%%%%%%%%%%%%%%%%%%%"
                                            mailD = json.loads(e['data'])
                                            mailD = mailD['emailto']
                                            print (a['title'], a['tagId'], mailD)
                                            # reportfile.write(a['title'] + "\t" + a['tagId'] + "\t" + mailD + "\n")
                                            details[a['title']] = [a['tagId'], mailD]

        elif 'nextcard' in a['cardtype']:
            actionUrl = a['url']
            method = 'POST'
            body = json.loads(a['content'])
            jsondata = method_url(body, headers1, actionUrl, method)
            jsondata = json.loads(jsondata)
            #
            print len(details)
            details = get_emailID(jsondata, details)
    return details


def getTagID(jsondata, details, details1):
    try :
        for a in jsondata['data']['elements']:
            if 'basecard' in a['cardtype']:
                details[a['tagId']]= a['title']
                details1[a['title']] = a['tagId']
            elif 'nextcard' in a['cardtype']:
                actionUrl = a['url']
                method = 'POST'
                body = json.loads(a['content'])
                body['pagesize'] = 5000
                jsondata = method_url(body, headers1, actionUrl, method)
                if jsondata == None:
                    return details, details1
                else:
                    jsondata = json.loads(jsondata)
                #
                if jsondata == None :
                    return details, details1
                else:
                    print len(details)
                    details, details1 = getTagID(jsondata, details, details1)
    except KeyError:
        return details, details1
    return details, details1


if __name__ == '__main__':
    cardType = {}    
    cardDetails = {}
    zbotID = LL.zbotID
    details = {}
    details1 = {}

    # timestamp = time.strftime("%d%m%Y_%H_%M_%S", time.localtime())
    # report = "tempfiles/userlist_" + timestamp
    #
    # reportfile = open (report, 'w')

    ### read the file structure into columns
      
    # i login
    headers, headers1 = LL.req_headers()
   
    # response = getBaseStructure(zbotID)
    # print response
    
    actionUrl = LL.BASE_URL + "zvice/interaction/" + zbotID
    method = "POST"
    responseBody = {'username': '', 'expired' : 'false', 'interactionID' : 'CommonInteraction_INTERACTION_TYPE_SEARCH_LIB_USER_PROFILE', "pagesize" : 5000}
    
    jsondata = method_url(responseBody, headers1, actionUrl, method)
    print jsondata
    jsondata = json.loads(jsondata)

    details, details1 = getTagID(jsondata, details, details1)
    # details = get_emailID(jsondata, details)
    
    print details


    # tempfiles / userlist_mill.csv
    with open("C:\Users\User\Dropbox\Zestl-scripts\millennium\script_inputs\Indus_22Nov.csv", 'w') as wf:
        # for t in details:
        #     print t

        for k, v in details.items():
            wf.write(k + "," + v + "\n")
    #
    # reportfile.close()
    # print "Check log at: ", report
 
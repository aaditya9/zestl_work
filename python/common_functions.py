
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
import csv
import StringIO
import itertools
import hashlib\

import lib.login1 as LL

def hit_url(method, BASE_URL, body, headers):
    jsondata = LL.invoke_rest(method, BASE_URL, body, headers)
    return jsondata['reply']
    
    
def getBaseCards(content):
    i = 0
    line = {}
    cardFound = 0
    cards = {}
    j = 0
    for v in content:
        # cardfound tells that a card at base level is found
        if cardFound == 1 and re.search("card", v[0].lower()): # a next card/ department found
            j += 1 # the next card
            line[i] = v
            cards[j] = v # add to the next card
            lencard = len(cards[j])
        elif cardFound == 1 and v[0] != '': #this is part of the existing card
            line[i] = v
            try:
                cards[j].append(v) # so append
            except KeyError:
                cards[j] = v
                lencard = len(cards[j])
        elif cardFound == 0 and re.search("card", v[0].lower()): # a new card was just found
            # print v[0]
            line[i] = v
            cardFound = 1
            j += 1  # increment the new card counter
            cards[j] = v
            lencard = len(cards[j])
            
        elif v[0] == "" :
            line[i] = v
            cardFound = 0
            # j += 1
            
        # else 
        i += 1
    # print cards
    print " ============================== "
    return cards, line, lencard
    



def returnCardcustomStatus(cards):
    for x in cards:
        title = x['title']
        cardtype = x['cardtype']
        print (title, cardtype)
        if re.search('basecard', cardtype):
            for a in x['actions']:
                if re.search('Customize', a['title']):
                    actionUrl = a['actionUrl']
                    body = json.loads(a['data'])
                    method = a['method']
                    print (actionUrl, body, method)
                    return method_url(body, headers1, actionUrl, method)

def returnJsonParams(cards, whichCardType):
    for x in cards:
        title = x['title']
        cardtype = x['cardtype']
        print (title, cardtype)
        if re.search('basecard', cardtype):
            for a in x['actions']:
                if re.search('Add Cards', a['title']):
                    for b in a['actions']:
                        if re.search(whichCardType.lower(), b['title'].lower()):
                            actionUrl = b['actionUrl']
                            method = b['method']
                            for k in b['inputs']:
                                for v in k['properties']:
                                    if v['name'] == 'id':
                                        keys = v['value']
                                        ks = 1
                                    elif v['name'] == 'hint' and ks == 1:
                                        values = "user defined"
                                        ks = 0
                                        body[keys] = values
                                    elif re.search('fault', v['name']) and ks == 1:
                                        values = v['value']
                                        ks = 0
                                        body[keys] = values
                                    elif v['name'] == 'text' and ks == 1:
                                        values = 'user input'
                                        ks = 0
                                        body[keys] = values
                                    elif v['name'] == 'list' and ks == 1:
                                        values = 'user selected'
                                        ks = 0
                                        body[keys] = values
                                    elif (v['name'] == 'hidden') or (v['name'] == 'idtype'):
                                        abc  = 0
                                    elif ks == 0:
                                        abc = 0
                                    else:
                                        values = "failed all else " + v['name']
                                        ks = 0
                                        body[keys] = values
                            return body, actionUrl, method         

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

#with open (sys.argv[1], 'r') as rf:
#    
#    headers, headers1 = LL.req_headers()
#    
#    
#    abc = 0
#    ks = 1
#    body = {}
#    
#    zbotID = LL.zbotID
#    
#    response = getBaseStructure(zbotID)
#    
#    cards = response['data']['elements']
    # whichCardType = 'department'
    # title = 'trial dept'
    # desc = 'delete'
    # zviceid = '9M9R3JXCSMMJH'
    # print any(x in whichCardType for x in ('department', 'text', 'forum', 'gallery'))
    # if (any(x in whichCardType for x in ('department', 'text', 'forum', 'gallery'))):
    #     body, actionUrl, method = returnJsonParams(cards, whichCardType)
    #     print actionUrl
    #     print body
    #     print method
    #     if('department' in whichCardType.lower()):
    #         body['title'] = title
    #         body['zviceinfo'] = desc
    #         body['zviceid'] = zviceid
    #         body['tagprofilestr'] = 'ORGANISATION'
    #         print body
    #         # response = method_url(body, headers1, actionUrl, method)
    #         # print response
    #         response = returnCardcustomStatus(cards)
    #         print "************************"
    #         print response
    #         
    #         
    # else:
    #     print "not supported"
    #     
#    content = csv.reader(rf)
#    # print content[2]
#    print "+++++++++++++++++++++++++++++++++"    
#    line = {}
#    lev1, line, lencard = getBaseCards(content)
#    print "+++++++++++++++++++++++++++++++++"    
#    print line
#    for items in lev1:
#        print lev1[items]
#
#        # for a in lev1[items]
#        whichCardType = re.sub(r'(\w+)\s+Card.*', r'\1', lev1[items][0])
#        desc = "enter a description here"
#        title = ""
#        zviceid = ""
#        body = {}
#        if (any(x in whichCardType.lower() for x in ('department', 'text', 'forum', 'gallery', 'calendar'))):
#            body, actionUrl, method = returnJsonParams(cards, whichCardType)
#            # print actionUrl
#            # print body
#            # print method
#            print whichCardType.lower()
#            if (len(lev1[items]) > lencard):
#                print lev1[items][lencard]
#                for s in lev1[items][lencard:]:
#                    print "==iiiiiiiiiiii====="
#                    print s
#                    for t in s:
#                        if 'title' in t.lower():
#                            title = re.sub(r'(.*)\(\witle\)',r'\1',t)
#                            print "Title found : " + title
#                        if 'tag' in t.lower():
#                            zviceid = re.sub(r'(.*)\(\wag\)',r'\1',t)
#                            print "tag found " + zviceid
#                        # if 'tag' in s.lower()
#            else:
#                print "No details supplied"
#            if('depart' in whichCardType.lower()):
#                body['title'] = title
#                body['zviceinfo'] = desc
#                body['zviceid'] = zviceid
#                body['tagprofilestr'] = 'ORGANISATION'
#                print "==========ddddddd============"
#                print body
#                # response = method_url(body, headers1, actionUrl, method)
#                # print response
#                # response = returnCardcustomStatus(cards)
#                # print "************************"
#                # print response
#            elif('text' in whichCardType.lower()):
#                body['title'] = title
#                body['desc'] = desc
#                print "==========ttttt============"
#                print body
#            elif('forum' in whichCardType.lower()):
#                body['text'] = title
#                body['desc'] = desc
#                print "==========fffffff============"
#                print body
#            elif('calendar' in whichCardType.lower()):
#                body['Title'] = title
#                body['Description'] = desc
#                print "==========cccccc============"
#                print body
#            elif('gallery' in whichCardType.lower()):
#                body['Title'] = title
#                body['Description'] = desc
#                print "==========ggggg============"
#                print body
#        else:
#            print "creating " + whichCardType + " is not yet supported"
#                    
#        # print cardname
#        # print lencard
#        # print (k, v)
#    # content.replace("\r","\n")
#    
#    # x,y = itertools.izip_longest(*csv.reader(rf))
#    # itertools.zip_longest
## print (x,y)

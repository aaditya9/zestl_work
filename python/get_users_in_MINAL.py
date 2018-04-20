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
import hashlib \
    # import lib.login1 as LL
import lib.login1 as LL
import common as CM


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


def getTagID(jsondata, details):
    try:
        for a in jsondata['data']['elements']:
            if 'basecard' in a['cardtype']:
                details[a['tagId']] = a['title']

            elif 'nextcard' in a['cardtype']:
                actionUrl = a['url']
                method = 'POST'
                body = json.loads(a['content'])
                body['pagesize'] = 5000
                jsondata = method_url(body, headers1, actionUrl, method)
                if jsondata == None:
                    return details
                else:
                    jsondata = json.loads(jsondata)
                #
                if jsondata == None:
                    return details
                else:
                    print len(details)
                    details = getTagID(jsondata, details)
    except KeyError:
        return details
    return details


if __name__ == '__main__':
    cardType = {}
    cardDetails = {}
    zbotID = LL.zbotID
    details = {}
    outfile = "C:\Users\Minal Thorat\Dropbox\Zestl-scripts\millennium\script_inputs\mi_prod.csv"

    headers, headers1 = LL.req_headers()

    actionUrl = LL.BASE_URL + "zvice/interaction/" + zbotID
    method = "POST"
    responseBody = {'username': '', 'expired': 'false',
                    'interactionID': 'CommonInteraction_INTERACTION_TYPE_SEARCH_LIB_USER_PROFILE', "pagesize": 5000}

    jsondata = method_url(responseBody, headers1, actionUrl, method)
    print jsondata
    jsondata = json.loads(jsondata)

    details = getTagID(jsondata, details)
    # details = get_emailID(jsondata, details)

    print details

    with open("tempfiles/userlist_mill.csv", 'w') as wf:
        for k, v in details.items():
            wf.write(k + "," + v + "\n")

    with open(outfile, "w") as of:

        for k, v in details.items():

            of.write("\n" + k + ",")
            print k
            jdata = CM.getBaseStructure(k, headers1, LL.BASE_URL)
            print jdata
            for element in jdata['data']['elements']:
                if element['cardtype'] == "basecard":
                    of.write(CM.force_decode(element['title']) + ",")
                    of.write(CM.force_decode(element['content']) + ",")
                    of.write(CM.force_decode(element['contact']) + ",")

                elif element['title'] == "Contact Details":
                    print "found"
                    for action in element['actions']:
                        if action['title'] == "Explore":
                            print "go"
                            url = action['actionUrl']
                            method = action['method']
                            body = json.loads(action['data'])
                            jsonresponse = CM.hit_url_method(body, headers1, method, url)
                            print jsonresponse
                            contact = json.loads(jsonresponse)['data']['elements'][1]['content'].split("<br>")
                            print contact
                #     url = element['cardsjsonurl']
                #     # url = element['actions']['actionUrl']
                #     body = json.loads(element['content'])
                #     method = element['method']
                #     contact = json.loads(CM.hit_url_method(body, headers1, method, url))
                #     contact = contact['data']['elements'][0]['content'].split("<br>")
                #     writecount = 0
                #     for detail in contact:
                #         if detail != "":
                #             detail = CM.force_decode(detail)
                #             of.write(detail + ",")
                #             writecount += 1
                #     if writecount == 0:
                #         of.write(",,")
                #     if writecount == 1:
                #         of.write(",")
                #
                #     # print contact
                #     print  "contacts done"
                #
                # elif element['title'] == "More Details":
                #     url = element['cardsjsonurl']
                #     body = json.loads(element['content'])
                #     method = element['method']
                #     moreDetails = json.loads(CM.hit_url_method(body, headers1, method, url))
                #     try:
                #         for detail in moreDetails['data']['elements']:
                #             of.write(
                #                 CM.force_decode(detail['title']) + " : " + CM.force_decode(detail['content']) + ",")
                #     except:
                #         print "No more details fields"
                #     print "more details done"
                #     print "done"
                #
                # elif element['title'] == "Memberships":
                #     url = element['cardsjsonurl']
                #     body = {}
                #     method = element['method']
                #     member = (CM.hit_url_method(body, headers1, method, url))
                #     # print member
                #     member = json.loads(member)
                #     try:
                #         for element in member['data']['elements']:
                #             try:
                #                 of.write(CM.force_decode(element['title']) + " : " + CM.force_decode(
                #                     element['content']) + ",")s
                #             except:
                #                 print "couldnt write"
                #     except:
                #         print "no memberships"
                #     print "memberships done"
                #     print "done"
                #
                # elif element['title'] == "Link to TwigMe User":
                #     url = element['actions'][1]['actionUrl']
                #     body = json.loads(element['actions'][1]['data'])
                #     method = element['actions'][1]['method']
                #     link = (CM.hit_url_method(body, headers1, method, url))
                #     # print link
                #     link = json.loads(link)
                #     of.write("Linked user : " + CM.force_decode(link['data']['elements'][0]['title']) + ",")
                #     print ""
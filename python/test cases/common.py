
# import json
# import base64
import time
# import urllib2
# from urllib2 import URLError
# from urllib2 import HTTPError
import requests
# import urllib
import json
# import time
# import os

import logging

def force_decode(string, codecs=['utf8', 'cp1252']):
    for i in codecs:
        try:
            return string.decode(i)
        except:
            return("")

    logging.warn("cannot decode url %s" % ([string]))



def parse_files(filename):
    with open(filename, 'r') as rf:
        for line in rf:
            if isinstance(line, str):
                line = force_decode(line)
            # print line
            try:
                line = unicode(line)
            except:
                print line
                print type(line)
                return "errors"
    return "success"

def hit_url_method(body, headers, method, BASE_URL):
    jsondata = invoke_rest(method, BASE_URL, json.dumps(body), headers)
    # print jsondata
    return jsondata['reply']

def hit_url_method_without_convesion(body, headers, method, BASE_URL):
    jsondata = invoke_rest(method, BASE_URL, body, headers)
    return jsondata['reply']

def invoke_rest(request_type, rest_url, payload=None, headers=None):
    count = 1
    while True:
        try:
            api_url = rest_url
            if request_type == 'GET':
                r = requests.get(api_url, headers=headers)

                to_ret = {'code': r.status_code, 'reply': r.text}
                return to_ret
            elif request_type == 'POST':
                r = requests.post(api_url, data=payload, headers=headers)
                to_ret = {'code': r.status_code, 'reply': r.text}
                return to_ret
            elif request_type == 'PUT':
                r = requests.put(api_url, data=payload, headers=headers)
                to_ret = {'code': r.status_code, 'reply': r.text}
                return to_ret
            else:
                return "Invalid request type ", request_type
        except Exception, e:
            print str(e)
            print headers
            print "Error in invoking " + request_type + ", " + api_url + ", Reattempting " + str(count)
            count = count + 1
            time.sleep(50.0 / 1000.0);  # Sleep 50 milli sec
            # return "Exception:", e, " in getting the API call"


def getBaseStructure(zbotID, headers1, BASE_URL):
    # print BASE_URL
    url = BASE_URL + 'zvice/detailscard/' + zbotID
    # print url
    RequestBody = {}
    method = "POST"
    response = hit_url_method(RequestBody, headers1, method, url)
    # return response
    return json.loads(response)


def EDIT_submission_using_NEW_API(BASE_URL,zviceID,headers1,form_ID,input_data,submission_ID):
    form_ID = str(form_ID)
    submission_ID = str(submission_ID)
    body = {}
    method = "GET"
    url = BASE_URL + zviceID + "/formdetails/" + form_ID
    jasub = hit_url_method(body, headers1, method, url)
    jasub = json.loads(jasub)

    body = {}
    for a in jasub['data']['form']['Elements'][0]['Elements']:
        for k, v in input_data.items():
            if k == a['ElementID']:
                body[a['FormMetaID']] = v
    method = "PUT"
    url = BASE_URL + zviceID + "/forms/" + form_ID + "/submissions/" + submission_ID
    jsonresponse = hit_url_method(body, headers1, method, url)
    return jsonresponse
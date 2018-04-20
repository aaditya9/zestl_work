import logon as LL
import common as CM
import info as info
import requests

BASE_URL = info.url
email = info.email
pwd = info.pwd
headers, headers1 = LL.req_headers(email, pwd, BASE_URL)

def membership_add(bId,title,desc):
    url = BASE_URL + "membership/" + bId
    method = "POST"
    body = {}
    body['Title'] = title
    body['Description'] = desc
    body['Fees'] = "100"
    body['Duration'] = "2"
    body['NumSessions'] = "2"
    body['SessionDuration'] = "2"
    body['SessionDurationUnit'] = None
    jsonresponse = CM.hit_url_method(body, headers1, method, url)
    return jsonresponse

def membership_delete(bId,Mem_ID):
    url = BASE_URL + "delete/membership/" + Mem_ID + "/org/" + bId
    method = "POST"
    body = {}
    jsonresponse = CM.hit_url_method(body, headers1, method, url)
    return jsonresponse

def membership_edit(bId,title,desc,Mem_ID):
    url = BASE_URL + "membership/" + Mem_ID + "/org/" + bId
    method = "PUT"
    body = {}
    body['Title'] = title
    body['Description'] = desc
    body['Fees'] = "100"
    body['Duration'] = "2"
    body['NumSessions'] = "2"
    body['SessionDuration'] = "2"
    body['SessionDurationUnit'] = None
    jsonresponse = CM.hit_url_method(body, headers1, method, url)
    return jsonresponse
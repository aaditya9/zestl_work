import requests
import json
import re
from urllib import urlopen
import csv
import time
import common as CM
import lib.login_generic as LL
import form_elements_create_using_new_struct as FORMS


def hit_url_method(body, headers, method, BASE_URL):
    jsondata = LL.invoke_rest(method, BASE_URL, json.dumps(body), headers)
    return jsondata['reply']


def registerZvice(headers, body, zviceID):
    return LL.invoke_rest('PUT', LL.BASE_URL + 'zvice/register/' + zviceID, body, headers)

def getBaseStructure(zbotID, headers1, BASE_URL):
    url = BASE_URL + 'zvice/detailscard/' + zbotID
    RequestBody = {}
    response = CM.hit_url_method(RequestBody, headers1, "POST", url)
    return response


def hit_url(body, headers, zbotID, BASE_URL):
    jsondata = LL.invoke_rest('POST', BASE_URL, json.dumps(body), headers)
    return jsondata['reply']


def getPublicIp():
    data = str(urlopen('http://checkip.dyndns.com/').read())
    return re.compile(r'Address: (\d+\.\d+\.\d+\.\d+)').search(data).group(1)


def getAllUserGroups(headers, zbotID, BASE_URL):
    jsondata = LL.invoke_rest('GET', BASE_URL + 'usergroups/' + zbotID, None, headers)
    return jsondata['reply']


def change_view_permissions_fullurl(body, headers, BASE_URL):
    jsondata = LL.invoke_rest('POST', BASE_URL , json.dumps(body), headers)
    return jsondata['reply']

def add_user(business_id,u_name,u_email):
    method = "POST"
    url = LL.BASE_URL + 'zvice/interaction/' + business_id
    body = {'zvicetype': 'ITAG', 'zviceloc': 'Pune', 'zvicelink': 'NEW', 'lat': 'lat', 'long': 'long', 'tagprofile': 0,
            'media_type': 'image/jpg',
            'media_ext': 'jpg', 'media': "", 'media_size': 0, 'zbotid': business_id}
    body['title'] = u_name
    body['linkemail'] = u_email
    body['autogentag'] = "true"
    body['interactionID'] = "CommonInteraction_INTERACTION_TYPE_CREATE_LIB_USER_PROFILE"
    jsonreply = hit_url_method(body, headers1, method, url)
    return jsonreply


BASE_URL = "http://twig-me.com/v13/"  ### dev server
zviceID = "3QVRRWHHJX3D9"  # Work flow demo department
zviceID = "WHGJ7HTVTDFH3"
email = "admin@zestl.com"
pwd = "TwigMeNow"

#
# url = BASE_URL + zviceID + "/tags/" + zviceID
# url = BASE_URL + "search/" + zviceID + "/tags/" + zviceID + "/cards"
# url = u'http://www.twig-me.com/v11/all_actions/business/WHGJ7HTVTDFH3'
# url = u'http://www.twig-me.com/v11/settings_action/business/WHGJ7HTVTDFH3'
# url = u'http://www.twig-me.com/v11/usergroups/WHGJ7HTVTDFH3'
# # url = u'http://www.twig-me.com/v11/usergroups/search/WHGJ7HTVTDFH3'
# # url = u'http://www.twig-me.com/v11/usergroups/4/WHGJ7HTVTDFH3'
# k1 = "trial_key1"
# v1 = "12"
# # url = BASE_URL + "workflow/" + zviceID + "/" + k1 + "/value/" + v1
# # url = BASE_URL + "workflow/" + zviceID + "/" + k1

headers, headers1 = LL.req_headers(email, pwd, zviceID, BASE_URL)

# url = BASE_URL + "workflow/" + zviceID + "/type"
method = 'POST'
# method = "GET"
body = { "TaggedCardIDs"  : "571, 572", "Tags" : "Minal"}
body = {"Tags" : "Ideaion:Marketing:WFID:17"}
# body = {'title' :   "Type A"}
body = {}
# body = {"cardType":"ORG_BASE_CARD"}
# body = {"businessTag":"WHGJ7HTVTDFH3"}
url = 'http://twig-me.com/v11/workflow/WHGJ7HTVTDFH3/cards'
url = u'http://www.twig-me.com/v11/workflow/WHGJ7HTVTDFH3'

url = BASE_URL + "search/" + zviceID + "/tags/" + zviceID + "/cards"
body = {'Tags': 'task:WFE1_1:WFID:62,task:WFE1_2:WFID:62,task:WFE1_3:WFID:62,task:WFE1_4:WFID:62,task:WFE1_5:WFID:62'}
url = u'http://www.twig-me.com/v13/all_actions/WHGJ7HTVTDFH3/formsubmission/23840'
url = u'http://www.twig-me.com/v13/tasks/WHGJ7HTVTDFH3/23840'
url = u'http://www.twig-me.com/v13/tasks/getsingle/WHGJ7HTVTDFH3/23841'
url = u'http://www.twig-me.com/v13/tasks/edit/WHGJ7HTVTDFH3'
body = {}


body['TaskID'] = "23841"
body['Status'] = "Assigned"
    # for gid in v:
    # try:
body['UserGroupIDLevel1'] = "4"

response = hit_url_method(body, headers1, method, url)
response = json.loads(response)
#
# response = getBaseStructure(zviceID, headers1, BASE_URL)
# response = json.loads(response)

# p_cardID = CM.create_txt_card("for task trials", "", zviceID, headers1, "", BASE_URL, "true","false")
p_cardID = 1958

# formID = FORMS.form_card(BASE_URL, headers1, "task trials", zviceID, str(p_cardID))

formID = 1960

task = {}
task['title'] = "task no 4 - Sayali testing"
task['duration'] = 2

usergroups = getAllUserGroups(headers1, zviceID, BASE_URL)
grplist = json.loads(usergroups)['output']['usergroup']
    # try:
grpID = grplist["A trial grp"]
task['grpID'] = grpID
response = CM.create_task_for_workflow(BASE_URL, zviceID, headers1, formID, task)

response = hit_url_method(body, headers1, method, url)
# response = CM.getBaseStructure(zviceID, headers1, BASE_URL)
response = json.loads(response)
print response
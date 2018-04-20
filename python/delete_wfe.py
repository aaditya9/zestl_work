import common as CM
import logon as LL
import json
import logging
import requests
import wfe_parser as WP
import time
import csv
import datetime

def delete_user_group(BASE_URL,zviceID,grp_ID):
    body = {}
    url = BASE_URL + "usergroups/" + str(grp_ID) + "/delete/" + zviceID
    method = "POST"
    response = CM.hit_url_method(body, headers1, method, url)
    return response


SERVER = "http://twig-me.com/" #Dev
version = "v13/"
BASE_URL = SERVER + version
zviceID = "WHGJ7HTVTDFH3" # Future group
email = "admin@zestl.com"
pwd = "TwigMeNow"
headers, headers1 = LL.req_headers(email, pwd, BASE_URL)
flow = ["TOP","MKT","NPD","COM","COE","PKG"]
# newtag = val1['subFlow'] + ":WFID_" + str(tagName) + ", wfe:" + val1['name']
# tagName = "TOP:WFID_369"

# this tag name i am using for to find out all top level cards in that workFlow Ex:- TOP,MKT,COE,COM,NPD,PKG ************
tagName = "WFID_369"
result = CM.get_all_tagIds(tagName,BASE_URL,zviceID,headers1)
print result
for ele in json.loads(result)['data']['elements']:
    cardID = ele['cardID']
    print cardID
#********************************************************

#*********  here i am finding the name of groups related to that WorkFlow ***********
wID = 369
for grp in flow:
    grpname = grp + "p_" + str(wID)
    print grpname
    result = CM.find_out_grp_ID(grpname,headers1,zviceID,BASE_URL)
    grp_ID = result
    result = delete_user_group(BASE_URL,zviceID,grp_ID)
    print result
#**************************************************************************

# tagName = "DOCSEARCH::WFID_369"
# result = CM.add_tags_future(CardIds, newtag, BASE_URL, body['BusinessTag'], headers1, body['WorkflowID'])
# result = CM.get_tags_by_cardID(cardID,BASE_URL,zviceID,headers1)
# result = CM.get_all_tagIds(tagName,BASE_URL,zviceID,headers1)
# print result
# for ele in json.loads(result)['data']['elements']:
#     cardID = ele['cardID']
#     print cardID

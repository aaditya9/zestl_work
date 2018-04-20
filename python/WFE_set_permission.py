import csv
import common as CM
import logon as LL
import json
import logging
import requests
import time
import csv
import datetime
import re

# SERVER = "http://twig-me.com/" #Dev
SERVER = "https://future.twig.me/"
# SERVER = "http://13.126.76.186/"    #future group server
version = "v13/"
BASE_URL = SERVER + version
zviceID = "WHGJ7HTVTDFH3" # Future group
# zviceID = "83H6LVUBRXWZ5"   # MInal dev server
# zviceID = "WKMUYXELA9LCC"  #Gene Path
email = "admin@zestl.com"
pwd = "TwigMeNow"
headers, headers1 = LL.req_headers(email, pwd, BASE_URL)

outfile = "C:/Users/Minal Thorat/Dropbox/Zestl-scripts/millennium/script_inputs/minal_try.csv"
cardIDlistFile = "C:/Users/Minal Thorat/MINAL OFFICE DATA\Hardik/PROD_Future_Group_forms_justCreated/form_tables.csv"
# cardIDlistFile = "C:/Users/Minal Thorat/MINAL OFFICE DATA/Hardik/6DEC_data_FG/form_tables.csv"
###### one wfe only below :::

def set_per(BASE_URL,zviceID,actionType,grpID,cardID):
    url = BASE_URL + 'card/permissions/' + zviceID
    method = "POST"
    body = {}
    body['opType'] = "1"
    body['actionType'] = actionType
    body['groupID'] = grpID
    body['cardID'] = cardID
    body['cardType'] = "GenericCard"
    response = CM.hit_url_method(body, headers1, method, url)
    return response


def delete_allowed(BASE_URL,cardID):
    url = BASE_URL + "card/permissions/" + zviceID
    method = "POST"
    body = {}
    body['opType'] = '2'
    body['groupID'] = -2001
    body['cardType'] = "GenericCard"
    body['cardID'] = cardID
    body['actionType'] = "ALLOWED_USERS"
    response = CM.hit_url_method(body, headers1, method, url)
    return response

    # TOP_WFE1:Milestones
    # Dependency
    # form, 75082

# group_name = "Milestone Dependency Form"
# cardID = 75082
# grp_ID = CM.find_out_grp_ID(group_name, headers1, zviceID, BASE_URL)
# print grp_ID
# result = set_per(BASE_URL,zviceID,"OPERATOR",grp_ID,cardID)
# print result

#
hasHeader = "Y"
cardList = {}
with open(cardIDlistFile, 'r') as rf:
    data = csv.reader(rf, delimiter=',')
    if hasHeader == "Y":
        row1 = data.next()

    for row in data:
        cardList[row[0]] = row[1]

    print cardList
counter = 0
with open(outfile, 'r') as of:
    data = csv.reader(of, delimiter=',')
    if hasHeader == "Y":
        row1 = data.next()
    for row in data:
        counter = counter + 1
        print counter
        formkey = row[0] + ":" + row[1]
        print "working for " + row[0] + " : " + row[1]
        cardID = cardList[formkey]
        view_per_grp = row[2]
        # print view_per_grp
        grp_name = view_per_grp.split(';')
        for name in grp_name:
            # print name
            grp_ID = CM.find_out_grp_ID(name, headers1, zviceID, BASE_URL)
            # print grp_ID
            result = set_per(BASE_URL,zviceID,"OPERATOR",grp_ID,cardID)
            print result

        # allwed = row[4]
        # result = delete_allowed(BASE_URL,cardID)
        # print result
        # a_name = allwed
        # grp_ID = CM.find_out_grp_ID(a_name, headers1, zviceID, BASE_URL)
        # # print grp_ID
        # result = set_per(BASE_URL, zviceID, "ALLOWED_USERS", grp_ID, cardID)
        # print result
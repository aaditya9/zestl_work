# ***************** USING FILE ********************* #

# import logon as LL
# import common as CM
# import json
# import csv
#
# SERVER = "https://twig.me/"
# version = "v8/"
# BASE_URL = SERVER + version
#
# def find(action):
#     for b in action['inputs'][1]['properties']:
#         title = "default"
#         if title == b['name']:
#             # print "----"
#             id = b['value']
#             # print id
#             return id
#
# hasHeader = "Y"
# email = "admin@zestl.com"
# pwd = "Zspladmin99"
# headers, headers1 = LL.req_headers(email, pwd, BASE_URL)
# GRfile = "C:/Users/Minal Thorat/Dropbox/Zestl-scripts/millennium/script_inputs/more_view.csv"
# csvfile = "C:/Users/Minal Thorat/Dropbox/Zestl-scripts/millennium/script_inputs/minal_users.csv"
# with open (csvfile, 'r') as infile:
#     data = csv.reader(infile, delimiter=',')
#     if hasHeader == "Y":
#         row1 = data.next()
#     counter = 0
#     for row in data:
#         counter += 1
#         print counter
#         zviceID = CM.force_decode(row[0].strip())
#         print "Working for this Zvice ID :- " + zviceID
#         jsondata = CM.getBaseStructure(zviceID, headers1, BASE_URL)
#         url = "https://twig.me/v8/all_actions/user/"+ zviceID
#         method = "GET"
#         body = {}
#         ja = CM.hit_url_method(body, headers1, method, url)
#         # print ja
#
#         url = "https://twig.me/v8/settings_action/user/" + zviceID
#         method = "POST"
#         body = {"cardType":"ORG_USER_CARD"}
#         ja = CM.hit_url_method(body, headers1, method, url)
#         # print ja
#
#         url = "https://twig.me/v8/user/communication/" + zviceID + "/groups"
#         method = "GET"
#         body ={}
#         ja = CM.hit_url_method(body, headers1, method, url)
#         for grpname in json.loads(ja)['data']['elements']:
#             with open(GRfile, 'r') as gfile:
#                 data1 = csv.reader(gfile, delimiter=',')
#                 if hasHeader == "Y":
#                     row2 = data1.next()
#                 # counter = 0
#                 for row in data1:
#                     # counter += 1
#                     # print counter
#                     name = CM.force_decode(row[0].strip())
#                     print "Working for this Group :- " + name
#                     if name == grpname['title']:
#                         # print "present"
#                         url = grpname['cardsjsonurl']
#                         method = grpname['method']
#                         ja = CM.hit_url_method(body, headers1, method, url)
#                         # print ja
#                         for grp in json.loads(ja)['data']['elements']:
#                             if "textcard" in grp['cardtype']:
#                                 # print "present"
#                                 for action in grp['actions']:
#                                     if "Remove User Group" == action['title']:
#                                         # print "present1111"
#                                         url = action['actionUrl']
#                                         method = action['method']
#                                         body = {}
#                                         id = find(action)
#                                         # print id
#                                         body['UserGroupID'] = id
#                                         ja = CM.hit_url_method(body, headers1, method, url)
#                                         print ja




# **************** Using Separate names ****************************#

import logon as LL
import common as CM
import json
import csv

SERVER = "https://twig.me/"
version = "v8/"
BASE_URL = SERVER + version

def find(action):
    for b in action['inputs'][1]['properties']:
        title = "default"
        if title == b['name']:
            # print "----"
            id = b['value']
            # print id
            return id

hasHeader = "Y"
email = "admin@zestl.com"
pwd = ""
headers, headers1 = LL.req_headers(email, pwd, BASE_URL)
GRfile = "C:/Users/Minal Thorat/Dropbox/Zestl-scripts/millennium/script_inputs/more_view.csv"
csvfile = "C:/Users/Minal Thorat/Dropbox/Zestl-scripts/millennium/script_inputs/minal_users.csv"
with open (csvfile, 'r') as infile:
    data = csv.reader(infile, delimiter=',')
    if hasHeader == "Y":
        row1 = data.next()
    counter = 0
    for row in data:
        counter += 1
        print counter
        zviceID = CM.force_decode(row[0].strip())
        print "Working for this Zvice ID :- " + zviceID
        jsondata = CM.getBaseStructure(zviceID, headers1, BASE_URL)
        url = "https://twig.me/v8/all_actions/user/"+ zviceID
        method = "GET"
        body = {}
        ja = CM.hit_url_method(body, headers1, method, url)
        # print ja

        url = "https://twig.me/v8/settings_action/user/" + zviceID
        method = "POST"
        body = {"cardType":"ORG_USER_CARD"}
        ja = CM.hit_url_method(body, headers1, method, url)
        # print ja

        url = "https://twig.me/v8/user/communication/" + zviceID + "/groups"
        method = "GET"
        body ={}
        ja = CM.hit_url_method(body, headers1, method, url)
        for grpname in json.loads(ja)['data']['elements']:
            if "Gtest1" == grpname['title']:
                print "working for : " + grpname['title']
                url = grpname['cardsjsonurl']
                method = grpname['method']
                ja = CM.hit_url_method(body, headers1, method, url)
                for grp in json.loads(ja)['data']['elements']:
                    if "textcard" in grp['cardtype']:
                        for action in grp['actions']:
                            if "Remove User Group" == action['title']:
                                url = action['actionUrl']
                                method = action['method']
                                body = {}
                                id = find(action)
                                body['UserGroupID'] = id
                                ja = CM.hit_url_method(body, headers1, method, url)
                                print ja

            elif "Gtest2" == grpname['title']:
                print "working for : " + grpname['title']
                url = grpname['cardsjsonurl']
                method = grpname['method']
                ja = CM.hit_url_method(body, headers1, method, url)
                for grp in json.loads(ja)['data']['elements']:
                    if "textcard" in grp['cardtype']:
                        for action in grp['actions']:
                            if "Remove User Group" == action['title']:
                                url = action['actionUrl']
                                method = action['method']
                                body = {}
                                id = find(action)
                                body['UserGroupID'] = id
                                ja = CM.hit_url_method(body, headers1, method, url)
                                print ja

            elif "Gtest3" == grpname['title']:
                print "working for : " + grpname['title']
                url = grpname['cardsjsonurl']
                method = grpname['method']
                ja = CM.hit_url_method(body, headers1, method, url)
                for grp in json.loads(ja)['data']['elements']:
                    if "textcard" in grp['cardtype']:
                        for action in grp['actions']:
                            if "Remove User Group" == action['title']:
                                url = action['actionUrl']
                                method = action['method']
                                body = {}
                                id = find(action)
                                body['UserGroupID'] = id
                                ja = CM.hit_url_method(body, headers1, method, url)
                                print ja
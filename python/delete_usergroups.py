#!/usr/local/bin/python

import base64
import time
import urllib2
from urllib2 import URLError
from urllib2 import HTTPError
import requests
import urllib
import json
import csv
import logon as LL
import common as CM


# def getAllUserGroups(headers, zbotID, BASE_URL):
#     url = BASE_URL + 'usergroups/' + zbotID
#     method = "GET"
#     body = {}
#     jsondata = CM.hit_url_method(body, headers, method, url)
#     return jsondata



if __name__ == '__main__':

    # SERVER = "https://twig.me/" # twigMe prod
    SERVER = "https://future.twig.me/"
    version = "v13/"
    # SERVER = "https://future.twig.me/v13/"
    BASE_URL = SERVER + version

    zbotID = "WHGJ7HTVTDFH3"

    email = "admin@zestl.com"
    pwd = "TwigMeNow"

    delfile = "C:/Users/Minal Thorat/Dropbox/Zestl-scripts/millennium/script_inputs/one.csv"
    # i must login
    headers, headers1 = LL.req_headers(email, pwd, BASE_URL)


    # usergroups = getAllUserGroups(headers1, zbotID, BASE_URL)
    # groups = json.loads(usergroups)['output']['usergroup']
    # for k, v in groups.items():
    #     print k

    with open(delfile, 'r') as rf:
        data = csv.reader(rf, delimiter=',')
        for row in data:
            try:
                grpname = row[0]
                result = CM.find_out_grp_ID(grpname,headers1,zbotID,BASE_URL)
                print result
                # grpID = groups[grpname]
                # print grpname + " : " + str(grpID)

                url = BASE_URL + "usergroups/" + str(result) + "/delete/" + zbotID
                body = {}
                method = "POST"
                result = CM.hit_url_method(body, headers1, method, url)
                print result
            except KeyError:
                print "usergroup " + row[0]  + " not found in database"
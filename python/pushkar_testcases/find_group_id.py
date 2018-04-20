import logon as LL
import time
import json

SERVER = "https://twig.me/"
version = "v8/"
BASE_URL = SERVER + version

ZbotID = "8SFKZCV5PFAXV"    ####  Business ID
email = "admin@zestl.com"
pwd = ""
allowedusers = "Minal"
headers, headers1 = LL.req_headers(email, pwd, BASE_URL)

def getAllUserGroups(headers, zbotID, BASE_URL):
    jsondata = LL.invoke_rest('GET', BASE_URL + 'usergroups/' + zbotID + "?filter={\"limit\":1000,\"offset\":0}", None, headers)
    return jsondata['reply']

usergroups = getAllUserGroups(headers1, ZbotID, BASE_URL)
print usergroups
grplist = json.loads(usergroups)['output']['usergroup']
grpID = grplist[allowedusers]
print grpID
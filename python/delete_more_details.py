import password as PW
import logon as LL
import common as CM
import json
import csv

SERVER = "http://twig.me/"
version = "v8/"
BASE_URL = SERVER + version

hasHeader = "Y"
# zviceID = "3W84QARF3DXLJ"    ####  minal prod Business ID

email = "admin@zestl.com"
pwd = PW.pwd
inputFile = "C:/Users/Minal Thorat/Dropbox/Zestl-scripts/millennium/script_inputs/Part5-190usersTagIds.csv"

headers, headers1 = LL.req_headers(email, pwd, BASE_URL)
def find(subac1):
    for b in subac1['inputs'][1]['properties']:
        title = "default"
        if title == b['name']:
            print "----"
            id = b['value']
            print id
            return id

with open(inputFile, 'r') as rf:
    data = csv.reader(rf, delimiter=',')
    if hasHeader == "Y":
        row1 = data.next()
    for row in data:
        zviceID = row[0].strip()
        jsondata = CM.getBaseStructure(zviceID, headers1, BASE_URL)
        for a in jsondata['data']['elements']:
            # title = "More Details"
            if "More Details" == a['title']:
                print "present"
                for action in a['actions']:
                    if "Explore" in action['title']:
                        body = {"interactionID": "CommonInteraction_INTERACTION_TYPE_SHOW_GENERIC_NOTES", "notetype": "P",
                                "useclubbing": "false"}
                        url = action['actionUrl']
                        method = "POST"
                        ja = CM.hit_url_method(body, headers1, method, url)
                        print ja
                        print "1st level"
                        for ac in json.loads(ja)['data']['elements']:
                            # title1 = "Age"
                            title1 = "textcard"
                            # if title1 == ac['title']:
                            if title1 in ac['cardtype']:
                                print "Found 2"
                                for subac1 in ac['actions']:
                                    title = "Delete"
                                    if title in subac1['title']:
                                        print "3rd level"
                                        id = find(subac1)
                                        print id
                                        method = "POST"
                                        url = subac1['actionUrl']
                                        body = {}
                                        body['interactionID'] = "CommonInteraction_INTERACTION_TYPE_DELETE_GENERIC_NOTE"
                                        body['noteid'] = id
                                        subja = CM.hit_url_method(body, headers1, method, url)
                                        print subja
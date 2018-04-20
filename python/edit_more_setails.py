import logon as LL
import common as CM
import json
import csv

SERVER = "http://twig.me/"
version = "v8/"
BASE_URL = SERVER + version
email = "admin@zestl.com"
pwd = "Zspladmin99"

hasHeader = "Y"
# zviceID = "E6XXXWNU4ZDKE"
hasHeader = "Y"
inputFile = "C:/Users/Minal Thorat/Dropbox/Zestl-scripts/millennium/script_inputs/minal_users.csv"
def find(action):
    for b in action['inputs'][3]['properties']:
        title = "default"
        if title == b['name']:
            # print "----"
            id = b['value']
            print id
            return id

headers, headers1 = LL.req_headers(email, pwd, BASE_URL)

with open(inputFile, 'r') as rf:
    data = csv.reader(rf, delimiter=',')
    if hasHeader == "Y":
        row1 = data.next()
    method = "POST"

    counter = 0
    for row in data:
        counter += 1
        print counter
        zviceID = row[0].strip()
        print "working for this zvice : " + zviceID
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
                        for sub in json.loads(ja)['data']['elements']:
                            if "B8 Teacher" == sub['title']:
                                print "present"
                                for action in sub['actions']:
                                    if "Edit" == action['title']:
                                        print "ready to edit"
                                        body = {}
                                        action['method']
                                        action['actionUrl']
                                        id = find(action)
                                        # print id
                                        body['noteheader'] = "B8 Teacher"
                                        body['note'] = "Ms. Shreeya Sonawane"
                                        body['interactionID'] = "CommonInteraction_INTERACTION_TYPE_MODIFY_GENERIC_NOTE"
                                        body['noteid'] = id
                                        ja = CM.hit_url_method(body, headers1, method, url)
                                        print ja
import json
import csv
import logon as LL
import common as CM
import re
import requests
import base64


SERVER = "https://twig.me/"
version = "v8/"
BASE_URL = SERVER + version
hasHeader = "Y"
# zviceID = "W66SB4Z8BRJ7R"    ####  Business ID
email = "admin@zestl.com"
pwd = "Zspladmin99"
inputFile = "C:/Users/Minal Thorat/Dropbox/Zestl-scripts/millennium/script_inputs/one.csv"
headers, headers1 = LL.req_headers(email, pwd, BASE_URL)
def find(subaction):
    for b in subaction['inputs'][0]['properties']:
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
        zviceID = row[0]
        print "working on :  " + zviceID
        jsondata = CM.getBaseStructure(zviceID, headers1, BASE_URL)
        for a in jsondata['data']['elements']:
            # title = "About Me! "
            if "About Me! " == a['title']:
                print "card found"
                url = a['cturl']
                method = a['ctmethod']
                body = json.loads(a['ctjsondata'])
                # body  = {"parentCardID":7950}
                print body
                jaction = CM.hit_url_method(body, headers1, method, url)
                print jaction
            # else:print " card not found"
                for sub in json.loads(jaction)['data']['elements']:
                    title = "About Me! "
                    if title == sub['title']:
                        print "ready to delete"
                        for action in sub['actions']:
                            title = "All actions"
                            if title == action['title']:
                                url = action['actionUrl']
                                method = action['method']
                                body = {}
                                jaction = CM.hit_url_method(body, headers1, method, url)
                                print jaction
                                for subaction in json.loads(jaction)['data']['ondemand_action']:
                                    if "Delete" == subaction['title']:
                                        print "go"
                                        id = find(subaction)
                                        print id
                                        url = subaction['actionUrl']
                                        method = subaction['method']
                                        body = {}
                                        body['cardID'] = id
                                        body['opType'] = 2
                                        body['interactionID'] = "CommonInteraction_INTERACTION_TYPE_CARD_OPERATION"
                                        jaction = CM.hit_url_method(body, headers1, method, url)
                                        print jaction
                    else:print "card is not present"
            else:print "not found card"
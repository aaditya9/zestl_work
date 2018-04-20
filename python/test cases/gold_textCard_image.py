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
zviceID = "W66SB4Z8BRJ7R"    ####  Business ID
email = "admin@zestl.com"
pwd = "Zspladmin99"
# inputFile = "C:/Users/Minal Thorat/Dropbox/Zestl-scripts/millennium/script_inputs/card_not_present_tags.csv"
headers, headers1 = LL.req_headers(email, pwd, BASE_URL)
# with open(inputFile, 'r') as rf:
#     data = csv.reader(rf, delimiter=',')
#     if hasHeader == "Y":
#         row1 = data.next()
#     for row in data:
#         zviceID = row[0]
#         print "working on :  " + zviceID
jsondata = CM.getBaseStructure(zviceID, headers1, BASE_URL)
for a in jsondata['data']['elements']:
    if "About Me! " == a['title']:
        print "found"
        for sub in a['actions']:
            if "All actions" == sub['title']:
                url = sub['actionUrl']
                method = sub['method']
                body = {}
                jaction = CM.hit_url_method(body, headers1, method, url)
                print jaction
                for ondemand in json.loads(jaction)['data']['ondemand_action']:
                    if "Profile Image" == ondemand['title']:
                        print "ready to update"
                        url = ondemand['actionUrl']
                        method = ondemand['method']
                        fname = "C:/Users/Minal Thorat/Dropbox/Zestl-Deployment/TEST_ATTACHMENT/About Me!.png"
                        print url
                        with open(fname, "rb") as image_file:
                            encoded_string = base64.b64encode(image_file.read())
                        encoded_string = encoded_string.encode('utf8')
                        body = {}
                        typ = "img/jpg"
                        body['media_name'] = "About Me!.png"
                        body['media'] = encoded_string
                        body['media_type'] = typ
                        body['media_ext'] = "png"
                        body['media_size'] = 120000
                        body['remove'] = False
                        body['media_compressed'] = True
                        jaction = CM.hit_url_method(body, headers1, method, url)
                        print jaction
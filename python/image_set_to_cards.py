import json
import csv
import logon as LL
import common as CM
import re
import requests
import base64


SERVER = "https://twig.me/"
# SERVER = "http://35.154.64.11/"
version = "v5/"
BASE_URL = SERVER + version

zviceID = "DU8BFMK4WUBZF"    ####  Business ID

email = "admin@zestl.com"
pwd = "Zspladmin99"

headers, headers1 = LL.req_headers(email, pwd, BASE_URL)

jsondata = CM.getBaseStructure(zviceID, headers1, BASE_URL)

for a in jsondata['data']['elements']:
    title = "Body Analysis"
    if title in a['title']:
        print "1st level"
        for b in a['actions']:
            title = "Set Background Image"
            if title in b['title']:
                print "2nd level"
                url = b['actionUrl']
                method = "POST"
                imgFile = "C:/Users/User/Dropbox/Zestl-Deployment/minal/minal.jpg"
                with open(imgFile, "rb") as image_file:
                    encoded_string = base64.b64encode(image_file.read())
                encoded_string = encoded_string.encode('utf8')
                # print encoded_string\
                typ = "img/jpg"
                body = {}
                body['media'] = encoded_string
                body['media_type'] = typ
                body['media_ext'] = "jpg"
                body['media_size'] = 120000
                body['media_name'] = "minal.png"
                body['remove'] = 'false'
                print CM.hit_url_method(body, headers1, method, url)
                print "done"


import json
import logon as LL
import common as CM
import re
import requests
import csv


SERVER = "https://www.twig.me/"
version = "v8/"
BASE_URL = SERVER + version
zviceID = "8SFKZCV5PFAXV"    ####  Business ID
email = "minal@zestl.com"
pwd = "minal123"
headers, headers1 = LL.req_headers(email, pwd, BASE_URL)
jsondata = CM.getBaseStructure(zviceID, headers1, BASE_URL)
for a in jsondata['data']['elements']:
    title = "TEXT"
    if title == a['title']:
        print "present"
        url = "https://twig.me/v8/all_actions/8SFKZCV5PFAXV/textcard/102"
        method = "GET"
        body = {}
        ja = CM.hit_url_method(body, headers1, method, url)
        print ja
        for sub in json.loads(ja)['data']['ondemand_action']:
            if "User Permission Settings" == sub['title']:
                # print "found"
                url = "https://twig.me/v8/permission_action/8SFKZCV5PFAXV/permission/102"
                method = "POST"
                body = {}
                body['cardType'] = "TEXT"
                ja = CM.hit_url_method(body, headers1, method, url)
                print ja
                for sub1 in json.loads(ja)['data']['ondemand_action']:
                    if "Communication Preferences" == sub1['title']:
                        url = "https://twig.me/v8/permissions/communication/8SFKZCV5PFAXV"
                        method = "POST"
                        body = {}
                        body['cardType'] = "GenericCard"
                        body['cardID'] = 102
                        ja = CM.hit_url_method(body, headers1, method, url)
                        print ja
                        for sub2 in json.loads(ja)['data']['elements']:
                            if "Communication via Mail/Notification" == sub2['title']:
                                url = sub2['cardsjsonurl']
                                method = "POST"
                                body = {}
                                body['cardType'] = "GenericCard"
                                body['cardID'] = 102
                                body['actionType'] = "MAIL"
                                ja = CM.hit_url_method(body, headers1, method, url)
                                print ja
                                for sub3 in json.loads(ja)['data']['elements']:
                                    if "textcard" == sub3['cardtype']:
                                        for sub4 in sub3['actions']:
                                            if "Settings" == sub4['title']:
                                                for sub5 in sub4['actions']:
                                                    if "Mail / Notification" == sub5['title']:
                                                        print "FOUND"
                                                        url = sub5['actionUrl']
                                                        method = sub5['method']
                                                        body = {}
                                                        body['cardType'] = "GenericCard"
                                                        body['cardID'] = 102
                                                        body['actionType'] = "MAIL"
                                                        body['sendMail'] = "true"
                                                        body['sendNotification'] = "true"
                                                        ja = CM.hit_url_method(body, headers1, method, url)
                                                        print ja